# Setup Guide - Installing Python 3.11 for ML Features

## Current Situation
- ✅ You have Python 3.14 (current)
- ✅ Your old project is running on localhost (keep it!)
- ❌ This project needs Python 3.11/3.13 for ML libraries (LightGBM, Prophet, SHAP)

## Solution: Install Python 3.11 Side-by-Side

You can have **multiple Python versions** installed without affecting your existing project!

### Step 1: Download Python 3.11

1. Go to: https://www.python.org/downloads/release/python-31111/
2. Download: **Windows installer (64-bit)** - `python-3.11.11-amd64.exe`
3. **Important**: During installation, check ✅ **"Add python.exe to PATH"**
4. **Also check**: ✅ **"Install for all users"** (optional but recommended)

### Step 2: Verify Installation

Open a **NEW** terminal/PowerShell and run:
```powershell
py -3.11 --version
```
Should show: `Python 3.11.11`

### Step 3: Create Separate Virtual Environment for This Project

```powershell
# Navigate to this project
cd C:\Water-AI

# Create venv with Python 3.11 (won't affect your old project!)
py -3.11 -m venv venv311

# Activate it
.\venv311\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 4: Run the Application

```powershell
# Make sure venv311 is activated
.\venv311\Scripts\activate

# Run on different port (8502) so it doesn't conflict with your old project
streamlit run app/streamlit_app.py --server.port 8502
```

## Benefits of This Approach

✅ **Your old project stays untouched** - It still uses Python 3.14  
✅ **This project gets Python 3.11** - Full ML functionality  
✅ **Both can run simultaneously** - Different ports (8501 vs 8502)  
✅ **No conflicts** - Separate virtual environments

## Quick Commands Reference

```powershell
# For your OLD project (Python 3.14):
.\venv\Scripts\activate
# (your existing commands)

# For THIS project (Python 3.11):
.\venv311\Scripts\activate
streamlit run app/streamlit_app.py --server.port 8502
```

## Troubleshooting

**Q: Can I uninstall Python 3.11 later?**  
A: Yes! Multiple Python versions don't interfere. Uninstall from "Add or Remove Programs" if needed.

**Q: Will this affect my old project?**  
A: No! Virtual environments are isolated. Your old project keeps using Python 3.14.

**Q: Why not use Python 3.14?**  
A: ML libraries (LightGBM, Prophet, SHAP) don't support Python 3.14 yet. They need 3.11-3.13.

## Alternative: Use Anaconda/Miniconda

If you prefer conda:
```powershell
# Install Miniconda from https://docs.conda.io/en/latest/miniconda.html
# Then:
conda create -n water-ai python=3.11
conda activate water-ai
pip install -r requirements.txt
```

---

**Need help?** The project is ready - just needs Python 3.11!



