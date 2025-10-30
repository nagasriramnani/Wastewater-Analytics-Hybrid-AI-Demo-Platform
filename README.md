# 💧 Wastewater Analytics & Hybrid-AI Demo Platform (v2.0)

A production-grade Streamlit application demonstrating hybrid-AI capabilities for wastewater treatment plant operations. Built with a focus on enterprise-level UX, local-first privacy, and comprehensive analytics.

## 🎯 Features

- **🏠 Dashboard**: Real-time KPIs, trend visualizations, and quick actions
- **🤖 AI Training Studio**: Train multiple ML models (LightGBM, Prophet, Random Forest) with live progress tracking
- **📊 Forecasting Hub**: Generate forecasts with confidence intervals and scenario analysis
- **🚨 Anomaly Detection**: Identify outliers using z-score and IQR methods with root-cause analysis
- **🔍 Explainability Lab**: SHAP explanations, partial dependence plots, and what-if analysis
- **📈 Benchmarking Suite**: Multi-site comparison with radar charts and period-over-period analysis
- **🧾 Professional Reporting**: Generate PDF, PPTX, and HTML reports with customizable sections

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   make setup
   ```
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

5. **Generate sample data** (optional):
   ```bash
   python scripts/generate_synthetic.py
   ```

6. **Run the application**:
   ```bash
   make run
   ```
   Or directly:
   ```bash
   streamlit run app/streamlit_app.py
   ```

7. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
wastewater-ai-platform/
├── app/
│   ├── ui/              # UI components and pages
│   ├── ai/              # ML models and pipeline
│   ├── data/            # Sample datasets and model registry
│   └── streamlit_app.py # Main entrypoint
├── config/              # Configuration files
├── docs/                # Documentation
├── reports/             # Generated reports
├── scripts/             # Utility scripts
├── tests/               # Test suite
└── requirements.txt     # Python dependencies
```

## 📊 Sample Data

Sample datasets are located in `app/data/raw/`:
- `wwtp_sample.csv`: Synthetic wastewater treatment plant data (1095 rows)
- `uci_sample.csv`: UCI Water Treatment style dataset (500 rows)

Generate more data:
```bash
python scripts/generate_synthetic.py
```

## 🧪 Testing

Run the test suite:
```bash
make test
```

Run specific test categories:
```bash
pytest tests/test_pipeline.py    # Pipeline tests
pytest tests/test_models.py       # Model tests
pytest tests/test_ui_smoke.py     # UI smoke tests
pytest tests/test_reports.py      # Report generation tests
```

## 🛠️ Development

### Code Quality

Format code:
```bash
make fmt
```

Lint code:
```bash
make lint
```

Type checking:
```bash
make typecheck
```

### Running Tests

```bash
make test
```

## 📖 Documentation

- [Architecture Guide](docs/architecture.md)
- [User Guide](docs/user-guide.md)
- [Demo Script](docs/demo-script.md)

## 🎨 Design System

The platform uses the **Aqua Analytics** theme:
- Primary Color: `#1f77b4` (Blue)
- Success/Teal: `#2ca07c`
- Alert: `#ff7f0e` (Orange)
- Background: `#f8f9fa` (Light Gray)

Typography: Inter (body) and Fira Mono (code)

## 🔒 Privacy & Security

- **Local-first**: All processing happens locally
- **No external calls**: No data transmission to external services
- **Session isolation**: Each Streamlit session is independent
- **Input sanitization**: All inputs are validated

## 📝 Usage Example

1. **Upload Data**: Go to AI Training Studio → Upload Dataset
2. **Train Models**: Select target column and click "Train All Models"
3. **View Forecasts**: Navigate to Forecasting Hub and generate predictions
4. **Detect Anomalies**: Use Anomaly Detection Center to identify outliers
5. **Explain Results**: Open Explainability Lab for SHAP explanations
6. **Generate Report**: Create professional PDF/PPTX reports in Reporting

## 🐛 Troubleshooting

**Issue**: Module not found errors
- **Solution**: Ensure virtual environment is activated and dependencies are installed

**Issue**: Models fail to train
- **Solution**: Check that target column has sufficient non-null values (>10%)

**Issue**: Reports fail to generate
- **Solution**: Ensure `reports/` directory exists and is writable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- ML Models: LightGBM, Prophet, scikit-learn
- Visualization: Plotly
- Design inspiration: Modern analytics dashboards

## 📧 Support

For issues and questions, please open an issue on the repository.

---

**Made with 💧 for wastewater operations**



