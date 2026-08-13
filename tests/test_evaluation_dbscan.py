# -*- coding: utf-8 -*-
"""
CustomerSegmentation DBSCAN & Evaluation Unit Test Suite
Tests DBSCAN density clustering, Silhouette score calculation, and invalid data handling.
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.preprocessing import basic_cleaning, build_rfm
from ml.clustering import run_dbscan, run_hierarchical
from ml.evaluation import evaluate_clusters


class TestCustomerSegmentationEval(unittest.TestCase):

    def setUp(self):
        """Construct synthetic multi-customer transaction dataset."""
        data = {
            'InvoiceNo': ['1', '2', '3', '4', '5', '6'],
            'Quantity': [10, 5, 2, 50, 1, -5],  # includes negative invalid quantity
            'UnitPrice': [5.0, 10.0, 15.0, 2.0, 1.0, 10.0],
            'CustomerID': [101, 102, 103, 104, 105, None],  # includes NaN CustomerID
            'InvoiceDate': pd.date_range(start='2026-01-01', periods=6, freq='D')
        }
        self.raw_df = pd.DataFrame(data)

    def test_invalid_data_filtering(self):
        """Test filtering out negative quantities and NaN customer IDs."""
        cleaned = basic_cleaning(self.raw_df)
        self.assertEqual(len(cleaned), 5)  # 6th row dropped due to negative quantity & NaN CustomerID

    def test_dbscan_clustering(self):
        """Test DBSCAN model execution."""
        cleaned = basic_cleaning(self.raw_df)
        rfm = build_rfm(cleaned)
        labels, model = run_dbscan(rfm, eps=1.5, min_samples=2)
        self.assertEqual(len(labels), len(rfm))

    def test_silhouette_evaluation(self):
        """Test Silhouette score computation for cluster evaluation."""
        cleaned = basic_cleaning(self.raw_df)
        rfm = build_rfm(cleaned)
        labels, _ = run_hierarchical(rfm, n_clusters=2)
        rfm['Cluster'] = labels
        metrics = evaluate_clusters(rfm, label_col='Cluster')
        self.assertIn('silhouette_score', metrics)


if __name__ == "__main__":
    unittest.main()
