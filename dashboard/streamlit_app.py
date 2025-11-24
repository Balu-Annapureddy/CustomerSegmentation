import streamlit as st
import pandas as pd
import os
import sys

# Add project root to system path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from ml.preprocessing import load_data, basic_cleaning, build_rfm
from ml.clustering import run_kmeans, run_hierarchical
from ml.evaluation import evaluate_clusters
from ml.visualizations import plot_clusters, plot_rfm_distributions

# Paths
BASE_DIR = ROOT_DIR
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")
st.title("🛍 Customer Segmentation Dashboard")

# File uploader
uploaded = st.sidebar.file_uploader("Upload CSV/XLSX Dataset", type=["csv", "xlsx"])

if uploaded:
    filename = uploaded.name
    savepath = os.path.join(DATA_DIR, filename)
    with open(savepath, "wb") as f:
        f.write(uploaded.getbuffer())
    st.sidebar.success(f"Saved uploaded file as: {filename}")
    df = load_data(savepath)
else:
    st.sidebar.info("Using sample data from /data folder")
    default_file = "Online Retail.xlsx"
    savepath = os.path.join(DATA_DIR, default_file)
    df = load_data(savepath)

# Cleaning + RFM
df = basic_cleaning(df)

required_cols = {"InvoiceDate", "CustomerID", "Quantity", "UnitPrice"}
rfm = None
if required_cols.issubset(df.columns):
    rfm = build_rfm(df)
    st.subheader("📊 RFM Analysis")
    st.success("RFM dataset created successfully!")
    st.dataframe(rfm.head())

    dist_figs = plot_rfm_distributions(rfm)
    if isinstance(dist_figs, list):
        for fig in dist_figs:
            st.pyplot(fig)
    else:
        st.pyplot(dist_figs)
else:
    st.warning("⚠ Dataset missing required columns for RFM analysis (InvoiceDate/CustomerID/Quantity/UnitPrice).")

# Stop if RFM not created
if rfm is None:
    st.stop()

# Clustering options
st.sidebar.header("Clustering Options")
algorithm = st.sidebar.selectbox("Select Algorithm", ["KMeans", "Hierarchical"])

if algorithm == "KMeans":
    clusters, model = run_kmeans(rfm)
else:
    clusters, model = run_hierarchical(rfm)

rfm["Cluster"] = clusters

# Evaluation
metrics = evaluate_clusters(rfm)
st.subheader("Cluster Evaluation Metrics")
st.json(metrics)

# Cluster plots
st.subheader("Cluster Visualization")
fig = plot_clusters(rfm)
st.pyplot(fig)
