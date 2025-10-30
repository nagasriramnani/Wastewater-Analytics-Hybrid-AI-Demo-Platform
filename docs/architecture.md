# Architecture Guide

## System Overview

The Wastewater Analytics Platform is built as a modular Streamlit application with a clean separation between UI, business logic, and ML components.

## Architecture Layers

### 1. Presentation Layer (`app/ui/`)

- **Pages** (`app/ui/pages/`): Streamlit page modules
- **Components** (`app/ui/components/`): Reusable UI components (KPICard, TrendCard, etc.)
- **Theme** (`app/ui/theme/`): Design system and styling
- **State** (`app/ui/state/`): Session state management
- **Export** (`app/ui/export/`): Report generation

### 2. AI/ML Layer (`app/ai/`)

#### Models (`app/ai/models/`)
- `LightGBMRegressor`: Gradient boosting model
- `ProphetForecaster`: Time series forecasting
- `RandomForestRegressor`: Ensemble regression

#### Pipeline (`app/ai/pipeline/`)
- `DataIngestionEngine`: Data loading and schema detection
- `FeatureFactory`: Feature engineering (lags, rolling windows, time features)
- `ModelOrchestrator`: Coordinates model training and evaluation
- `ValidationSuite`: Data quality and model validation
- `ServingLayer`: Model persistence and prediction serving

#### Utils (`app/ai/utils/`)
- Metrics calculation (MAE, RMSE, SMAPE, etc.)
- Anomaly scoring algorithms

### 3. Data Layer (`app/data/`)

- `raw/`: Sample datasets and uploaded files
- `processed/`: Processed/engineered datasets
- `registry/`: Trained models and artifacts

## Data Flow

```
User Upload → DataIngestionEngine → FeatureFactory
                                          ↓
ModelOrchestrator → Model Training → ServingLayer
                                          ↓
UI Pages ← StateManager ← Predictions/Results
```

## Design Patterns

### 1. Factory Pattern
- `FeatureFactory`: Creates feature sets from raw data
- `ComponentLibrary`: Creates UI components

### 2. Orchestrator Pattern
- `ModelOrchestrator`: Coordinates complex ML workflows

### 3. Manager Pattern
- `ThemeManager`: Manages theme and styling
- `StateManager`: Manages session state
- `ExportManager`: Manages report generation

## Configuration

Configuration files in `config/`:
- `settings.yaml`: Application settings (theme, thresholds, defaults)
- `logging.yaml`: Logging configuration

## Security Considerations

- Local-first: No external API calls
- Session isolation: Each Streamlit session is independent
- Input validation: All inputs validated before processing
- No sensitive data logging

## Performance Optimizations

- Model training: Early stopping, row limits for demos
- Caching: Streamlit @st.cache_data for expensive operations
- Lazy loading: Page modules loaded on demand

## Extensibility

To add a new model:
1. Create class in `app/ai/models/` inheriting from `BaseModel`
2. Implement `fit()` and `predict()` methods
3. Add to `ModelOrchestrator.train_all()`

To add a new page:
1. Create module in `app/ui/pages/`
2. Implement `render()` function
3. Add route in `app/streamlit_app.py`

## Technology Stack

- **UI Framework**: Streamlit 1.28.0
- **ML Libraries**: LightGBM 4.0.0, Prophet 1.1.0, scikit-learn 1.3.0
- **Visualization**: Plotly 5.15.0
- **Explainability**: SHAP 0.42.0
- **Reporting**: ReportLab, python-pptx, WeasyPrint
- **Data**: pandas, numpy

## Testing Strategy

- Unit tests: Individual components (models, pipelines, utils)
- Integration tests: End-to-end workflows
- Smoke tests: UI components and basic functionality



