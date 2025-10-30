"""Dashboard page."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.ui.components.library import ComponentLibrary
from app.ui.state.manager import StateManager


def render():
    """Render the dashboard page."""
    ComponentLibrary.section_header("📊 Overview Dashboard", icon="🏠")
    
    # Get current dataset
    df = StateManager.get_dataset()
    
    if df is None:
        ComponentLibrary.empty_state(
            "No dataset loaded. Please upload or select a dataset from the AI Training Studio.",
            icon="📊",
            action_button={"label": "Go to Training Studio", "on_click": None},
        )
        return
    
    # Display KPIs
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    with col1:
        if 'bod' in df.columns.str.lower().str.lower().tolist():
            bod_col = [c for c in df.columns if 'bod' in c.lower()][0]
            latest_value = df[bod_col].dropna().iloc[-1] if len(df) > 0 else 0
            ComponentLibrary.kpi_card("Effluent BOD", f"{latest_value:.2f} mg/L", icon="💧")
        else:
            ComponentLibrary.kpi_card("Data Points", f"{len(df):,}", icon="📊")
    
    with col2:
        if 'cod' in df.columns.str.lower().tolist():
            cod_col = [c for c in df.columns if 'cod' in c.lower()][0]
            latest_value = df[cod_col].dropna().iloc[-1] if len(df) > 0 else 0
            ComponentLibrary.kpi_card("Effluent COD", f"{latest_value:.2f} mg/L", icon="🔬")
        else:
            ComponentLibrary.kpi_card("Columns", f"{len(df.columns)}", icon="📋")
    
    with col3:
        if len(numeric_cols) > 0:
            avg_value = df[numeric_cols[0]].mean()
            ComponentLibrary.kpi_card("Average Value", f"{avg_value:.2f}", icon="📈")
        else:
            ComponentLibrary.kpi_card("Sites", f"{df['site_id'].nunique() if 'site_id' in df.columns else 'N/A'}", icon="🏭")
    
    with col4:
        date_cols = [c for c in df.columns if 'date' in c.lower()]
        if date_cols:
            date_col = date_cols[0]
            if pd.api.types.is_datetime64_any_dtype(df[date_col]):
                date_range = (df[date_col].max() - df[date_col].min()).days
                ComponentLibrary.kpi_card("Date Range", f"{date_range} days", icon="📅")
            else:
                ComponentLibrary.kpi_card("Records", f"{len(df):,}", icon="📝")
        else:
            ComponentLibrary.kpi_card("Records", f"{len(df):,}", icon="📝")
    
    # Trend visualization
    st.markdown("### Trend Analysis")
    
    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select metric", numeric_cols[:5], key="dashboard_metric")
        
        # Get date column for x-axis
        date_cols = [c for c in df.columns if 'date' in c.lower()]
        x_col = date_cols[0] if date_cols else df.index
        
        if date_cols:
            df_plot = df[[date_cols[0], selected_col]].dropna().copy()
            x_vals = df_plot[date_cols[0]]
        else:
            df_plot = df[[selected_col]].dropna().copy()
            x_vals = df_plot.index
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=df_plot[selected_col],
            mode='lines+markers',
            name=selected_col,
            line=dict(color='#1f77b4', width=2),
        ))
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis_title=date_cols[0] if date_cols else "Index",
            yaxis_title=selected_col,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No numeric columns found for trend visualization.")
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Train Models", use_container_width=True):
            st.session_state.page_redirect = "training"
            st.rerun()
    
    with col2:
        if st.button("📊 Generate Forecast", use_container_width=True):
            st.session_state.page_redirect = "forecasting"
            st.rerun()
    
    with col3:
        if st.button("🧾 Create Report", use_container_width=True):
            st.session_state.page_redirect = "reporting"
            st.rerun()



