from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_session import Session
import os
import pandas as pd
import matplotlib
# Set the backend to Agg, which is designed for non-interactive rendering
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import io
import base64

# Import ALL necessary functions
from ml.preprocessing import basic_cleaning, build_rfm
from ml.clustering import run_kmeans, run_hierarchical, run_dbscan
from ml.evaluation import evaluate_clusters
from ml.visualizations import plot_clusters, plot_clusters_3d

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'data'
app.config['PLOT_FOLDER'] = 'static/plots'
# Use environment variable for secret key, fallback to a random string if not set (for dev)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_prod')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Initialize Session
Session(app)

# Ensure plot and data folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PLOT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return redirect(url_for('upload_file'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file:
            filename = file.filename
            lower_name = filename.lower()
            
            try:
                # Read data directly from the uploaded file object (stream)
                if lower_name.endswith('.csv'):
                    df_raw = pd.read_csv(file)
                elif lower_name.endswith(('.xlsx', '.xls')):
                    df_raw = pd.read_excel(file, engine='openpyxl')
                else:
                    flash("Unsupported file type. Supported: CSV, XLSX, XLS.", 'error')
                    return redirect(request.url)
                
                # Clean and Process RFM
                df_cleaned = basic_cleaning(df_raw)
                
                # Check for required RFM columns
                required_cols = {"InvoiceDate", "CustomerID", "Quantity", "UnitPrice"}
                if not required_cols.issubset(df_cleaned.columns):
                    flash("Missing required columns for RFM analysis: InvoiceDate, CustomerID, Quantity, UnitPrice.", 'error')
                    return redirect(request.url)
                
                rfm_df = build_rfm(df_cleaned)

                if rfm_df.empty:
                     flash("RFM dataset is empty after filtering for positive Monetary value.", 'error')
                     return redirect(request.url)
                
                # Save to session-specific file
                file_id = str(uuid.uuid4())
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.pkl")
                rfm_df.to_pickle(file_path)
                
                session['file_id'] = file_id
                flash(f"Successfully loaded and processed RFM for {len(rfm_df)} customers.", 'success')
                
                return redirect(url_for('select_algorithm'))
            except Exception as e:
                flash(f"Error processing file: {e}", 'error')
                print(f"Error details: {e}") 
                return redirect(request.url)

    return render_template('upload.html')

@app.route('/select', methods=['GET', 'POST'])
def select_algorithm():
    if 'file_id' not in session:
        flash("Please upload a dataset first.", 'warning')
        return redirect(url_for('upload_file'))
        
    if request.method == 'POST':
        algo = request.form.get('algorithm')
        n_clusters = request.form.get('n_clusters', 5)
        
        # DBSCAN params
        eps = request.form.get('eps', 0.5)
        min_samples = request.form.get('min_samples', 5)
        
        return redirect(url_for('results', algorithm=algo, n_clusters=n_clusters, eps=eps, min_samples=min_samples))
        
    return render_template('select_algorithm.html')

@app.route('/results/<algorithm>')
def results(algorithm):
    if 'file_id' not in session:
        flash("RFM data not found. Please re-upload.", 'error')
        return redirect(url_for('upload_file'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session['file_id']}.pkl")
    if not os.path.exists(file_path):
        flash("Session expired or file lost. Please re-upload.", 'error')
        return redirect(url_for('upload_file'))

    rfm_df = pd.read_pickle(file_path)
    
    # Get params
    n_clusters = request.args.get('n_clusters', 5, type=int)
    eps = request.args.get('eps', 0.5, type=float)
    min_samples = request.args.get('min_samples', 5, type=int)

    try:
        if algorithm.lower() == 'kmeans':
            labels, model = run_kmeans(rfm_df, n_clusters=n_clusters)
        elif algorithm.lower() == 'hierarchical':
            labels, model = run_hierarchical(rfm_df, n_clusters=n_clusters)
        elif algorithm.lower() == 'dbscan':
            labels, model = run_dbscan(rfm_df, eps=eps, min_samples=min_samples)
        else:
            flash(f"Algorithm '{algorithm}' not supported.", 'error')
            return redirect(url_for('select_algorithm'))
    except Exception as e:
        flash(f"Error running clustering algorithm: {e}", 'error')
        print(f"Clustering Error: {e}")
        return redirect(url_for('select_algorithm'))

    # Add clusters to the DataFrame
    rfm_df["Cluster"] = labels
    
    # Save updated DF with clusters back to session file (for export)
    rfm_df.to_pickle(file_path)
    
    # Run Evaluation
    metrics = evaluate_clusters(rfm_df)
    
    # ------------------
    # Generate Plots
    # ------------------
    # 1. Matplotlib 2D Plot (Base64)
    fig = plot_clusters(rfm_df)
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    # 2. Plotly 3D Plot (JSON)
    plotly_json = plot_clusters_3d(rfm_df)

    # Prepare data for display
    segment_summary = rfm_df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean().round(2).reset_index()
    segment_summary = segment_summary.to_html(classes='table table-striped', index=False)
    
    # Filter out the noise label (-1) for better display if using DBSCAN
    cluster_counts_filtered = {k: v for k, v in metrics['cluster_counts'].items() if k != -1}
    
    return render_template(
        'results.html', 
        plot_url=plot_url,
        plotly_json=plotly_json,
        algorithm=algorithm.capitalize(),
        metrics=metrics,
        segment_summary=segment_summary,
        cluster_counts=cluster_counts_filtered
    )

@app.route('/download')
def download_results():
    if 'file_id' not in session:
        flash("No data to download.", 'error')
        return redirect(url_for('upload_file'))
        
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session['file_id']}.pkl")
    if not os.path.exists(file_path):
        flash("File not found.", 'error')
        return redirect(url_for('upload_file'))
        
    rfm_df = pd.read_pickle(file_path)
    
    # Convert to CSV
    output = io.BytesIO()
    rfm_df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='customer_segments.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, port=8000)