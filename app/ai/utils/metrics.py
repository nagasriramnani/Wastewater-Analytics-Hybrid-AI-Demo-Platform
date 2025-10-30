"""Metrics and evaluation utilities."""

from typing import Dict, Any
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_regression(
    model: Any,
    X: Any,
    y: Any,
    predictions: Any = None,
) -> Dict[str, float]:
    """Evaluate regression model performance.
    
    Args:
        model: Trained model with predict method
        X: Feature matrix
        y: True target values
        predictions: Optional pre-computed predictions
        
    Returns:
        Dictionary with metrics
    """
    if predictions is None:
        predictions = model.predict(X)
    
    y_true = np.array(y)
    y_pred = np.array(predictions)
    
    # Remove any NaN values
    mask = ~(np.isnan(y_true) | np.isnan(y_pred))
    y_true = y_true[mask]
    y_pred = y_pred[mask]
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    # Calculate MAPE (Mean Absolute Percentage Error)
    with np.errstate(divide='ignore', invalid='ignore'):
        mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100
    
    # Calculate SMAPE (Symmetric Mean Absolute Percentage Error)
    with np.errstate(divide='ignore', invalid='ignore'):
        smape = np.mean(200 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred) + 1e-10))
    
    return {
        'mae': float(mae),
        'mse': float(mse),
        'rmse': float(rmse),
        'r2': float(r2),
        'mape': float(mape),
        'smape': float(smape),
    }


def calculate_anomaly_scores(
    values: np.ndarray,
    method: str = 'zscore',
    threshold: float = 3.0,
) -> np.ndarray:
    """Calculate anomaly scores using various methods.
    
    Args:
        values: Array of values
        method: 'zscore', 'iqr', or 'residual'
        threshold: Threshold for anomaly detection
        
    Returns:
        Array of anomaly scores (higher = more anomalous)
    """
    if method == 'zscore':
        mean = np.nanmean(values)
        std = np.nanstd(values)
        if std == 0:
            return np.zeros_like(values)
        scores = np.abs((values - mean) / std)
        return scores
    
    elif method == 'iqr':
        q1 = np.nanpercentile(values, 25)
        q3 = np.nanpercentile(values, 75)
        iqr = q3 - q1
        if iqr == 0:
            return np.zeros_like(values)
        scores = np.abs((values - np.nanmedian(values)) / iqr)
        return scores
    
    else:
        return np.zeros_like(values)



