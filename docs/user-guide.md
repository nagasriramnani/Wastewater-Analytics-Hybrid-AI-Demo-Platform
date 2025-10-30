# User Guide

## Getting Started

### First Time Setup

1. Ensure you have Python 3.9+ installed
2. Create and activate virtual environment
3. Install dependencies: `make setup`
4. Generate sample data: `python scripts/generate_synthetic.py`
5. Run the app: `make run`

## Navigation

The application has 7 main pages accessible via the sidebar:

### 🏠 Dashboard

**Purpose**: Overview of current dataset and key metrics

**Features**:
- KPI cards showing current values
- Trend visualizations
- Quick action buttons

**Usage**:
1. Load a dataset (see AI Training Studio)
2. View KPIs and trends
3. Quick access to other features

### 🤖 AI Training Studio

**Purpose**: Train and compare ML models

**Workflow**:
1. **Upload or Select Dataset**:
   - Upload: Drag and drop CSV/Excel file
   - Select: Choose from sample datasets

2. **Configure Training**:
   - Select date column (if time series)
   - Select site/station column (if multi-site)
   - Choose target variable

3. **Train Models**:
   - Click "Train All Models"
   - Wait for training to complete (<90s for demo data)
   - View metrics comparison

4. **Save Models**:
   - Models are automatically saved to registry
   - Best model is marked automatically

### 📊 Forecasting Hub

**Purpose**: Generate predictions and forecasts

**Workflow**:
1. Select trained model
2. Configure forecast:
   - Horizon (7-365 days)
   - Confidence interval
   - Target variable

3. Generate forecast:
   - Click "Generate Forecast"
   - View interactive chart with intervals

4. Scenario Analysis:
   - Adjust flow, temperature, aeration sliders
   - See adjusted forecast

### 🚨 Anomaly Detection Center

**Purpose**: Identify outliers and anomalies

**Workflow**:
1. Select target variable
2. Choose detection method:
   - Z-score (default)
   - IQR (Interquartile Range)

3. Set threshold (1.0-5.0)

4. Detect anomalies:
   - View timeline with anomalies highlighted
   - Review anomaly table
   - Analyze root causes

### 🔍 Explainability Lab

**Purpose**: Understand model predictions

**Features**:
- Global feature importance
- SHAP explanations (for LightGBM)
- Partial Dependence Plots
- What-If Analysis

**Workflow**:
1. Select trained model
2. View feature importance charts
3. For LightGBM: See SHAP summary plots
4. Generate PDP for specific features
5. Use What-If to test scenarios

### 📈 Benchmarking Suite

**Purpose**: Compare performance across sites

**Workflow**:
1. Select sites to compare
2. Choose metrics for benchmarking
3. Generate benchmark:
   - View comparison table
   - See radar chart
   - Period-over-period analysis

### 🧾 Reporting

**Purpose**: Generate professional reports

**Workflow**:
1. Configure report:
   - Title, subtitle, author
   - Output format (PDF/PPTX/HTML)
   - Sections to include

2. Generate report:
   - Click "Generate Report"
   - Download when ready

## Tips & Best Practices

### Data Preparation

- Ensure date column is parseable (YYYY-MM-DD format preferred)
- Remove extreme outliers before training
- Ensure target column has <10% missing values

### Model Training

- Start with sample data to test workflow
- Use "Max Rows" limit for faster demos
- Compare multiple models before selecting best

### Forecasting

- Longer horizons (90+ days) work best with Prophet
- Shorter horizons (7-30 days) work well with LightGBM
- Use scenario analysis for planning

### Anomaly Detection

- Start with default threshold (3.0)
- Review anomalies manually before taking action
- Use root-cause analysis to understand why

### Reporting

- Include all relevant sections for comprehensive reports
- Charts are embedded in PDF/PPTX
- HTML reports are interactive

## Troubleshooting

### Model Training Fails

- **Check**: Target column has sufficient data
- **Check**: Date column is correctly parsed
- **Solution**: Reduce max rows or fix data issues

### Forecasts Look Wrong

- **Check**: Model was trained on similar data
- **Check**: Forecast horizon is reasonable
- **Solution**: Retrain with more data

### Reports Won't Generate

- **Check**: `reports/` directory exists
- **Check**: Write permissions
- **Solution**: Create directory manually if needed

## Keyboard Shortcuts

- `Ctrl+R`: Refresh page (browser)
- `Ctrl+F`: Find in page
- `Esc`: Close dialogs

## Getting Help

- Check [README](../README.md) for setup issues
- Review [Architecture Guide](architecture.md) for technical details
- Open an issue on GitHub for bugs



