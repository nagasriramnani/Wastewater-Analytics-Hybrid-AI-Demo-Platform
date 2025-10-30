"""Smoke tests for UI components."""

import pytest
from app.ui.components.library import ComponentLibrary
from app.ui.state.manager import StateManager


def test_component_library_kpi_card():
    """Test KPI card component."""
    # Should not raise
    try:
        ComponentLibrary.kpi_card("Test", "100", delta="+5%", delta_type="up")
        assert True
    except Exception:
        pytest.fail("KPI card failed")


def test_component_library_alert_banner():
    """Test alert banner component."""
    try:
        ComponentLibrary.alert_banner("Test message", alert_type="info")
        assert True
    except Exception:
        pytest.fail("Alert banner failed")


def test_state_manager_init():
    """Test state manager initialization."""
    StateManager.init_session_state()
    assert True  # If no exception raised


def test_state_manager_dataset():
    """Test dataset storage."""
    import pandas as pd
    
    StateManager.init_session_state()
    df = pd.DataFrame({'a': [1, 2, 3]})
    
    StateManager.set_dataset(df)
    retrieved = StateManager.get_dataset()
    
    assert retrieved is not None
    assert len(retrieved) == 3



