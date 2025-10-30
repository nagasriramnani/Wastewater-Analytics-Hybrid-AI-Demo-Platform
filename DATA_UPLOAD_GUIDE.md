# 📊 Data Upload Guide - AI Training Studio

## What to Upload

The AI Training Studio accepts **wastewater treatment plant data** in CSV or Excel format.

### Recommended Data Format

Your CSV/Excel file should contain columns like:

#### Essential Columns:
- **Date/Time Column**: 
  - Column names: `date`, `timestamp`, `datetime`, `time`
  - Format: Any date format (YYYY-MM-DD, DD/MM/YYYY, etc.)
  
- **Site/Station Column** (optional for multi-site data):
  - Column names: `site_id`, `station`, `location`, `plant`, `site`
  - Format: Text/string values (e.g., "WWTP_01", "Plant A")

#### Target Variables (What You Want to Predict):
- `effluent_bod` - Biochemical Oxygen Demand (mg/L)
- `effluent_cod` - Chemical Oxygen Demand (mg/L)
- `effluent_tss` - Total Suspended Solids (mg/L)
- `nh4` - Ammonia (mg/L)
- `no3` - Nitrate (mg/L)
- `po4` - Phosphate (mg/L)

#### Feature Variables (Predictors):
- `influent_bod`, `influent_cod`, `influent_tss`
- `flow_m3d` - Flow rate (m³/day)
- `temperature_c` - Temperature (°C)
- `aeration_kwh` - Aeration energy (kWh)
- `energy_kwh` - Total energy consumption (kWh)

### Sample Data Structure

```
date,site_id,influent_bod,effluent_bod,flow_m3d,temperature_c,...
2019-01-01,WWTP_01,45.2,8.5,2500,18.5,...
2019-01-02,WWTP_01,47.1,7.9,2600,18.8,...
```

## Quick Start Options

### Option 1: Use Pre-loaded Sample Data ⭐ Easiest

1. Go to **AI Training Studio** page
2. Click **"Select Sample"** tab
3. Select **`wwtp_sample.csv`** 
4. Click **"Load Sample Dataset"**

This will load pre-generated sample data with:
- 1,095 rows (3 sites × 365 days)
- 15 columns (dates, sites, targets, features)
- Ready for training immediately!

### Option 2: Upload Your Own Data

1. Go to **AI Training Studio** page
2. Click **"Upload Dataset"** tab
3. Upload CSV/Excel file with:
   - Date column
   - Target variable (what you want to predict)
   - Feature columns (predictors)
4. The system will auto-detect schema!

## Example CSV Format

```csv
date,site_id,influent_bod,effluent_bod,influent_cod,effluent_cod,flow_m3d,temperature_c,aeration_kwh,energy_kwh
2024-01-01,WWTP_01,45.2,8.5,120.3,25.4,2500,18.5,150,450
2024-01-02,WWTP_01,47.1,7.9,125.6,24.8,2600,18.8,155,465
2024-01-03,WWTP_01,44.8,8.2,118.9,26.1,2480,18.2,148,442
```

## Minimum Requirements

- **At least 100 rows** (more is better)
- **At least 1 numeric target column** (BOD, COD, TSS, etc.)
- **Date column** (for time series features)
- **Some feature columns** (for predictions)

## What Happens After Upload

1. ✅ **Schema Detection**: System automatically finds date, site, and target columns
2. ✅ **Data Quality Check**: Validates missing data, duplicates, ranges
3. ✅ **Ready to Train**: Configure training and click "Train All Models"

## Tips

- **For Best Results**: Include 6+ months of daily data
- **Multiple Sites**: Include site_id column for site-specific training
- **Clean Data**: Remove extreme outliers before upload (or let system handle it)
- **Target Selection**: Choose a target with <10% missing values

## Current Sample Data

You already have sample data ready:
- `wwtp_sample.csv` - 1,095 rows, 15 columns, 3 sites
- `uci_sample.csv` - 500 rows, 11 columns

**Just select "wwtp_sample.csv" from the dropdown and click "Load Sample Dataset"!** 🚀

---

**Need Help?** The system will guide you through schema detection and show data quality metrics before training.

