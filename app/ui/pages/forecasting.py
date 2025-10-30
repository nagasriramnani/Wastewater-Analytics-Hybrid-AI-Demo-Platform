"""Forecasting Hub page."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from app.ui.components.library import ComponentLibrary
from app.ui.state.manager import StateManager
from app.ai.pipeline.serving import ServingLayer
from app.ai.pipeline.ingestion import DataIngestionEngine
from app.ai.pipeline.features import FeatureFactory


def render():
    """Render the Forecasting Hub page."""
    ComponentLibrary.section_header("📊 Forecasting Hub")
    
    df = StateManager.get_dataset()
    if df is None:
        ComponentLibrary.empty_state(
            "No dataset loaded. Please upload a dataset from the AI Training Studio.",
            icon="📊",
        )
        return
    
    # Get trained models
    models = StateManager.get_all_models()
    if not models:
        ComponentLibrary.alert_banner(
            "No trained models found. Please train models in the AI Training Studio first.",
            alert_type="warning",
        )
        return
    
    # Model selection
    model_options = list(models.keys()) + ["best"]
    selected_model_key = st.selectbox("Select Model", model_options)
    model = models.get(selected_model_key) if selected_model_key != "best" else StateManager.get_model("best")
    
    if model is None:
        st.error("Selected model is not available.")
        return
    
    # Forecasting configuration
    st.markdown("### ⚙️ Forecast Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        horizon = st.slider(
            "Forecast Horizon (days)",
            min_value=7,
            max_value=365,
            value=30,
        )
        confidence = st.selectbox(
            "Confidence Interval",
            [0.8, 0.9, 0.95],
            index=2,
        )
    
    with col2:
        # Target selection
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        target_col = st.selectbox("Target Variable", numeric_cols[:10])
    
    # Generate forecast
    if st.button("🚀 Generate Forecast", type="primary"):
        with st.spinner("Generating forecast..."):
            try:
                # Check if we have training metadata
                training_metadata = st.session_state.get('training_metadata', {})
                
                # Get date and site columns from metadata or auto-detect
                ingestion = DataIngestionEngine()
                schema = ingestion.detect_schema(df)
                date_col = training_metadata.get('date_col') or schema.get('date_column')
                site_col = training_metadata.get('site_col') or schema.get('site_column')
                
                serving = ServingLayer()
                
                # Try Prophet first (works with raw time series data)
                if hasattr(model, 'forecast') and hasattr(model, 'model') and hasattr(model, 'target_col'):
                    # Prophet model - use its forecast method
                    forecast_result = serving.forecast(model, df, horizon=horizon)
                elif isinstance(model, dict) and 'forecast' in dir(model):
                    forecast_result = serving.forecast(model, df, horizon=horizon)
                else:
                    # For non-time-series models, we need feature engineering
                    # Check if model was trained with feature engineering
                    feature_names = training_metadata.get('feature_names')
                    
                    if feature_names and len(feature_names) > 0:
                        # Model was trained with features - need to engineer same features
                        try:
                            # Build features using same factory settings
                            factory = FeatureFactory(max_lags=7)
                            feature_set = factory.build(
                                df,
                                target_col=target_col,
                                date_col=date_col,
                                site_col=site_col,
                                test_size=0.0,  # Use all data for forecasting
                                val_size=0.0,
                            )
                            
                            # Get last row's features for prediction
                            if len(feature_set.train_X) > 0:
                                last_features = feature_set.train_X.iloc[[-1]]
                                
                                # Ensure columns match (may have some missing lags at end)
                                # Use only features that exist in both
                                model_features = []
                                if hasattr(model, 'feature_names_in_'):
                                    model_features = list(model.feature_names_in_)
                                elif hasattr(model, 'model') and hasattr(model.model, 'feature_name_'):
                                    model_features = list(model.model.feature_name_)
                                
                                if model_features:
                                    # Align features
                                    available_features = [f for f in model_features if f in last_features.columns]
                                    if available_features:
                                        X_pred = last_features[available_features]
                                        # Fill any missing with 0
                                        for col in model_features:
                                            if col not in X_pred.columns:
                                                X_pred[col] = 0
                                        X_pred = X_pred[model_features]  # Reorder to match training
                                        predictions = model.predict(X_pred)
                                        
                                        # Extrapolate for horizon
                                        last_value = df[target_col].dropna().iloc[-1] if len(df) > 0 else predictions[0]
                                        trend = (predictions[0] - last_value) if len(predictions) > 0 else 0
                                        forecast = [predictions[0] + trend * (i+1) for i in range(horizon)]
                                    else:
                                        raise ValueError("No matching features found")
                                else:
                                    predictions = model.predict(last_features)
                                    last_value = df[target_col].dropna().iloc[-1] if len(df) > 0 else predictions[0]
                                    trend = (predictions[0] - last_value) if len(predictions) > 0 else 0
                                    forecast = [predictions[0] + trend * (i+1) for i in range(horizon)]
                            else:
                                raise ValueError("Could not create features")
                            
                            std = np.std(df[target_col].dropna().tail(30).values) if len(df) > 30 else df[target_col].std()
                            forecast_result = {
                                'forecast': np.array(forecast),
                                'lower': np.array(forecast) - 1.96 * std,
                                'upper': np.array(forecast) + 1.96 * std,
                            }
                        except Exception as feat_error:
                            # Fallback to simple extrapolation if feature engineering fails
                            st.warning(f"Feature engineering failed, using simple extrapolation: {str(feat_error)}")
                            last_values = df[target_col].dropna().tail(30).values if len(df) > 30 else df[target_col].dropna().values
                            if len(last_values) > 1:
                                trend = np.mean(np.diff(last_values))
                                forecast = [last_values[-1] + trend * (i+1) for i in range(horizon)]
                            else:
                                forecast = [last_values[-1]] * horizon if len(last_values) > 0 else [0] * horizon
                            
                            std = np.std(last_values) if len(last_values) > 1 else abs(last_values[-1] * 0.1) if len(last_values) > 0 else 1.0
                            forecast_result = {
                                'forecast': np.array(forecast),
                                'lower': np.array(forecast) - 1.96 * std,
                                'upper': np.array(forecast) + 1.96 * std,
                            }
                    else:
                        # No feature engineering metadata - use simple extrapolation
                        last_values = df[target_col].dropna().tail(30).values if len(df) > 30 else df[target_col].dropna().values
                        if len(last_values) > 1:
                            trend = np.mean(np.diff(last_values))
                            forecast = [last_values[-1] + trend * (i+1) for i in range(horizon)]
                        else:
                            forecast = [last_values[-1]] * horizon if len(last_values) > 0 else [0] * horizon
                        
                        std = np.std(last_values) if len(last_values) > 1 else abs(last_values[-1] * 0.1) if len(last_values) > 0 else 1.0
                        forecast_result = {
                            'forecast': np.array(forecast),
                            'lower': np.array(forecast) - 1.96 * std,
                            'upper': np.array(forecast) + 1.96 * std,
                        }
                
                st.session_state.forecast_result = forecast_result
                st.session_state.forecast_horizon = horizon
                st.session_state.forecast_target = target_col
                st.success("✅ Forecast generated!")
            except Exception as e:
                st.error(f"Forecast generation failed: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    # Display forecast
    if 'forecast_result' in st.session_state:
        st.markdown("### 📈 Forecast Visualization")
        
        forecast_result = st.session_state.forecast_result
        horizon = st.session_state.forecast_horizon
        target_col = st.session_state.forecast_target
        
        # Get historical data
        hist_data = df[target_col].dropna().tail(100).values
        hist_dates = pd.date_range(end=pd.Timestamp.now(), periods=len(hist_data), freq='D')
        forecast_dates = pd.date_range(start=hist_dates[-1] + pd.Timedelta(days=1), periods=horizon, freq='D')
        
        # Create plot
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=hist_dates,
            y=hist_data,
            mode='lines',
            name='Historical',
            line=dict(color='#1f77b4', width=2),
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_result['forecast'],
            mode='lines',
            name='Forecast',
            line=dict(color='#2ca07c', width=2, dash='dash'),
        ))
        
        # Confidence intervals
        fig.add_trace(go.Scatter(
            x=forecast_dates.tolist() + forecast_dates.tolist()[::-1],
            y=list(forecast_result['upper']) + list(forecast_result['lower'])[::-1],
            fill='tonexty',
            fillcolor='rgba(44, 160, 124, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name=f'{int(confidence*100)}% Confidence',
            showlegend=True,
        ))
        
        fig.update_layout(
            title=f"{target_col} Forecast ({horizon} days)",
            xaxis_title="Date",
            yaxis_title=target_col,
            height=500,
            hovermode='x unified',
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Scenario analysis
        st.markdown("### 🔮 Scenario Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            flow_change = st.slider("Flow Change (%)", -50, 50, 0, 5, key="scenario_flow_slider")
        with col2:
            temp_change = st.slider("Temperature Change (%)", -20, 20, 0, 5, key="scenario_temp_slider")
        with col3:
            aeration_change = st.slider("Aeration Change (%)", -30, 30, 0, 5, key="scenario_aeration_slider")
        
        if st.button("🔄 Update Forecast with Scenarios"):
            # Adjust forecast based on scenarios
            adjusted_forecast = forecast_result['forecast'] * (1 + flow_change/100) * (1 + temp_change/100) * (1 + aeration_change/100)
            
            st.info(f"Scenario-adjusted forecast: Mean = {np.mean(adjusted_forecast):.2f} "
                   f"(vs baseline {np.mean(forecast_result['forecast']):.2f})")



