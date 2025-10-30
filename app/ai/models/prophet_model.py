"""Prophet time series forecasting model."""

from typing import Any, Optional, Dict
import pandas as pd
import numpy as np
from prophet import Prophet
from .base import BaseModel


class ProphetForecaster(BaseModel):
    """Prophet time series forecasting wrapper."""
    
    def __init__(
        self,
        yearly_seasonality: bool = True,
        weekly_seasonality: bool = True,
        daily_seasonality: bool = False,
    ):
        """Initialize Prophet model.
        
        Args:
            yearly_seasonality: Enable yearly seasonality
            weekly_seasonality: Enable weekly seasonality
            daily_seasonality: Enable daily seasonality
        """
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.daily_seasonality = daily_seasonality
        self.model: Optional[Prophet] = None
        self.date_col: Optional[str] = None
        self.target_col: Optional[str] = None
    
    def fit(
        self,
        df: pd.DataFrame,
        target: str,
        date_col: str,
        **kwargs,
    ) -> 'ProphetForecaster':
        """Train the model.
        
        Args:
            df: Input DataFrame
            target: Target column name
            date_col: Date column name
        """
        self.date_col = date_col
        self.target_col = target
        
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = df[[date_col, target]].copy()
        prophet_df.columns = ['ds', 'y']
        prophet_df = prophet_df.dropna()
        
        # Sort by date
        prophet_df = prophet_df.sort_values('ds')
        
        # Initialize and fit Prophet
        self.model = Prophet(
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
        )
        
        try:
            self.model.fit(prophet_df)
        except Exception as e:
            # Fallback: simpler model if fit fails
            self.model = Prophet(yearly_seasonality=False, weekly_seasonality=False)
            self.model.fit(prophet_df)
        
        return self
    
    def predict(self, X: Any) -> np.ndarray:
        """Make predictions (requires date column in X).
        
        Args:
            X: Feature matrix (must include date column)
            
        Returns:
            Predictions array
        """
        if self.model is None:
            raise ValueError("Model must be fitted before prediction")
        
        # Prophet requires future dates
        # For now, return a placeholder
        # This should be handled by forecast() method
        return np.array([0.0] * len(X))
    
    def forecast(
        self,
        X: Any,
        horizon: int,
        **kwargs,
    ) -> Dict[str, np.ndarray]:
        """Generate forecast for future periods.
        
        Args:
            X: Not used (Prophet needs future dates)
            horizon: Number of periods to forecast
            
        Returns:
            Dictionary with 'forecast', 'lower', 'upper' arrays
        """
        if self.model is None:
            raise ValueError("Model must be fitted before forecast")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=horizon)
        
        # Make predictions
        forecast_df = self.model.predict(future)
        
        # Extract the forecasted values, lower, and upper bounds
        forecast_values = forecast_df['yhat'].tail(horizon).values
        lower_values = forecast_df['yhat_lower'].tail(horizon).values
        upper_values = forecast_df['yhat_upper'].tail(horizon).values
        
        return {
            'forecast': forecast_values,
            'lower': lower_values,
            'upper': upper_values,
        }
    
    def validate(
        self,
        df: pd.DataFrame,
        target: str,
        date_col: str,
        horizon: int = 30,
    ) -> Dict[str, float]:
        """Validate model on historical data.
        
        Args:
            df: Full dataset
            target: Target column
            date_col: Date column
            horizon: Forecast horizon for validation
            
        Returns:
            Dictionary with metrics
        """
        if self.model is None:
            return {'rmse': float('inf'), 'mae': float('inf')}
        
        # Use last horizon periods for validation
        prophet_df = df[[date_col, target]].copy()
        prophet_df.columns = ['ds', 'y']
        prophet_df = prophet_df.sort_values('ds').dropna()
        
        if len(prophet_df) < horizon:
            horizon = len(prophet_df) // 2
        
        train_df = prophet_df.iloc[:-horizon]
        test_df = prophet_df.iloc[-horizon:]
        
        # Fit on training data
        val_model = Prophet(
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
        )
        val_model.fit(train_df)
        
        # Predict
        future = val_model.make_future_dataframe(periods=horizon)
        forecast = val_model.predict(future)
        
        # Calculate metrics
        actual = test_df['y'].values
        predicted = forecast['yhat'].tail(horizon).values
        
        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        
        return {
            'mae': float(mae),
            'rmse': float(rmse),
        }



