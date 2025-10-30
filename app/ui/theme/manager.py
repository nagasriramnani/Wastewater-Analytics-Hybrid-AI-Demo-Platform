"""Theme manager for Aqua Analytics design system."""

from pathlib import Path
from typing import Dict, Any
import streamlit as st
import yaml


# Aqua Analytics color palette
AQUA_COLORS = {
    "primary": "#1f77b4",
    "teal": "#2ca07c",
    "alert": "#ff7f0e",
    "bg": "#f8f9fa",
    "text": "#333333",
    "text_light": "#666666",
}


class ThemeManager:
    """Manages theme injection and design system constants."""
    
    def __init__(self):
        """Initialize theme manager with config."""
        self.config = self._load_config()
        self.colors = self.config.get("theme", {}).get("colors", AQUA_COLORS)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load settings from config file."""
        try:
            config_path = Path("config/settings.yaml")
            if config_path.exists():
                with open(config_path, "r") as f:
                    return yaml.safe_load(f) or {}
        except Exception:
            pass
        return {}
    
    def inject_theme(self) -> None:
        """Inject CSS theme into Streamlit app."""
        css = f"""
        <style>
        :root {{
          --color-primary: {self.colors.get('primary', AQUA_COLORS['primary'])};
          --color-teal: {self.colors.get('teal', AQUA_COLORS['teal'])};
          --color-alert: {self.colors.get('alert', AQUA_COLORS['alert'])};
          --bg: {self.colors.get('bg', AQUA_COLORS['bg'])};
          --text: {self.colors.get('text', AQUA_COLORS['text'])};
          --text-light: {self.colors.get('text_light', AQUA_COLORS['text_light'])};
        }}
        
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Fira+Mono:wght@400&display=swap');
        
        /* Base styling */
        .main {{
          background-color: var(--bg);
          font-family: 'Inter', sans-serif;
        }}
        
        /* Cards */
        .aqua-card {{
          background: white;
          border-radius: 16px;
          padding: 20px;
          box-shadow: 0 4px 14px rgba(0,0,0,0.06);
          margin-bottom: 16px;
        }}
        
        /* KPI Cards */
        .kpi-card {{
          background: linear-gradient(135deg, var(--color-primary) 0%, #2a5f8f 100%);
          border-radius: 12px;
          padding: 24px;
          color: white;
          text-align: center;
          box-shadow: 0 6px 20px rgba(31, 119, 180, 0.3);
        }}
        
        .kpi-title {{
          font-size: 14px;
          opacity: 0.9;
          margin-bottom: 8px;
          font-weight: 500;
        }}
        
        .kpi-value {{
          font-size: 32px;
          font-weight: 700;
          margin: 8px 0;
        }}
        
        .kpi-delta {{
          font-size: 12px;
          padding: 4px 8px;
          border-radius: 4px;
          display: inline-block;
          margin-top: 8px;
        }}
        
        .kpi-delta.up {{
          background: rgba(44, 160, 124, 0.2);
          color: var(--color-teal);
        }}
        
        .kpi-delta.down {{
          background: rgba(255, 127, 14, 0.2);
          color: var(--color-alert);
        }}
        
        /* Alert Banner */
        .alert-banner {{
          padding: 12px 16px;
          border-radius: 8px;
          margin-bottom: 16px;
          border-left: 4px solid;
        }}
        
        .alert-info {{
          background: #e3f2fd;
          border-color: var(--color-primary);
          color: #1976d2;
        }}
        
        .alert-warning {{
          background: #fff3e0;
          border-color: var(--color-alert);
          color: #f57c00;
        }}
        
        .alert-success {{
          background: #e8f5e9;
          border-color: var(--color-teal);
          color: #388e3c;
        }}
        
        /* Empty State */
        .empty-state {{
          text-align: center;
          padding: 60px 20px;
          color: var(--text-light);
        }}
        
        .empty-state-icon {{
          font-size: 64px;
          margin-bottom: 16px;
        }}
        
        /* Section Headers */
        .section-header {{
          font-size: 24px;
          font-weight: 700;
          color: var(--text);
          margin: 24px 0 16px 0;
          padding-bottom: 8px;
          border-bottom: 2px solid var(--color-primary);
        }}
        
        /* Loading Spinner */
        .spinner-overlay {{
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 200px;
        }}
        
        /* Focus states for accessibility */
        button:focus-visible,
        input:focus-visible,
        select:focus-visible {{
          outline: 2px solid var(--color-primary);
          outline-offset: 2px;
        }}
        
        /* Code blocks */
        code {{
          font-family: 'Fira Mono', monospace;
          background: #f5f5f5;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 0.9em;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    def get_color(self, name: str) -> str:
        """Get a theme color by name."""
        return self.colors.get(name, AQUA_COLORS.get(name, "#000000"))


def inject_theme():
    """Convenience function to inject theme."""
    manager = ThemeManager()
    manager.inject_theme()
    return manager



