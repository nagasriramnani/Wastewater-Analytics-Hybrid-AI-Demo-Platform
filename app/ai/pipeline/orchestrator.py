"""Model orchestrator for training and evaluation."""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import pandas as pd
from .ingestion import DataIngestionEngine
from .features import FeatureFactory
from .validation import ValidationSuite
from .serving import ServingLayer
from ..utils.metrics import evaluate_regression

# Optional imports for ML models (may not be available on Python 3.14)
try:
    from ..models.lightgbm_model import LightGBMRegressor
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    LightGBMRegressor = None

try:
    from ..models.prophet_model import ProphetForecaster
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    ProphetForecaster = None

try:
    from ..models.random_forest_model import RandomForestRegressor
    RANDOM_FOREST_AVAILABLE = True
except ImportError:
    RANDOM_FOREST_AVAILABLE = False
    RandomForestRegressor = None


@dataclass
class TrainResult:
    """Result of model training."""
    models: Dict[str, Any]
    metrics: Dict[str, Dict[str, float]]
    best_model_key: str
    feature_names: Optional[List[str]] = None


class ModelOrchestrator:
    """Orchestrates model training, evaluation, and serving."""
    
    def __init__(
        self,
        max_rows: Optional[int] = None,
        early_stopping_rounds: int = 50,
    ):
        """Initialize orchestrator.
        
        Args:
            max_rows: Maximum rows to use for training (for demo speed)
            early_stopping_rounds: Early stopping rounds for LightGBM
        """
        self.max_rows = max_rows
        self.early_stopping_rounds = early_stopping_rounds
        self.ingestion = DataIngestionEngine()
        self.feature_factory = FeatureFactory()
        self.validator = ValidationSuite()
        self.serving = ServingLayer()
    
    def train_all(
        self,
        df: pd.DataFrame,
        target: str,
        date_col: Optional[str] = None,
        site_col: Optional[str] = None,
        horizon: int = 30,
    ) -> TrainResult:
        """Train all available models.
        
        Args:
            df: Input DataFrame
            target: Target column name
            date_col: Date column name
            site_col: Site/station column name
            horizon: Forecast horizon for time series models
            
        Returns:
            TrainResult with all trained models and metrics
        """
        # Subsample for demo speed if needed
        if self.max_rows and len(df) > self.max_rows:
            df = df.head(self.max_rows).copy()
        
        # Validate data quality
        quality_report = self.validator.validate_data_quality(df, target)
        if quality_report['quality_score'] < 0.5:
            raise ValueError(f"Data quality too low: {quality_report['quality_score']:.2f}")
        
        models = {}
        metrics = {}
        
        # Build features for LightGBM and RandomForest
        feature_names = None
        try:
            feature_set = self.feature_factory.build(
                df,
                target,
                date_col=date_col,
                site_col=site_col,
            )
            feature_names = feature_set.feature_names
            
            # Train LightGBM (if available)
            if LIGHTGBM_AVAILABLE and LightGBMRegressor is not None:
                try:
                    lgb = LightGBMRegressor(
                        early_stopping_rounds=self.early_stopping_rounds,
                    )
                    lgb.fit(feature_set.train_X, feature_set.train_y, feature_set.val_X, feature_set.val_y)
                    models['lightgbm'] = lgb
                    metrics['lightgbm'] = evaluate_regression(lgb, feature_set.val_X, feature_set.val_y)
                except Exception as e:
                    models['lightgbm'] = None
                    metrics['lightgbm'] = {'rmse': float('inf'), 'mae': float('inf')}
            else:
                models['lightgbm'] = None
                metrics['lightgbm'] = {'rmse': float('inf'), 'mae': float('inf')}
            
            # Train RandomForest (if available)
            if RANDOM_FOREST_AVAILABLE and RandomForestRegressor is not None:
                try:
                    rf = RandomForestRegressor()
                    rf.fit(feature_set.train_X, feature_set.train_y)
                    models['random_forest'] = rf
                    metrics['random_forest'] = evaluate_regression(rf, feature_set.val_X, feature_set.val_y)
                except Exception as e:
                    models['random_forest'] = None
                    metrics['random_forest'] = {'rmse': float('inf'), 'mae': float('inf')}
            else:
                models['random_forest'] = None
                metrics['random_forest'] = {'rmse': float('inf'), 'mae': float('inf')}
        except Exception as e:
            # Fallback if feature engineering fails
            feature_names = None
            models['lightgbm'] = None
            models['random_forest'] = None
            metrics['lightgbm'] = {'rmse': float('inf'), 'mae': float('inf')}
            metrics['random_forest'] = {'rmse': float('inf'), 'mae': float('inf')}
        
        # Train Prophet (time series specific, if available)
        if PROPHET_AVAILABLE and ProphetForecaster is not None:
            try:
                if date_col:
                    prophet = ProphetForecaster()
                    prophet.fit(df, target, date_col=date_col)
                    models['prophet'] = prophet
                    # Prophet validation requires different approach
                    if date_col:
                        metrics['prophet'] = prophet.validate(df, target, date_col, horizon=horizon)
                    else:
                        metrics['prophet'] = {'rmse': float('inf'), 'mae': float('inf')}
                else:
                    models['prophet'] = None
                    metrics['prophet'] = {'rmse': float('inf'), 'mae': float('inf')}
            except Exception as e:
                models['prophet'] = None
                metrics['prophet'] = {'rmse': float('inf'), 'mae': float('inf')}
        else:
            models['prophet'] = None
            metrics['prophet'] = {'rmse': float('inf'), 'mae': float('inf')}
        
        # Determine best model (lowest RMSE)
        valid_metrics = {k: v for k, v in metrics.items() if 'rmse' in v and v['rmse'] != float('inf')}
        if valid_metrics:
            best_model_key = min(valid_metrics, key=lambda k: valid_metrics[k]['rmse'])
        else:
            best_model_key = 'lightgbm' if models.get('lightgbm') else list(models.keys())[0]
        
        return TrainResult(
            models=models,
            metrics=metrics,
            best_model_key=best_model_key,
            feature_names=feature_names,
        )



