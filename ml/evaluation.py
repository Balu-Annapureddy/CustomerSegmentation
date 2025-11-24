from sklearn.metrics import silhouette_score
from ml.clustering import scale_features 

def evaluate_clusters(df, label_col="Cluster"):
    """
    Evaluates clusters using Silhouette Score on scaled RFM features.
    """
    if label_col not in df.columns:
        raise ValueError("Cluster column not found")
    
    scaled_data, _ = scale_features(df)
    labels = df[label_col]
    
    # Filter out noise points (-1) from DBSCAN before scoring
    if -1 in labels.unique():
        clean_mask = labels != -1
        scaled_data = scaled_data[clean_mask]
        labels = labels[clean_mask]

    score = None
    try:
        if len(labels.unique()) > 1 and len(scaled_data) > 1:
            score = silhouette_score(scaled_data, labels) 
    except Exception as e:
        print(f"Error during silhouette_score calculation: {e}")
        score = None

    counts = df[label_col].value_counts().to_dict()
    return {"silhouette_score": score, "cluster_counts": counts}