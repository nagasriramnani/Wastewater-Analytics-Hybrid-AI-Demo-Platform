# 🚀 Quick Start - Run This Project

## Option A: With Python 3.11 (Full ML Features) ⭐ Recommended

```powershell
# 1. Install Python 3.11 from python.org (see SETUP_GUIDE.md)

# 2. Create new virtual environment
py -3.11 -m venv venv311
.\venv311\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application (on port 8502 to avoid conflicts)
streamlit run app/streamlit_app.py --server.port 8502

# 5. Open browser: http://localhost:8502
```

## Option B: With Python 3.14 (UI Only - No ML Training)

```powershell
# 1. Activate current venv
.\venv\Scripts\activate

# 2. Run application
streamlit run app/streamlit_app.py --server.port 8502

# Note: ML features (training, forecasting) will show errors
# But you can still see the UI and data visualization
```

## What Runs Where

| Project | Python Version | Port | Status |
|---------|---------------|------|--------|
| Your Old Project | 3.14 | 8501 | ✅ Running |
| This Water-AI Project | 3.11 (need to install) | 8502 | ⏳ Need Python 3.11 |

## After Setup

1. **Load sample data**: AI Training Studio → Select `wwtp_sample.csv`
2. **Train models**: Click "Train All Models" (works with Python 3.11)
3. **Generate forecasts**: Forecasting Hub
4. **View explainability**: Explainability Lab
5. **Create reports**: Reporting page

---

**Your old project on port 8501 is safe and untouched!** ✅



