"""Main Streamlit application entrypoint."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from streamlit_option_menu import option_menu
from app.ui.theme.manager import inject_theme
from app.ui.state.manager import StateManager

# Page configuration
st.set_page_config(
    page_title="Wastewater Analytics & Hybrid-AI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject theme
theme_manager = inject_theme()

# Initialize session state
StateManager.init_session_state()

# Header
st.markdown(
    """
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: var(--color-primary); margin: 0;'>💧 Wastewater Analytics & Hybrid-AI</h1>
        <p style='color: var(--text-light); margin: 5px 0;'>Aqua Analytics Platform v2.0</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
with st.sidebar:
    st.markdown(
        "<div style='text-align: center; padding: 10px 0;'>"
        "<h2 style='color: var(--color-primary);'>Aqua Analytics</h2>"
        "</div>",
        unsafe_allow_html=True,
    )
    
    # Use native Streamlit selectbox as workaround for pyarrow requirement
    try:
        selection = option_menu(
            menu_title=None,
            options=[
                "🏠 Dashboard",
                "🤖 AI Training Studio",
                "📊 Forecasting Hub",
                "🚨 Anomaly Detection",
                "🔍 Explainability Lab",
                "📈 Benchmarking Suite",
                "🧾 Reporting",
            ],
            icons=[
                "house",
                "cpu",
                "graph-up",
                "exclamation-triangle",
                "search",
                "bar-chart",
                "file-earmark-text",
            ],
            menu_icon="water",
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "white"},
                "icon": {"color": "#1f77b4", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#e8f4f8",
                },
                "nav-link-selected": {"background-color": "#1f77b4"},
            },
        )
    except Exception:
        # Fallback to native Streamlit selectbox if option_menu fails
        selection = st.selectbox(
            "📋 Navigation",
            options=[
                "🏠 Dashboard",
                "🤖 AI Training Studio",
                "📊 Forecasting Hub",
                "🚨 Anomaly Detection",
                "🔍 Explainability Lab",
                "📈 Benchmarking Suite",
                "🧾 Reporting",
            ],
            key="page_selector",
        )

# Error boundary wrapper
try:
    # Route to appropriate page
    if selection == "🏠 Dashboard":
        from app.ui.pages.dashboard import render
        render()
    elif selection == "🤖 AI Training Studio":
        from app.ui.pages.training_studio import render
        render()
    elif selection == "📊 Forecasting Hub":
        from app.ui.pages.forecasting import render
        render()
    elif selection == "🚨 Anomaly Detection":
        from app.ui.pages.anomaly_detection import render
        render()
    elif selection == "🔍 Explainability Lab":
        from app.ui.pages.explainability import render
        render()
    elif selection == "📈 Benchmarking Suite":
        from app.ui.pages.benchmarking import render
        render()
    elif selection == "🧾 Reporting":
        from app.ui.pages.reporting import render
        render()
    else:
        st.error("Page not found")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.exception(e)


