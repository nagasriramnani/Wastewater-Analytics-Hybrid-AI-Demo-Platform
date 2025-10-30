"""Explainability Lab page."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
from app.ui.components.library import ComponentLibrary
from app.ui.state.manager import StateManager


def render():
    """Render the Explainability Lab page."""
    ComponentLibrary.section_header("🔍 Explainability Lab")
    
    df = StateManager.get_dataset()
    if df is None:
        ComponentLibrary.empty_state(
            "No dataset loaded. Please upload a dataset from the AI Training Studio.",
            icon="📊",
        )
        return
    
    models = StateManager.get_all_models()
    if not models:
        ComponentLibrary.alert_banner(
            "No trained models found. Please train a model in the AI Training Studio first.",
            alert_type="warning",
        )
        return
    
    # Model selection
    model_options = list(models.keys()) + ["best"]
    selected_model_key = st.selectbox("Select Model", model_options)
    model = models.get(selected_model_key) if selected_model_key != "best" else StateManager.get_model("best")
    
    if model is None or not hasattr(model, 'predict'):
        st.error("Selected model is not suitable for explainability analysis.")
        return
    
    st.markdown("### 📊 Global Feature Importance")
    
    # Get feature importance
    if hasattr(model, 'get_feature_importance'):
        importances = model.get_feature_importance()
    elif hasattr(model, 'feature_importances_'):
        importances = dict(zip(model.feature_names_in_ if hasattr(model, 'feature_names_in_') else range(len(model.feature_importances_)), model.feature_importances_))
    else:
        importances = {}
    
    if importances:
        # Sort by importance
        sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:10]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[v for _, v in sorted_features],
            y=[k for k, _ in sorted_features],
            orientation='h',
            marker_color='#1f77b4',
        ))
        
        fig.update_layout(
            title="Top 10 Feature Importances",
            xaxis_title="Importance",
            height=400,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # SHAP explanations (if LightGBM)
    if SHAP_AVAILABLE and (selected_model_key == "lightgbm" or "lightgbm" in str(type(model)).lower()):
        st.markdown("### 🎯 SHAP Explanations")
        
        try:
            # Prepare data for SHAP
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:10]
            sample_data = df[numeric_cols].dropna().head(100)
            
            if len(sample_data) > 0 and hasattr(model, 'predict'):
                with st.spinner("Computing SHAP values..."):
                    explainer = shap.TreeExplainer(model.model if hasattr(model, 'model') else model)
                    shap_values = explainer.shap_values(sample_data)
                    
                    # Summary plot
                    st.markdown("#### Summary Plot")
                    fig = shap.summary_plot(shap_values, sample_data, show=False)
                    st.pyplot(fig)
                    
                    # Waterfall plot for single prediction
                    st.markdown("#### Local Explanation (Waterfall)")
                    instance_idx = st.slider("Select instance", 0, min(50, len(sample_data)-1), 0, key="instance_select_slider")
                    
                    if isinstance(shap_values, list):
                        shap_values_single = shap_values[instance_idx]
                    else:
                        shap_values_single = shap_values[instance_idx]
                    
                    st.info(f"Instance {instance_idx}: Prediction = {model.predict(sample_data.iloc[[instance_idx]])[0]:.2f}")
        except Exception as e:
            st.warning(f"SHAP analysis unavailable: {str(e)}")
    
    # Partial Dependence (simplified)
    st.markdown("### 📈 Partial Dependence Analysis")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if len(numeric_cols) > 0:
        feature_for_pdp = st.selectbox("Feature for PDP", numeric_cols[:5])
        
        if st.button("📊 Generate PDP"):
            with st.spinner("Computing partial dependence..."):
                # Simple PDP approximation
                feature_values = df[feature_for_pdp].dropna().values
                unique_vals = np.linspace(feature_values.min(), feature_values.max(), 20)
                
                # For demo: approximate PDP
                pdp_values = []
                for val in unique_vals:
                    temp_df = df.copy()
                    temp_df[feature_for_pdp] = val
                    if hasattr(model, 'predict'):
                        predictions = model.predict(temp_df[numeric_cols[:10]].fillna(0).head(10))
                        pdp_values.append(np.mean(predictions))
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=unique_vals,
                    y=pdp_values,
                    mode='lines+markers',
                    marker_color='#2ca07c',
                ))
                
                fig.update_layout(
                    title=f"Partial Dependence: {feature_for_pdp}",
                    xaxis_title=feature_for_pdp,
                    yaxis_title="Average Prediction",
                    height=400,
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # What-if analysis
    st.markdown("### 🔮 What-If Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        feature1 = st.selectbox("Feature 1", numeric_cols[:5] if len(numeric_cols) > 0 else [])
        value1 = st.slider(f"{feature1} value", 
                          float(df[feature1].min()) if len(numeric_cols) > 0 else 0.0,
                          float(df[feature1].max()) if len(numeric_cols) > 0 else 100.0,
                          float(df[feature1].mean()) if len(numeric_cols) > 0 else 50.0,
                          key="whatif_feature1_slider")
    
    with col2:
        feature2 = st.selectbox("Feature 2", numeric_cols[:5] if len(numeric_cols) > 1 else [])
        if len(numeric_cols) > 1:
            value2 = st.slider(f"{feature2} value",
                              float(df[feature2].min()),
                              float(df[feature2].max()),
                              float(df[feature2].mean()),
                              key="whatif_feature2_slider")
        else:
            value2 = 0.0
    
    if st.button("🔍 Predict with What-If Values"):
        try:
            # Create input with what-if values
            instance = df[numeric_cols[:10]].iloc[0].copy() if len(df) > 0 else pd.Series([0]*min(10, len(numeric_cols)))
            if feature1 in instance.index:
                instance[feature1] = value1
            if feature2 in instance.index and len(numeric_cols) > 1:
                instance[feature2] = value2
            
            prediction = model.predict(pd.DataFrame([instance]).fillna(0))
            st.success(f"Predicted value: **{prediction[0]:.2f}**")
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")

