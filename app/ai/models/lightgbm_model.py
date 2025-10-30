"""LightGBM regression model."""

from typing import Any, Optional
import pandas as pd
import numpy as np
import lightgbm as lgb
from .base import BaseModel


class LightGBMRegressor(BaseModel):
    """LightGBM regression model wrapper."""
    
    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 5,
        early_stopping_rounds: int = 50,
        random_seed: int = 42,
    ):
        """Initialize LightGBM model.
        
        Args:
            n_estimators: Number of boosting rounds
            learning_rate: Learning rate
            max_depth: Maximum tree depth
            early_stopping_rounds: Early stopping rounds
            random_seed: Random seed
        """
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.early_stopping_rounds = early_stopping_rounds
        self.random_seed = random_seed
        self.model: Optional[lgb.LGBMRegressor] = None
    
    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        val_X: Optional[pd.DataFrame] = None,
        val_y: Optional[pd.Series] = None,
    ) -> 'LightGBMRegressor':
        """Train the model.
        
        Args:
            X: Training features
            y: Training target
            val_X: Validation features (optional, for early stopping)
            val_y: Validation target (optional)
        """
        self.model = lgb.LGBMRegressor(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=self.max_depth,
            random_state=self.random_seed,
            verbose=-1,
        )
        
        # Fit with validation set if provided
        if val_X is not None and val_y is not None:
            self.model.fit(
                X,
                y,
                eval_set=[(val_X, val_y)],
                callbacks=[
                    lgb.early_stopping(self.early_stopping_rounds, verbose=False),
                ],
            )
        else:
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
        feature_names = self.model.feature_name_
        
        return dict(zip(feature_names, importances))



