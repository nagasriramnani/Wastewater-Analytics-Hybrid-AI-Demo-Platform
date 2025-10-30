"""Component library for Aqua Analytics UI."""

from typing import Optional, Dict, Any
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ComponentLibrary:
    """Library of reusable UI components."""
    
    @staticmethod
    def kpi_card(
        title: str,
        value: str,
        delta: Optional[str] = None,
        delta_type: Optional[str] = None,
        icon: Optional[str] = None,
    ) -> None:
        """Render a KPI card with optional delta indicator.
        
        Args:
            title: KPI title
            value: Main value to display
            delta: Change indicator (e.g., "+5.2%", "-3.1%")
            delta_type: "up" or "down" for styling
            icon: Optional emoji or icon character
        """
        icon_text = f"{icon} " if icon else ""
        delta_html = ""
        if delta:
            delta_class = f"up" if delta_type == "up" else "down"
            delta_html = f'<div class="kpi-delta {delta_class}">{delta}</div>'
        
        html = f"""
        <div class="kpi-card">
            <div class="kpi-title">{icon_text}{title}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def section_header(title: str, icon: Optional[str] = None) -> None:
        """Render a section header.
        
        Args:
            title: Section title
            icon: Optional emoji or icon
        """
        icon_text = f"{icon} " if icon else ""
        st.markdown(f'<div class="section-header">{icon_text}{title}</div>', unsafe_allow_html=True)
    
    @staticmethod
    def alert_banner(
        message: str,
        alert_type: str = "info",
        icon: Optional[str] = None,
    ) -> None:
        """Render an alert banner.
        
        Args:
            message: Alert message
            alert_type: "info", "warning", or "success"
            icon: Optional emoji or icon
        """
        icon_text = f"{icon} " if icon else ""
        st.markdown(
            f'<div class="alert-banner alert-{alert_type}">{icon_text}{message}</div>',
            unsafe_allow_html=True,
        )
    
    @staticmethod
    def empty_state(
        message: str,
        icon: str = "📊",
        action_button: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Render an empty state.
        
        Args:
            message: Message to display
            icon: Icon character/emoji
            action_button: Optional dict with "label" and "on_click" for button
        """
        st.markdown(
            f"""
            <div class="empty-state">
                <div class="empty-state-icon">{icon}</div>
                <p>{message}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if action_button:
            st.button(action_button.get("label", "Get Started"), key="empty_state_action")
    
    @staticmethod
    def trend_card(
        title: str,
        data,
        x_col: str,
        y_col: str,
        trend_type: str = "line",
        height: int = 300,
    ) -> None:
        """Render a trend visualization card.
        
        Args:
            title: Chart title
            data: DataFrame or dict with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            trend_type: "line", "bar", or "area"
            height: Chart height in pixels
        """
        st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
        
        import pandas as pd
        
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = data
        
        fig = go.Figure()
        
        if trend_type == "line":
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode='lines+markers',
                name=y_col,
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4),
            ))
        elif trend_type == "bar":
            fig.add_trace(go.Bar(
                x=df[x_col],
                y=df[y_col],
                name=y_col,
                marker_color='#1f77b4',
            ))
        elif trend_type == "area":
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode='lines',
                fill='tonexty',
                name=y_col,
                line=dict(color='#1f77b4'),
            ))
        
        fig.update_layout(
            height=height,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def data_quality_card(
        stats: Dict[str, Any],
    ) -> None:
        """Render a data quality summary card.
        
        Args:
            stats: Dict with keys like 'missing_pct', 'duplicates', 'rows', 'columns', etc.
        """
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ComponentLibrary.kpi_card(
                "Total Rows",
                f"{stats.get('rows', 0):,}",
                icon="📊",
            )
        with col2:
            ComponentLibrary.kpi_card(
                "Columns",
                f"{stats.get('columns', 0)}",
                icon="📋",
            )
        with col3:
            missing_pct = stats.get('missing_pct', 0)
            ComponentLibrary.kpi_card(
                "Missing Data",
                f"{missing_pct:.1f}%",
                delta_type="up" if missing_pct < 5 else "down",
                icon="⚠️",
            )
        with col4:
            ComponentLibrary.kpi_card(
                "Duplicates",
                f"{stats.get('duplicates', 0):,}",
                delta_type="up" if stats.get('duplicates', 0) == 0 else "down",
                icon="🔍",
            )
        
        if stats.get('date_range'):
            st.info(f"📅 Date Range: {stats['date_range'][0]} to {stats['date_range'][1]}")


# Convenience instances
KPICard = ComponentLibrary.kpi_card
Section = ComponentLibrary.section_header
AlertBanner = ComponentLibrary.alert_banner
EmptyState = ComponentLibrary.empty_state
TrendCard = ComponentLibrary.trend_card
DataQualityCard = ComponentLibrary.data_quality_card



