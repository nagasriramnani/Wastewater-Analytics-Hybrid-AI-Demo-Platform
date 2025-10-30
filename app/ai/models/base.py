"""Base model interface."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseModel(ABC):
    """Base class for all models."""
    
    @abstractmethod
    def fit(self, X: Any, y: Any, *args, **kwargs) -> 'BaseModel':
        """Train the model."""
        pass
    
    @abstractmethod
    def predict(self, X: Any) -> Any:
        """Make predictions."""
        pass
    
    def forecast(
        self,
        X: Any,
        horizon: int,
        **kwargs,
    ) -> dict:
        """Generate forecast with confidence intervals (optional)."""
        predictions = self.predict(X)
        return {
            'forecast': predictions,
            'lower': predictions,
            'upper': predictions,
        }



