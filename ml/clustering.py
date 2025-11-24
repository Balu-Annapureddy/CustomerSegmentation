import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

def scale_features(df):
    """
    Scales the RFM features (Recency, Frequency, Monetary) using StandardScaler.
    """
    feature_cols = ['Recency', 'Frequency', 'Monetary']
    numeric_df = df[feature_cols] 
    
    scaler = StandardScaler()
    scaled = scaler.fit_transform(numeric_df)
    
    return scaled, feature_cols

def run_kmeans(df, n_clusters=5):
    scaled, _ = scale_features(df)
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto') 
    labels = model.fit_predict(scaled)
    return labels, model

def run_dbscan(df, eps=0.5, min_samples=5):
    scaled, _ = scale_features(df)
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(scaled) 
    return labels, model

def run_hierarchical(df, n_clusters=5):
    scaled, _ = scale_features(df)
    model = AgglomerativeClustering(n_clusters=n_clusters)
    labels = model.fit_predict(scaled)
    return labels, model