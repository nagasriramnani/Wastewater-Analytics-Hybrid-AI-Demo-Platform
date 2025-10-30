"""Benchmarking Suite page."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from app.ui.components.library import ComponentLibrary
from app.ui.state.manager import StateManager


def render():
    """Render the Benchmarking Suite page."""
    ComponentLibrary.section_header("📈 Benchmarking Suite")
    
    df = StateManager.get_dataset()
    if df is None:
        ComponentLibrary.empty_state(
            "No dataset loaded. Please upload a dataset from the AI Training Studio.",
            icon="📊",
        )
        return
    
    # Site selection
    site_cols = [c for c in df.columns if any(x in c.lower() for x in ['site', 'station', 'location', 'plant'])]
    
    if site_cols:
        site_col = site_cols[0]
        sites = df[site_col].unique().tolist()
        selected_sites = st.multiselect("Select Sites to Compare", sites, default=sites[:3] if len(sites) >= 3 else sites)
        
        if not selected_sites:
            st.warning("Please select at least one site.")
            return
    else:
        selected_sites = ["All"]
        site_col = None
    
    # Metrics selection
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    metrics = st.multiselect(
        "Select Metrics for Benchmarking",
        numeric_cols[:10],
        default=numeric_cols[:4] if len(numeric_cols) >= 4 else numeric_cols,
    )
    
    if not metrics:
        st.warning("Please select at least one metric.")
        return
    
    # Compute benchmark metrics
    if st.button("📊 Generate Benchmark", type="primary"):
        with st.spinner("Computing benchmarks..."):
            results = {}
            
            for site in selected_sites:
                if site_col:
                    site_df = df[df[site_col] == site]
                else:
                    site_df = df
                
                site_metrics = {}
                for metric in metrics:
                    values = site_df[metric].dropna()
                    if len(values) > 0:
                        site_metrics[metric] = {
                            'mean': float(values.mean()),
                            'std': float(values.std()),
                            'min': float(values.min()),
                            'max': float(values.max()),
                            'median': float(values.median()),
                        }
                
                results[site] = site_metrics
            
            st.session_state.benchmark_results = results
            st.success("✅ Benchmark computed!")
    
    # Display results
    if 'benchmark_results' in st.session_state:
        results = st.session_state.benchmark_results
        
        st.markdown("### 📊 Performance Comparison Table")
        
        # Create comparison DataFrame
        comparison_data = []
        for site, site_metrics in results.items():
            for metric, stats in site_metrics.items():
                comparison_data.append({
                    'Site': site,
                    'Metric': metric,
                    'Mean': stats['mean'],
                    'Std': stats['std'],
                    'Min': stats['min'],
                    'Max': stats['max'],
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Radar chart
        st.markdown("### 🎯 Radar Chart Comparison")
        
        if len(metrics) > 0 and len(selected_sites) > 0:
            # Normalize metrics for radar chart
            fig = go.Figure()
            
            for site in selected_sites:
                if site in results:
                    values = []
                    labels = []
                    
                    for metric in metrics[:6]:  # Limit to 6 metrics for readability
                        if metric in results[site]:
                            # Normalize to 0-100 scale
                            normalized = (results[site][metric]['mean'] / 
                                        max([results[s][metric]['mean'] for s in selected_sites if metric in results.get(s, {})] + [1])) * 100
                            values.append(normalized)
                            labels.append(metric[:20])  # Truncate long names
                    
                    if values:
                        # Close the radar chart
                        values.append(values[0])
                        labels.append(labels[0])
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=labels,
                            fill='toself',
                            name=site,
                        ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100]),
                ),
                showlegend=True,
                height=500,
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Period-over-period analysis
        st.markdown("### 📅 Period-over-Period Analysis")
        
        date_cols = [c for c in df.columns if 'date' in c.lower()]
        if date_cols:
            date_col = date_cols[0]
            
            period = st.selectbox("Comparison Period", ["Weekly", "Monthly", "Quarterly"])
            
            if st.button("📊 Compare Periods"):
                # Simple period comparison
                df_period = df.copy()
                if not pd.api.types.is_datetime64_any_dtype(df_period[date_col]):
                    df_period[date_col] = pd.to_datetime(df_period[date_col], errors='coerce')
                
                if period == "Weekly":
                    df_period['period'] = df_period[date_col].dt.isocalendar().week
                elif period == "Monthly":
                    df_period['period'] = df_period[date_col].dt.month
                else:
                    df_period['period'] = df_period[date_col].dt.quarter
                
                # Aggregate by period
                period_agg = df_period.groupby('period')[metrics[0]].mean()
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=period_agg.index,
                    y=period_agg.values,
                    marker_color='#1f77b4',
                ))
                
                fig.update_layout(
                    title=f"{period} Trend: {metrics[0]}",
                    xaxis_title=period,
                    yaxis_title=metrics[0],
                    height=400,
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Export
        if st.button("📥 Export Benchmark Report"):
            st.info("Export functionality will generate charts and tables as PNG/PDF.")



