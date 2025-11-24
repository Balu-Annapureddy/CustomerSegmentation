📊 Customer Segmentation Web Application (RFM Analysis)

This project is a Flask-based web application that performs Customer Segmentation using:

RFM Model → Recency, Frequency, Monetary

Clustering Algorithms → K-Means, Hierarchical, DBSCAN

Users can upload transaction data, choose an algorithm, and view:

Cluster scatter plots

Evaluation metrics

Segment summaries

🚀 Getting Started

To run this application, you must set up a Python virtual environment to avoid dependency conflicts.

✅ 1. Prerequisites

Python 3.8+

pip installed

🔧 2. Setup (Using a Virtual Environment)
A. Create the Virtual Environment

Navigate to the project's root directory:

# Create a virtual environment named 'venv'
python -m venv venv

B. Activate the Virtual Environment

You must activate it every time before running the project.

Operating System	Command
Windows (Command Prompt)	venv\Scripts\activate.bat
Windows (PowerShell)	venv\Scripts\Activate.ps1
macOS / Linux	source venv/bin/activate

When active, your terminal will look like:

(venv) C:\>

C. Install Dependencies

After activation:

pip install -r requirements.txt

▶️ 3. Running the Application

With (venv) active:

python app.py


You will see:

 * Running on http://127.0.0.1:8000


Open this in your browser:

👉 http://127.0.0.1:8000

💾 Usage & Workflow
1. Upload Data

Upload a CSV/XLSX file containing:

InvoiceDate

CustomerID

Quantity

UnitPrice

2. Select Algorithm

Choose from:

K-Means

Hierarchical

DBSCAN

(Optional: choose number of clusters)

3. View Results

You will see:

✔ Scatter plot (Recency vs. Monetary)
✔ Silhouette Score
✔ Segment summary table (mean RFM per cluster)

🗂️ Project Structure
Customer-Segmentation/
├── app.py                      # Main Flask backend
├── requirements.txt            # Project dependencies
├── templates/                  # HTML files
│   ├── base.html
│   ├── upload.html
│   ├── select_algorithm.html
│   └── results.html
├── static/
│   └── plots/                  # Auto-generated cluster plots
└── ml/
    ├── preprocessing.py        # RFM calculation
    ├── clustering.py           # K-Means, Hierarchical, DBSCAN
    ├── evaluation.py           # Silhouette metrics
    └── visualizations.py       # Matplotlib plotting

⚙️ Technical Details
RFM Model

Recency = Days since last purchase

Frequency = Number of purchases

Monetary = Total amount spent

Removes invalid rows (Quantity <= 0 or UnitPrice <= 0)

Feature Scaling

Uses StandardScaler to avoid biased clustering.

Plotting

Plots saved as PNG inside static/plots/ using Matplotlib’s non-interactive backend.