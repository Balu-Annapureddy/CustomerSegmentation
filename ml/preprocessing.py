import pandas as pd
import numpy as np

def basic_cleaning(df):
    """
    Performs basic data cleaning steps: 
    - Cleans column names.
    - Converts InvoiceDate to datetime.
    - Drops NaNs from CustomerID and converts to int.
    - Filters out non-positive Quantity and UnitPrice.
    """
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

    if 'CustomerID' in df.columns:
        df = df.dropna(subset=['CustomerID'])
        try:
            df['CustomerID'] = df['CustomerID'].astype(int) 
        except Exception:
            pass

    if 'Quantity' in df.columns:
        df = df[df['Quantity'].astype(float) > 0]
    if 'UnitPrice' in df.columns:
        df = df[df['UnitPrice'].astype(float) > 0]

    df = df.drop_duplicates().reset_index(drop=True)
    return df

def build_rfm(df, reference_date=None):
    """
    Calculates Recency, Frequency, and Monetary values for each customer.
    """
    df = df.copy()
    if 'InvoiceDate' not in df.columns or 'CustomerID' not in df.columns:
        raise ValueError("For RFM you need 'InvoiceDate' and 'CustomerID' columns")

    if reference_date is None:
        reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
        df['Amount'] = df['Quantity'].astype(float) * df['UnitPrice'].astype(float)
    else:
        df['Amount'] = 0.0

    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'Amount': 'sum'
    }).rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'Amount': 'Monetary'}).reset_index()

    rfm = rfm[rfm['Monetary'] > 0].reset_index(drop=True)
    return rfm