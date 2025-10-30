"""Model serving layer for predictions."""

from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
from pathlib import Path
import joblib


class ServingLayer:
    """Serves model predictions and handles model persistence."""
    
    def __init__(self, registry_path: Optional[str] = None):
        """Initialize serving layer.
        
        Args:
            registry_path: Path to model registry directory
        """
        self.registry_path = Path(registry_path) if registry_path else Path("app/data/registry")
        self.registry_path.mkdir(parents=True, exist_ok=True)
    
    def save_model(
        self,
        model: Any,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Save model to registry.
        
        Args:
            model: Model object to save
            name: Model name/identifier
            metadata: Optional metadata dictionary
            
        Returns:
            Path to saved model
        """
        model_path = self.registry_path / f"{name}.joblib"
        joblib.dump(model, model_path)
        
        # Save metadata if provided
        if metadata:
            import json
            metadata_path = self.registry_path / f"{name}_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        return str(model_path)
    
    def load_model(self, name: str) -> Optional[Any]:
        """Load model from registry.
        
        Args:
            name: Model name/identifier
            
        Returns:
            Loaded model or None if not found
        """
        model_path = self.registry_path / f"{name}.joblib"
        if not model_path.exists():
            return None
        
        return joblib.load(model_path)
    
    def predict(
        self,
        model: Any,
        X: pd.DataFrame,
        return_std: bool = False,
    ) -> np.ndarray:
        """Make predictions with model.
        
        Args:
            model: Trained model
            X: Feature matrix
            return_std: Whether to return standard deviation (for probabilistic models)
            
        Returns:
            Predictions array
        """
        predictions = model.predict(X)
        return predictions
    
    def forecast(
        self,
        model: Any,
        X: pd.DataFrame,
        horizon: int,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate forecast with confidence intervals.
        
        Args:
            model: Trained model with forecast method
            X: Feature matrix
            horizon: Forecast horizon
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dictionary with 'forecast', 'lower', 'upper' arrays
        """
        # Try model.forecast() if available, otherwise use predict
        if hasattr(model, 'forecast'):
            result = model.forecast(X, horizon=horizon, **kwargs)
            return result
        
        # Fallback: just use predict
        predictions = self.predict(model, X)
        
        # Simple confidence intervals (can be improved with model-specific logic)
        std = np.std(predictions) if len(predictions) > 1 else predictions[0] * 0.1
        lower = predictions - 1.96 * std
        upper = predictions + 1.96 * std
        
        return {
            'forecast': predictions,
            'lower': lower,
            'upper': upper,
        }
    
    def list_models(self) -> List[str]:
        """List all models in registry.
        
        Returns:
            List of model names
        """
        models = []
        for path in self.registry_path.glob("*.joblib"):
            models.append(path.stem)
        return models



