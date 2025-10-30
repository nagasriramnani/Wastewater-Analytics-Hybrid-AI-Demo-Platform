"""Tests for ML pipeline components."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from app.ai.pipeline.ingestion import DataIngestionEngine
from app.ai.pipeline.features import FeatureFactory
from app.ai.pipeline.validation import ValidationSuite
from app.ai.pipeline.serving import ServingLayer


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'date': dates,
        'site_id': ['WWTP_01'] * 100,
        'target': np.random.randn(100).cumsum() + 50,
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
    })


def test_ingestion_load_csv(tmp_path):
    """Test CSV loading."""
    # Create test CSV
    test_file = tmp_path / "test.csv"
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    df.to_csv(test_file, index=False)
    
    engine = DataIngestionEngine()
    loaded_df = engine.load_from_path(str(test_file))
    
    assert len(loaded_df) == 3
    assert 'a' in loaded_df.columns
    assert 'b' in loaded_df.columns


def test_ingestion_detect_schema(sample_df):
    """Test schema detection."""
    engine = DataIngestionEngine()
    schema = engine.detect_schema(sample_df)
    
    assert schema['date_column'] == 'date'
    assert schema['site_column'] == 'site_id'
    assert 'target' in schema['target_columns'] or 'target' in schema['feature_columns']


def test_ingestion_validate_data(sample_df):
    """Test data validation."""
    engine = DataIngestionEngine()
    stats = engine.validate_data(sample_df)
    
    assert stats['rows'] == 100
    assert stats['columns'] == 5
    assert 'missing_pct' in stats
    assert 'duplicates' in stats


def test_feature_factory_build(sample_df):
    """Test feature factory."""
    factory = FeatureFactory(max_lags=3)
    feature_set = factory.build(
        sample_df,
        target_col='target',
        date_col='date',
        site_col='site_id',
    )
    
    assert feature_set.train_X is not None
    assert feature_set.train_y is not None
    assert len(feature_set.train_X) > 0
    assert len(feature_set.train_y) > 0


def test_validation_validate_model_inputs(sample_df):
    """Test model input validation."""
    validator = ValidationSuite()
    X = sample_df[['feature1', 'feature2']]
    y = sample_df['target']
    
    result = validator.validate_model_inputs(X, y)
    assert result['valid'] is True


def test_serving_save_load_model(tmp_path):
    """Test model save and load."""
    serving = ServingLayer(registry_path=str(tmp_path))
    
    # Create dummy model
    class DummyModel:
        def predict(self, X):
            return np.array([1, 2, 3])
    
    model = DummyModel()
    path = serving.save_model(model, "test_model")
    
    assert Path(path).exists()
    
    loaded_model = serving.load_model("test_model")
    assert loaded_model is not None


def test_validation_data_quality(sample_df):
    """Test data quality validation."""
    validator = ValidationSuite()
    report = validator.validate_data_quality(sample_df, 'target')
    
    assert 'quality_score' in report
    assert 'checks' in report
    assert isinstance(report['quality_score'], float)



