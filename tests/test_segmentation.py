# -*- coding: utf-8 -*-
"""
CustomerSegmentation Unit Test Suite
Tests data preprocessing, RFM metric calculation, feature scaling, and K-Means clustering algorithms.
"""

import sys
import os
import unittest
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.preprocessing import basic_cleaning, build_rfm
from ml.clustering import scale_features, run_kmeans


class TestCustomerSegmentation(unittest.TestCase):

    def setUp(self):
        """Construct synthetic e-commerce transaction dataset."""
        today = datetime.now()
        data = {
            'InvoiceNo': ['536365', '536365', '536366', '536367', '536368'],
            'StockCode': ['85123A', '71053', '22633', '84879', '22960'],
            'Description': ['WHITE HANGING HEART', 'WHITE METAL LANTERN', 'HAND WARMER', 'ASSORTED COLOUR BIRD', 'JAM MAKING SET'],
            'Quantity': [6, 6, 6, 32, 6],
            'InvoiceDate': [
                today - timedelta(days=10),
                today - timedelta(days=10),
                today - timedelta(days=5),
                today - timedelta(days=2),
                today - timedelta(days=1)
            ],
            'UnitPrice': [2.55, 3.39, 1.85, 1.69, 4.25],
            'CustomerID': [17850, 17850, 17850, 13047, 13047],
            'Country': ['United Kingdom'] * 5
        }
        self.raw_df = pd.DataFrame(data)

    def test_basic_cleaning(self):
        """Test column normalization and NaN removal."""
        cleaned = basic_cleaning(self.raw_df)
        self.assertEqual(len(cleaned), 5)
        self.assertIn('CustomerID', cleaned.columns)

    def test_build_rfm(self):
        """Test Recency, Frequency, and Monetary calculation."""
        cleaned = basic_cleaning(self.raw_df)
        rfm = build_rfm(cleaned)
        
        self.assertEqual(len(rfm), 2)  # Two unique customers (17850, 13047)
        self.assertIn('Recency', rfm.columns)
        self.assertIn('Frequency', rfm.columns)
        self.assertIn('Monetary', rfm.columns)

    def test_scale_features(self):
        """Test StandardScaler normalization."""
        cleaned = basic_cleaning(self.raw_df)
        rfm = build_rfm(cleaned)
        scaled, cols = scale_features(rfm)
        
        self.assertEqual(scaled.shape[0], 2)
        self.assertEqual(scaled.shape[1], 3)

    def test_kmeans_clustering(self):
        """Test K-Means model fitting."""
        cleaned = basic_cleaning(self.raw_df)
        rfm = build_rfm(cleaned)
        labels, model = run_kmeans(rfm, n_clusters=2)
        
        self.assertEqual(len(labels), 2)
        self.assertIsNotNone(model)


if __name__ == "__main__":
    unittest.main()
