"""Tests for ML models."""

import pytest
import pandas as pd
import numpy as np
from app.ai.models.lightgbm_model import LightGBMRegressor
from app.ai.models.random_forest_model import RandomForestRegressor
from app.ai.models.prophet_model import ProphetForecaster


@pytest.fixture
def sample_training_data():
    """Create sample training data."""
    X = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'feature3': np.random.randn(100),
    })
    y = pd.Series(X['feature1'] * 2 + X['feature2'] * 1.5 + np.random.randn(100) * 0.1)
    return X, y


def test_lightgbm_fit_predict(sample_training_data):
    """Test LightGBM model."""
    X, y = sample_training_data
    
    model = LightGBMRegressor(n_estimators=10)
    model.fit(X, y)
    
    predictions = model.predict(X.head(10))
    assert len(predictions) == 10
    assert all(np.isfinite(predictions))


def test_random_forest_fit_predict(sample_training_data):
    """Test Random Forest model."""
    X, y = sample_training_data
    
    model = RandomForestRegressor(n_estimators=10)
    model.fit(X, y)
    
    predictions = model.predict(X.head(10))
    assert len(predictions) == 10
    assert all(np.isfinite(predictions))


def test_prophet_fit():
    """Test Prophet model."""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'date': dates,
        'target': np.sin(np.arange(100) * 2 * np.pi / 365) * 10 + 50 + np.random.randn(100),
    })
    
    model = ProphetForecaster(yearly_seasonality=False, weekly_seasonality=False)
    model.fit(df, target='target', date_col='date')
    
    assert model.model is not None


def test_model_feature_importance(sample_training_data):
    """Test feature importance extraction."""
    X, y = sample_training_data
    
    model = LightGBMRegressor(n_estimators=10)
    model.fit(X, y)
    
    importance = model.get_feature_importance()
    assert isinstance(importance, dict)
    assert len(importance) > 0



