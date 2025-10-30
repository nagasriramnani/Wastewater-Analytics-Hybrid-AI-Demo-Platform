# Demo Script

This document provides a step-by-step guide for demonstrating the Wastewater Analytics Platform.

## Pre-Demo Setup (5 minutes)

1. **Start the application**:
   ```bash
   make run
   ```

2. **Verify sample data exists**:
   - Check `app/data/raw/wwtp_sample.csv` exists
   - If not, run: `python scripts/generate_synthetic.py`

3. **Open browser** to `http://localhost:8501`

## Demo Flow (15-20 minutes)

### Step 1: Dashboard Overview (2 min)

**Narrative**: "Let me show you the platform overview."

**Actions**:
- Navigate to Dashboard
- Point out: "The platform provides a comprehensive analytics solution for wastewater operations"
- Show: KPI cards, trend visualization (if data loaded)
- Explain: "This is our central hub for quick insights"

**Key Points**:
- Professional UI with Aqua Analytics theme
- Real-time KPIs
- Quick access to all features

### Step 2: Data Onboarding (3 min)

**Narrative**: "First, let's load some data."

**Actions**:
- Go to "🤖 AI Training Studio"
- Show: Upload and Select Sample tabs
- Select: "wwtp_sample.csv" from sample datasets
- Click: "Load Sample Dataset"

**Key Points**:
- Smart schema detection
- Data quality dashboard
- Automatic column identification

### Step 3: Model Training (4 min)

**Narrative**: "Now let's train multiple AI models to find the best one."

**Actions**:
1. Configure training:
   - Date column: "date" (auto-selected)
   - Site column: "site_id" (auto-selected)
   - Target: "effluent_bod"

2. Show training configuration:
   - Max rows: 5000 (for demo speed)
   - Horizon: 30 days

3. Click: "🚀 Train All Models"

4. During training:
   - Show progress indicators
   - Explain: "We're training LightGBM, Prophet, and Random Forest"

5. After training:
   - Show metrics comparison table
   - Explain: "LightGBM typically performs best"
   - Show: "Best model is automatically selected"

**Key Points**:
- Multiple models trained simultaneously
- Fast training (<90s for demo data)
- Automatic model comparison
- Models saved to registry

### Step 4: Forecasting (3 min)

**Narrative**: "Let's generate predictions for the next 30 days."

**Actions**:
1. Navigate to "📊 Forecasting Hub"

2. Show model selection:
   - Select "best" model
   - Explain: "Using the best performing model"

3. Configure forecast:
   - Horizon: 30 days
   - Confidence: 95%

4. Generate forecast:
   - Click "🚀 Generate Forecast"
   - Show interactive chart:
     - Historical data (blue line)
     - Forecast (green dashed line)
     - Confidence intervals (shaded area)

5. Scenario analysis:
   - Adjust flow slider: +10%
   - Adjust temperature: +5%
   - Click "Update Forecast with Scenarios"
   - Show: "Forecast adjusted based on operational changes"

**Key Points**:
- Interactive forecasts with confidence intervals
- Scenario analysis for planning
- Clear visualization

### Step 5: Anomaly Detection (2 min)

**Narrative**: "Now let's identify any anomalies in our data."

**Actions**:
1. Navigate to "🚨 Anomaly Detection Center"

2. Configure detection:
   - Target: "effluent_bod"
   - Method: Z-score
   - Threshold: 3.0

3. Detect anomalies:
   - Click "🔍 Detect Anomalies"
   - Show timeline chart with anomalies highlighted
   - Show anomaly table with scores

4. Root cause analysis:
   - Click on an anomaly
   - Show feature deviations

**Key Points**:
- Multiple detection methods
- Visual timeline
- Root cause analysis

### Step 6: Explainability (2 min)

**Narrative**: "Let's understand why the model makes certain predictions."

**Actions**:
1. Navigate to "🔍 Explainability Lab"

2. Show feature importance:
   - Bar chart of top features
   - Explain: "These features are most important"

3. SHAP explanations (if LightGBM):
   - Show summary plot
   - Explain: "Red increases prediction, blue decreases"

4. What-If analysis:
   - Adjust feature sliders
   - Show: "Predictions update in real-time"

**Key Points**:
- Transparent AI decisions
- Interactive what-if scenarios
- Multiple explanation methods

### Step 7: Benchmarking (2 min)

**Narrative**: "Let's compare performance across multiple treatment plants."

**Actions**:
1. Navigate to "📈 Benchmarking Suite"

2. Select sites:
   - Select 3 sites
   - Choose metrics: effluent_bod, effluent_cod, energy_kwh

3. Generate benchmark:
   - Click "📊 Generate Benchmark"
   - Show comparison table
   - Show radar chart
   - Explain: "Visual comparison of performance"

**Key Points**:
- Multi-site comparison
- Visual radar charts
- Easy performance benchmarking

### Step 8: Reporting (2 min)

**Narrative**: "Finally, let's generate a professional report."

**Actions**:
1. Navigate to "🧾 Reporting"

2. Configure report:
   - Title: "Q1 2024 Wastewater Analytics Report"
   - Author: "Analytics Team"
   - Format: PDF
   - Include: All sections

3. Generate report:
   - Click "📊 Generate Report"
   - Show download button
   - Explain: "Professional report with all findings"

**Key Points**:
- Multiple output formats (PDF/PPTX/HTML)
- Customizable sections
- Professional presentation

## Closing (1 min)

**Summary points**:
1. "We've demonstrated a complete analytics workflow"
2. "The platform combines multiple AI models for robust predictions"
3. "Everything runs locally - no data leaves your environment"
4. "All models are explainable and transparent"

**Questions to anticipate**:
- "Can it handle larger datasets?" → Yes, adjust max_rows parameter
- "Can I add custom models?" → Yes, see architecture guide
- "Is it production-ready?" → Framework is production-grade, customize for your needs

## Troubleshooting During Demo

**If training takes too long**:
- Reduce max_rows to 2000
- Explain: "For demo speed, we limit rows"

**If a model fails**:
- Explain: "Occasionally models may fail with certain data types"
- Continue with remaining models

**If data doesn't load**:
- Check file exists: `app/data/raw/wwtp_sample.csv`
- Re-generate: `python scripts/generate_synthetic.py`

## Demo Checklist

- [ ] Application runs without errors
- [ ] Sample data exists
- [ ] All pages accessible
- [ ] Models train successfully
- [ ] Forecasts generate
- [ ] Reports can be created
- [ ] Browser window ready
- [ ] Presentation screen/projector ready

## Tips for Success

1. **Practice first**: Run through the demo once before presenting
2. **Have backup**: Keep sample data file ready
3. **Focus on value**: Emphasize business outcomes, not just tech
4. **Be flexible**: Skip sections if short on time
5. **End strong**: Always show the report generation as a strong finish



