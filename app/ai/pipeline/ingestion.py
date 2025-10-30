"""Data ingestion engine for wastewater datasets."""

from pathlib import Path
from typing import Optional, Dict, Any, List
import pandas as pd
import streamlit as st


class DataIngestionEngine:
    """Handles data loading, schema detection, and validation."""
    
    def __init__(self):
        """Initialize ingestion engine."""
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.parquet']
    
    def load_from_path(self, file_path: str) -> pd.DataFrame:
        """Load dataset from file path.
        
        Args:
            file_path: Path to data file
            
        Returns:
            Loaded DataFrame
            
        Raises:
            ValueError: If file format is unsupported
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = path.suffix.lower()
        if suffix not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {suffix}")
        
        if suffix == '.csv':
            df = pd.read_csv(file_path)
        elif suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif suffix == '.parquet':
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(f"Cannot load {suffix} files")
        
        return df
    
    def detect_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect schema and domain mappings.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with schema information
        """
        schema = {
            'date_column': None,
            'site_column': None,
            'target_columns': [],
            'feature_columns': [],
            'numeric_columns': [],
            'categorical_columns': [],
        }
        
        # Detect date column
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                if pd.api.types.is_datetime64_any_dtype(df[col]) or \
                   self._can_parse_date(df[col].head(100)):
                    schema['date_column'] = col
                    break
        
        # Detect site/station column
        for col in df.columns:
            if any(x in col.lower() for x in ['site', 'station', 'location', 'plant']):
                if df[col].dtype in ['object', 'string']:
                    schema['site_column'] = col
                    break
        
        # Separate numeric and categorical
        for col in df.columns:
            if col in [schema['date_column'], schema['site_column']]:
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                schema['numeric_columns'].append(col)
                # Common targets in wastewater
                if any(x in col.lower() for x in ['bod', 'cod', 'tss', 'nh4', 'no3', 'po4']):
                    schema['target_columns'].append(col)
                else:
                    schema['feature_columns'].append(col)
            else:
                schema['categorical_columns'].append(col)
        
        return schema
    
    def _can_parse_date(self, series: pd.Series) -> bool:
        """Check if series can be parsed as dates."""
        try:
            pd.to_datetime(series.dropna().head(10))
            return True
        except:
            return False
    
    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data quality and return statistics.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation stats
        """
        stats = {
            'rows': len(df),
            'columns': len(df.columns),
            'missing_pct': (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100),
            'duplicates': df.duplicated().sum(),
            'date_range': None,
        }
        
        # Try to find date range
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                stats['date_range'] = (
                    str(df[col].min()),
                    str(df[col].max())
                )
                break
            elif 'date' in col.lower():
                try:
                    dates = pd.to_datetime(df[col].dropna())
                    if len(dates) > 0:
                        stats['date_range'] = (
                            str(dates.min()),
                            str(dates.max())
                        )
                except:
                    pass
        
        return stats
    
    def prepare_dataset(
        self,
        df: pd.DataFrame,
        date_col: Optional[str] = None,
        site_col: Optional[str] = None,
        target_col: Optional[str] = None,
    ) -> pd.DataFrame:
        """Prepare dataset for ML pipeline.
        
        Args:
            df: Raw DataFrame
            date_col: Name of date column
            site_col: Name of site/station column
            target_col: Name of target column
            
        Returns:
            Prepared DataFrame
        """
        df_clean = df.copy()
        
        # Parse date column if specified
        if date_col and date_col in df_clean.columns:
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
            df_clean = df_clean.sort_values(date_col)
        
        # Ensure site column is string
        if site_col and site_col in df_clean.columns:
            df_clean[site_col] = df_clean[site_col].astype(str)
        
        return df_clean



