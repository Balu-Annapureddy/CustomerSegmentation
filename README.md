# 📊 Customer Segmentation Web Application (RFM Analysis)

A Flask-based web application that performs **Customer Segmentation** using RFM (Recency, Frequency, Monetary) analysis and multiple clustering algorithms.

## ✨ Features

- **RFM Analysis**: Automatically calculates Recency, Frequency, and Monetary values
- **Multiple Clustering Algorithms**: 
  - K-Means
  - Hierarchical (Agglomerative)
  - DBSCAN (Density-Based)
- **Interactive 3D Visualization**: Plotly-powered 3D scatter plots
- **Data Export**: Download segmented customer data as CSV
- **Session Management**: Secure, multi-user support
- **Tunable Parameters**: Adjust cluster count and DBSCAN parameters

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip installed

### Setup & Installation

1. **Clone the repository** (if using Git)
```bash
git clone <your-repo-url>
cd Customer-Segmentation
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

| OS | Command |
|---|---|
| Windows (PowerShell) | `.\venv\Scripts\Activate.ps1` |
| Windows (CMD) | `venv\Scripts\activate.bat` |
| macOS / Linux | `source venv/bin/activate` |

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

**Option 1: One-Click (Windows)**
```bash
run.bat
```

**Option 2: Manual**
```bash
# Activate venv first (see above)
python app.py
```

Open your browser and navigate to: **http://127.0.0.1:8000**

## 💾 Usage Workflow

### 1. Upload Data
Upload a CSV or Excel file containing:
- `InvoiceDate`
- `CustomerID`
- `Quantity`
- `UnitPrice`

### 2. Select Algorithm
Choose your clustering method:
- **K-Means / Hierarchical**: Specify number of clusters (2-10)
- **DBSCAN**: Adjust `eps` and `min_samples` parameters

### 3. View Results
- **Cluster Metrics**: Silhouette score and cluster sizes
- **2D Plot**: Recency vs. Monetary scatter plot
- **3D Interactive Plot**: Explore all three RFM dimensions
- **Segment Summary**: Average RFM values per cluster
- **Download**: Export results as CSV

## 🗂️ Project Structure
```
Customer-Segmentation/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── run.bat                     # Quick-start script (Windows)
├── .gitignore                  # Git ignore rules
├── templates/                  # HTML templates
│   ├── base.html
│   ├── upload.html
│   ├── select_algorithm.html
│   └── results.html
├── static/
│   └── plots/                  # Auto-generated plots
└── ml/                         # ML modules
    ├── preprocessing.py        # RFM calculation
    ├── clustering.py           # Clustering algorithms
    ├── evaluation.py           # Metrics
    └── visualizations.py       # Plotting functions
```

## ⚙️ Technical Details

### RFM Model
- **Recency**: Days since last purchase
- **Frequency**: Number of purchases
- **Monetary**: Total amount spent

### Security Features
- Session-based file management (no global state)
- Environment variable support for secret keys
- 100MB file upload limit

### Visualization
- **Matplotlib**: 2D scatter plots
- **Plotly**: Interactive 3D visualizations

## 📝 License
This project was created as a B.Tech final year mini project.