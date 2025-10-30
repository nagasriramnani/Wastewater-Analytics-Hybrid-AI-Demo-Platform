"""Random Forest regression model."""

from typing import Any, Optional
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor as SKRandomForestRegressor
from .base import BaseModel


class RandomForestRegressor(BaseModel):
    """Random Forest regression wrapper."""
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        random_seed: int = 42,
    ):
        """Initialize Random Forest model.
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            min_samples_split: Minimum samples to split
            random_seed: Random seed
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_seed = random_seed
        self.model: Optional[SKRandomForestRegressor] = None
    
    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        **kwargs,
    ) -> 'RandomForestRegressor':
        """Train the model.
        
        Args:
            X: Training features
            y: Training target
        """
        self.model = SKRandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            random_state=self.random_seed,
            n_jobs=-1,
        )
        self.model.fit(X, y)
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions.
        
        Args:
            X: Feature matrix
            
        Returns:
            Predictions array
        """
        if self.model is None:
            raise ValueError("Model must be fitted before prediction")
        
        return self.model.predict(X)
    
    def get_feature_importance(self) -> dict:
        """Get feature importance.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if self.model is None:
            return {}
        
        importances = self.model.feature_importances_
        feature_names = self.model.feature_names_in_ if hasattr(self.model, 'feature_names_in_') else None
        
        if feature_names is None:
            # Fallback: use indices
            feature_names = [f"feature_{i}" for i in range(len(importances))]
        
        return dict(zip(feature_names, importances))



