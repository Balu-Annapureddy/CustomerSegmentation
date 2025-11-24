import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import plotly

def plot_clusters(df, feature_x="Recency", feature_y="Monetary", label_col="Cluster"):
    """
    Creates a scatter plot of clusters using Recency vs. Monetary.
    """
    # FIX: Explicitly create figure and axes
    fig, ax = plt.subplots(figsize=(8,6)) 
    
    # Plot using the axes object
    sns.scatterplot(data=df, x=feature_x, y=feature_y, hue=label_col, palette="tab10", s=70, ax=ax)
    
    ax.set_title(f"Cluster Plot: {feature_x} vs {feature_y}")
    plt.tight_layout()
    
    return fig # FIX: Return the FIGURE object (not plt)

def plot_rfm_distributions(rfm_df):
    """
    Creates a 3-panel histogram plot for RFM distributions.
    """
    fig, axes = plt.subplots(1,3,figsize=(18,5))
    for i, metric in enumerate(["Recency","Frequency","Monetary"]):
        sns.histplot(rfm_df[metric], kde=True, ax=axes[i])
        axes[i].set_title(f"{metric} Distribution")
    plt.tight_layout()
    return fig

def plot_clusters_3d(df, x="Recency", y="Frequency", z="Monetary", color="Cluster"):
    """
    Creates a 3D scatter plot using Plotly.
    Returns the JSON representation of the plot.
    """
    # Convert cluster to string to ensure discrete colors
    df = df.copy()
    df[color] = df[color].astype(str)
    
    fig = px.scatter_3d(
        df, x=x, y=y, z=z, color=color,
        title="3D Cluster Visualization (Recency, Frequency, Monetary)",
        opacity=0.7,
        size_max=10
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)