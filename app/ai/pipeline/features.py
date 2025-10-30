"""Feature engineering factory."""

from typing import Optional, Tuple, List
import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass
class FeatureSet:
    """Container for feature matrices and targets."""
    train_X: pd.DataFrame
    train_y: pd.Series
    val_X: pd.DataFrame
    val_y: pd.Series
    test_X: Optional[pd.DataFrame] = None
    test_y: Optional[pd.Series] = None
    feature_names: Optional[List[str]] = None


class FeatureFactory:
    """Factory for creating engineered features."""
    
    def __init__(self, max_lags: int = 7, window_sizes: List[int] = None):
        """Initialize feature factory.
        
        Args:
            max_lags: Maximum lag features to create
            window_sizes: Rolling window sizes for aggregations
        """
        self.max_lags = max_lags
        self.window_sizes = window_sizes or [3, 7, 14, 30]
    
    def build(
        self,
        df: pd.DataFrame,
        target_col: str,
        date_col: Optional[str] = None,
        site_col: Optional[str] = None,
        test_size: float = 0.2,
        val_size: float = 0.1,
    ) -> FeatureSet:
        """Build feature set from dataset.
        
        Args:
            df: Input DataFrame
            target_col: Target column name
            date_col: Date column name (for time-based features)
            site_col: Site/station column name
            test_size: Test set proportion
            val_size: Validation set proportion
            
        Returns:
            FeatureSet with train/val/test splits
        """
        df_features = df.copy()
        
        # Drop missing target values
        df_features = df_features.dropna(subset=[target_col])
        
        # Create time-based features
        if date_col and date_col in df_features.columns:
            df_features = self._add_time_features(df_features, date_col)
        
        # Create lag features
        df_features = self._add_lag_features(df_features, target_col, date_col)
        
        # Create rolling window features
        df_features = self._add_rolling_features(df_features, target_col, date_col, site_col)
        
        # Create site-specific features if site column exists
        if site_col and site_col in df_features.columns:
            df_features = self._add_site_features(df_features, site_col)
        
        # Select feature columns (exclude target, date, site)
        exclude_cols = [target_col]
        if date_col:
            exclude_cols.append(date_col)
        if site_col:
            exclude_cols.append(site_col)
        
        feature_cols = [c for c in df_features.columns if c not in exclude_cols]
        
        # Handle missing values
        df_features[feature_cols] = df_features[feature_cols].fillna(0)
        
        # Split data
        train_X, train_y, val_X, val_y, test_X, test_y = self._split_data(
            df_features,
            target_col,
            feature_cols,
            date_col,
            test_size,
            val_size,
        )
        
        return FeatureSet(
            train_X=train_X,
            train_y=train_y,
            val_X=val_X,
            val_y=val_y,
            test_X=test_X,
            test_y=test_y,
            feature_names=feature_cols,
        )
    
    def _add_time_features(self, df: pd.DataFrame, date_col: str) -> pd.DataFrame:
        """Add time-based features."""
        df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        df['hour'] = df[date_col].dt.hour
        df['day_of_week'] = df[date_col].dt.dayofweek
        df['day_of_month'] = df[date_col].dt.day
        df['month'] = df[date_col].dt.month
        df['quarter'] = df[date_col].dt.quarter
        df['is_weekend'] = (df[date_col].dt.dayofweek >= 5).astype(int)
        
        return df
    
    def _add_lag_features(
        self,
        df: pd.DataFrame,
        target_col: str,
        date_col: Optional[str] = None,
    ) -> pd.DataFrame:
        """Add lagged target features."""
        df = df.copy()
        
        if date_col:
            df = df.sort_values(date_col)
        
        for lag in range(1, min(self.max_lags + 1, len(df))):
            df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
        
        return df
    
    def _add_rolling_features(
        self,
        df: pd.DataFrame,
        target_col: str,
        date_col: Optional[str] = None,
        site_col: Optional[str] = None,
    ) -> pd.DataFrame:
        """Add rolling window statistics."""
        df = df.copy()
        
        if date_col:
            df = df.sort_values(date_col)
        
        group_cols = [date_col] if date_col else None
        if site_col and site_col in df.columns:
            group_cols = [site_col, date_col] if date_col else [site_col]
            for window in self.window_sizes:
                df[f'{target_col}_rolling_mean_{window}'] = df.groupby(site_col)[target_col].transform(
                    lambda x: x.rolling(window, min_periods=1).mean()
                )
                df[f'{target_col}_rolling_std_{window}'] = df.groupby(site_col)[target_col].transform(
                    lambda x: x.rolling(window, min_periods=1).std()
                )
        else:
            for window in self.window_sizes:
                df[f'{target_col}_rolling_mean_{window}'] = df[target_col].rolling(window, min_periods=1).mean()
                df[f'{target_col}_rolling_std_{window}'] = df[target_col].rolling(window, min_periods=1).std()
        
        return df
    
    def _add_site_features(self, df: pd.DataFrame, site_col: str) -> pd.DataFrame:
        """Add site-specific aggregations."""
        df = df.copy()
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if site_col in numeric_cols:
            numeric_cols.remove(site_col)
        
        # Site-level statistics (can be pre-computed or joined)
        # For simplicity, we'll skip this for now
        
        return df
    
    def _split_data(
        self,
        df: pd.DataFrame,
        target_col: str,
        feature_cols: List[str],
        date_col: Optional[str],
        test_size: float,
        val_size: float,
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        """Split data into train/val/test sets."""
        # Remove rows with NaN in features or target
        mask = ~(df[feature_cols + [target_col]].isnull().any(axis=1))
        df_clean = df[mask].copy()
        
        n = len(df_clean)
        test_end = int(n * (1 - test_size))
        val_end = int(n * (1 - test_size - val_size))
        
        # Time-based split if date column exists
        if date_col:
            df_clean = df_clean.sort_values(date_col)
            train_df = df_clean.iloc[:val_end]
            val_df = df_clean.iloc[val_end:test_end]
            test_df = df_clean.iloc[test_end:]
        else:
            # Random split
            train_df = df_clean.iloc[:val_end]
            val_df = df_clean.iloc[val_end:test_end]
            test_df = df_clean.iloc[test_end:]
        
        train_X = train_df[feature_cols]
        train_y = train_df[target_col]
        val_X = val_df[feature_cols]
        val_y = val_df[target_col]
        test_X = test_df[feature_cols] if len(test_df) > 0 else None
        test_y = test_df[target_col] if len(test_df) > 0 else None
        
        return train_X, train_y, val_X, val_y, test_X, test_y



