"""State manager for Streamlit session state."""

from typing import Optional, Any, Dict
import streamlit as st
import pandas as pd
from pathlib import Path


class StateManager:
    """Manages Streamlit session state across pages."""
    
    @staticmethod
    def init_session_state() -> None:
        """Initialize session state variables."""
        defaults = {
            "current_dataset": None,
            "dataset_path": None,
            "trained_models": {},
            "selected_model": None,
            "forecast_results": None,
            "anomaly_results": None,
            "selected_site": None,
            "explanation_data": None,
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def set_dataset(df: pd.DataFrame, path: Optional[str] = None) -> None:
        """Store current dataset in session state.
        
        Args:
            df: DataFrame to store
            path: Optional file path
        """
        st.session_state.current_dataset = df
        st.session_state.dataset_path = path
    
    @staticmethod
    def get_dataset() -> Optional[pd.DataFrame]:
        """Get current dataset from session state."""
        return st.session_state.get("current_dataset")
    
    @staticmethod
    def set_model(name: str, model: Any) -> None:
        """Store a trained model.
        
        Args:
            name: Model name/identifier
            model: Model object to store
        """
        if "trained_models" not in st.session_state:
            st.session_state.trained_models = {}
        st.session_state.trained_models[name] = model
    
    @staticmethod
    def get_model(name: str) -> Optional[Any]:
        """Get a stored model."""
        return st.session_state.get("trained_models", {}).get(name)
    
    @staticmethod
    def get_all_models() -> Dict[str, Any]:
        """Get all stored models."""
        return st.session_state.get("trained_models", {})
    
    @staticmethod
    def clear_state() -> None:
        """Clear all session state."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        StateManager.init_session_state()



