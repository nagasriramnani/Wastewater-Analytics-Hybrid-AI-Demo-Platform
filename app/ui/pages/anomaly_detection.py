"""Anomaly Detection Center page."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from app.ui.components.library import ComponentLibrary
from app.ui.state.manager import StateManager
from app.ai.utils.metrics import calculate_anomaly_scores


def render():
    """Render the Anomaly Detection Center page."""
    ComponentLibrary.section_header("🚨 Anomaly Detection Center")
    
    df = StateManager.get_dataset()
    if df is None:
        ComponentLibrary.empty_state(
            "No dataset loaded. Please upload a dataset from the AI Training Studio.",
            icon="📊",
        )
        return
    
    # Configuration
    st.markdown("### ⚙️ Detection Configuration")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    target_col = st.selectbox("Target Variable", numeric_cols[:10])
    
    method = st.selectbox("Detection Method", ["zscore", "iqr"])
    threshold = st.slider("Anomaly Threshold", 1.0, 5.0, 3.0, 0.5, key="anomaly_threshold_slider")
    
    # Detect anomalies
    if st.button("🔍 Detect Anomalies", type="primary"):
        with st.spinner("Analyzing data for anomalies..."):
            values = df[target_col].dropna().values
            
            scores = calculate_anomaly_scores(values, method=method, threshold=threshold)
            anomalies = scores > threshold
            
            # Store results
            anomaly_indices = np.where(anomalies)[0]
            anomaly_values = values[anomaly_indices]
            anomaly_scores = scores[anomaly_indices]
            
            st.session_state.anomaly_results = {
                'indices': anomaly_indices,
                'values': anomaly_values,
                'scores': anomaly_scores,
                'all_scores': scores,
                'target_col': target_col,
            }
            
            st.success(f"✅ Detected {len(anomaly_indices)} anomalies ({len(anomaly_indices)/len(values)*100:.1f}%)")
    
    # Display results
    if 'anomaly_results' in st.session_state:
        results = st.session_state.anomaly_results
        
        # Validate results structure
        if results is None or not isinstance(results, dict):
            st.error("Invalid anomaly results. Please run detection again.")
            return
        
        if 'target_col' not in results or results['target_col'] is None:
            st.error("Target column not found in results. Please run detection again.")
            return
        
        target_col_result = results['target_col']
        if target_col_result not in df.columns:
            st.error(f"Target column '{target_col_result}' not found in dataset. Please run detection again.")
            return
        
        st.markdown("### 📊 Anomaly Timeline")
        
        # Create timeline plot
        values = df[target_col_result].dropna().values
        dates = pd.date_range(end=pd.Timestamp.now(), periods=len(values), freq='D') if len(values) <= 1000 else None
        
        if dates is None:
            x_vals = np.arange(len(values))
        else:
            x_vals = dates
        
        fig = go.Figure()
        
        # Normal values
        normal_mask = ~np.isin(np.arange(len(values)), results['indices'])
        fig.add_trace(go.Scatter(
            x=x_vals[normal_mask],
            y=values[normal_mask],
            mode='markers',
            name='Normal',
            marker=dict(color='#1f77b4', size=4),
        ))
        
        # Anomalies
        fig.add_trace(go.Scatter(
            x=x_vals[results['indices']],
            y=results['values'],
            mode='markers',
            name='Anomaly',
            marker=dict(color='#ff7f0e', size=8, symbol='triangle-up'),
            text=[f"Score: {s:.2f}" for s in results['scores']],
            hovertemplate='Value: %{y}<br>Score: %{text}<extra></extra>',
        ))
        
        fig.update_layout(
            title=f"Anomaly Detection: {target_col_result}",
            xaxis_title="Time",
            yaxis_title=target_col_result,
            height=500,
            hovermode='closest',
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Anomaly table
        st.markdown("### 📋 Anomaly Details")
        
        if 'indices' in results and 'values' in results and 'scores' in results:
            anomaly_df = pd.DataFrame({
                'Index': results['indices'],
                'Value': results['values'],
                'Anomaly Score': results['scores'],
                'Severity': pd.cut(results['scores'], bins=[0, threshold, threshold*1.5, 100], labels=['Low', 'Medium', 'High']),
            })
        else:
            st.error("Anomaly results incomplete. Please run detection again.")
            return
        
        st.dataframe(anomaly_df, use_container_width=True)
        
        # Root cause analysis (simplified)
        st.markdown("### 🔍 Root Cause Analysis")
        
        if 'indices' in results and len(results['indices']) > 0:
            # Show feature deviations for anomalies
            anomaly_idx = results['indices'][0]
            if anomaly_idx < len(df):
                st.info(f"Analyzing anomaly at index {anomaly_idx}")
                
                # Simple feature comparison
                if len(numeric_cols) > 1:
                    comparison_df = pd.DataFrame({
                        'Feature': numeric_cols[:5],
                        'Anomaly Value': [df[col].iloc[anomaly_idx] if anomaly_idx < len(df) else np.nan for col in numeric_cols[:5]],
                        'Normal Range (Mean ± 2σ)': [
                            f"{df[col].mean():.2f} ± {2*df[col].std():.2f}"
                            for col in numeric_cols[:5]
                        ],
                    })
                    st.dataframe(comparison_df, use_container_width=True)
        
        # Export
        if st.button("📥 Export Anomaly Report"):
            st.info("Export functionality will generate a PDF report with anomaly details.")



