"""AI Training Studio page."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from app.ui.components.library import ComponentLibrary
from app.ui.state.manager import StateManager
from app.ai.pipeline.ingestion import DataIngestionEngine
from app.ai.pipeline.orchestrator import ModelOrchestrator
from app.ai.pipeline.serving import ServingLayer


def render():
    """Render the AI Training Studio page."""
    ComponentLibrary.section_header("🤖 AI Training Studio")
    
    # Data upload/selection section
    st.markdown("### 📁 Data Onboarding")
    
    upload_tab, select_tab = st.tabs(["Upload Dataset", "Select Sample"])
    
    with upload_tab:
        uploaded_file = st.file_uploader(
            "Upload wastewater dataset (CSV, Excel, Parquet)",
            type=['csv', 'xlsx', 'xls', 'parquet'],
            help="Upload a dataset with date, site, and target columns",
        )
        
        if uploaded_file is not None:
            try:
                ingestion = DataIngestionEngine()
                # Save temporarily
                temp_path = Path("app/data/raw/temp_upload.csv")
                temp_path.parent.mkdir(parents=True, exist_ok=True)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                df = ingestion.load_from_path(str(temp_path))
                StateManager.set_dataset(df, str(temp_path))
                st.success(f"✅ Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    with select_tab:
        sample_files = list(Path("app/data/raw").glob("*.csv"))
        if sample_files:
            selected_file = st.selectbox(
                "Select sample dataset",
                [f.name for f in sample_files],
            )
            if st.button("Load Sample Dataset"):
                try:
                    ingestion = DataIngestionEngine()
                    df = ingestion.load_from_path(str(Path("app/data/raw") / selected_file))
                    StateManager.set_dataset(df, str(Path("app/data/raw") / selected_file))
                    st.success(f"✅ Sample dataset loaded: {len(df)} rows")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading sample: {str(e)}")
        else:
            st.info("No sample datasets found. Generate one or upload your own.")
    
    # Show current dataset info
    df = StateManager.get_dataset()
    if df is not None:
        st.markdown("### 📊 Dataset Overview")
        
        # Data quality dashboard
        ingestion = DataIngestionEngine()
        stats = ingestion.validate_data(df)
        ComponentLibrary.data_quality_card(stats)
        
        # Schema detection
        schema = ingestion.detect_schema(df)
        
        col1, col2 = st.columns(2)
        with col1:
            date_col = st.selectbox(
                "Date Column",
                [None] + list(df.columns),
                index=0 if schema['date_column'] is None else list(df.columns).index(schema['date_column']) + 1,
                key="train_date_col",
            )
        
        with col2:
            site_col = st.selectbox(
                "Site/Station Column",
                [None] + list(df.columns),
                index=0 if schema['site_column'] is None else list(df.columns).index(schema['site_column']) + 1,
                key="train_site_col",
            )
        
        target_col = st.selectbox(
            "Target Column",
            schema['target_columns'] if schema['target_columns'] else schema['numeric_columns'][:10],
            key="train_target_col",
        )
        
        # Training configuration
        st.markdown("### ⚙️ Training Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            max_rows = st.number_input(
                "Max Rows (for demo speed)",
                min_value=100,
                max_value=50000,
                value=5000,
                step=100,
            )
            horizon = st.number_input(
                "Forecast Horizon (days)",
                min_value=7,
                max_value=365,
                value=30,
            )
        
        with col2:
            early_stopping = st.number_input(
                "Early Stopping Rounds",
                min_value=10,
                max_value=200,
                value=50,
            )
        
        # Model gallery
        st.markdown("### 🤖 Model Gallery")
        st.info("Available models: **LightGBM**, **Prophet**, **Random Forest**")
        
        # Train button
        if st.button("🚀 Train All Models", type="primary", use_container_width=True):
            if df is None or target_col is None:
                st.error("Please load a dataset and select a target column.")
            else:
                with st.spinner("Training models... This may take a moment."):
                    try:
                        orchestrator = ModelOrchestrator(
                            max_rows=max_rows,
                            early_stopping_rounds=early_stopping,
                        )
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("Preparing data...")
                        progress_bar.progress(20)
                        
                        result = orchestrator.train_all(
                            df,
                            target_col,
                            date_col=date_col,
                            site_col=site_col,
                            horizon=horizon,
                        )
                        
                        progress_bar.progress(80)
                        status_text.text("Saving models...")
                        
                        # Save models
                        serving = ServingLayer()
                        for model_name, model in result.models.items():
                            if model is not None:
                                metadata = {
                                    'target': target_col,
                                    'date_col': date_col,
                                    'site_col': site_col,
                                    'metrics': result.metrics.get(model_name, {}),
                                    'feature_names': result.feature_names,  # Store feature names
                                }
                                serving.save_model(model, f"{model_name}_{target_col}", metadata)
                                StateManager.set_model(model_name, model)
                        
                        StateManager.set_model("best", result.models.get(result.best_model_key))
                        st.session_state.training_result = result
                        
                        # Store training metadata for forecasting
                        st.session_state.training_metadata = {
                            'target': target_col,
                            'date_col': date_col,
                            'site_col': site_col,
                            'feature_names': result.feature_names,
                        }
                        
                        progress_bar.progress(100)
                        status_text.text("Training complete!")
                        
                        st.success(f"✅ Training complete! Best model: **{result.best_model_key}**")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Training failed: {str(e)}")
                        st.exception(e)
        
        # Show training results if available
        if 'training_result' in st.session_state:
            st.markdown("### 📈 Training Results")
            result = st.session_state.training_result
            
            # Metrics comparison table
            metrics_df = pd.DataFrame(result.metrics).T
            st.dataframe(metrics_df.style.format("{:.4f}"), use_container_width=True)
            
            # Visualization
            fig = go.Figure()
            for model_name, metrics in result.metrics.items():
                if 'rmse' in metrics:
                    fig.add_trace(go.Bar(
                        x=[model_name],
                        y=[metrics['rmse']],
                        name=model_name,
                        text=f"{metrics['rmse']:.2f}",
                        textposition='auto',
                    ))
            
            fig.update_layout(
                title="Model RMSE Comparison",
                yaxis_title="RMSE",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)



