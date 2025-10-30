"""Validation suite for models and data."""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np


class ValidationSuite:
    """Suite of validation functions."""
    
    @staticmethod
    def validate_model_inputs(
        X: pd.DataFrame,
        y: Optional[pd.Series] = None,
    ) -> Dict[str, Any]:
        """Validate model inputs.
        
        Args:
            X: Feature matrix
            y: Optional target vector
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': [],
        }
        
        if X.empty:
            results['valid'] = False
            results['issues'].append("Feature matrix is empty")
            return results
        
        # Check for all NaN columns
        nan_cols = X.columns[X.isnull().all()].tolist()
        if nan_cols:
            results['warnings'].append(f"Columns with all NaN: {nan_cols}")
        
        # Check for infinite values
        inf_cols = []
        for col in X.select_dtypes(include=[np.number]).columns:
            if np.isinf(X[col]).any():
                inf_cols.append(col)
        if inf_cols:
            results['warnings'].append(f"Columns with infinite values: {inf_cols}")
        
        # Check target if provided
        if y is not None:
            if len(y) != len(X):
                results['valid'] = False
                results['issues'].append(f"Length mismatch: X={len(X)}, y={len(y)}")
            
            if y.isnull().all():
                results['valid'] = False
                results['issues'].append("Target contains only NaN values")
        
        return results
    
    @staticmethod
    def validate_forecast_horizon(
        horizon: int,
        min_val: int = 1,
        max_val: int = 365,
    ) -> bool:
        """Validate forecast horizon."""
        return min_val <= horizon <= max_val
    
    @staticmethod
    def validate_data_quality(
        df: pd.DataFrame,
        target_col: str,
    ) -> Dict[str, Any]:
        """Comprehensive data quality check.
        
        Args:
            df: Input DataFrame
            target_col: Target column name
            
        Returns:
            Quality report
        """
        report = {
            'quality_score': 1.0,
            'checks': {},
        }
        
        # Check missing values in target
        missing_target = df[target_col].isnull().sum()
        missing_target_pct = missing_target / len(df) * 100
        report['checks']['target_missing'] = {
            'count': int(missing_target),
            'percentage': float(missing_target_pct),
            'passed': missing_target_pct < 10,  # Less than 10% missing
        }
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        duplicate_pct = duplicates / len(df) * 100
        report['checks']['duplicates'] = {
            'count': int(duplicates),
            'percentage': float(duplicate_pct),
            'passed': duplicate_pct < 5,
        }
        
        # Check data range
        if pd.api.types.is_numeric_dtype(df[target_col]):
            target_min = df[target_col].min()
            target_max = df[target_col].max()
            report['checks']['target_range'] = {
                'min': float(target_min),
                'max': float(target_max),
                'passed': target_min >= 0 and target_max < 1e6,  # Reasonable range
            }
        
        # Calculate quality score
        passed_checks = sum(1 for check in report['checks'].values() if check['passed'])
        total_checks = len(report['checks'])
        report['quality_score'] = passed_checks / total_checks if total_checks > 0 else 0.0
        
        return report



