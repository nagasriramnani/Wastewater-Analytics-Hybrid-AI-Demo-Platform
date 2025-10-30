"""Synthetic data generator for wastewater datasets."""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta


def generate_wwtp_sample(
    n_sites: int = 3,
    n_days: int = 365,
    start_date: str = "2019-01-01",
    output_path: str = "app/data/raw/wwtp_sample.csv",
) -> pd.DataFrame:
    """Generate synthetic WWTP dataset similar to Kaggle Melbourne dataset.
    
    Args:
        n_sites: Number of treatment plants
        n_days: Number of days of data
        start_date: Start date string
        output_path: Output file path
        
    Returns:
        Generated DataFrame
    """
    dates = pd.date_range(start=start_date, periods=n_days, freq='D')
    sites = [f"WWTP_{i+1:02d}" for i in range(n_sites)]
    
    np.random.seed(42)
    data = []
    
    for site in sites:
        # Base levels for each site
        base_bod = np.random.uniform(5, 15)
        base_cod = np.random.uniform(20, 40)
        base_tss = np.random.uniform(10, 25)
        
        # Seasonal patterns
        day_of_year = np.arange(n_days) % 365
        
        for i, date in enumerate(dates):
            # Seasonal variation
            seasonal = np.sin(2 * np.pi * day_of_year[i] / 365) * 3
            
            # Random noise
            noise_bod = np.random.normal(0, 1)
            noise_cod = np.random.normal(0, 2)
            noise_tss = np.random.normal(0, 1.5)
            
            # Influent values (higher)
            influent_bod = base_bod * 4 + seasonal + noise_bod * 2
            influent_cod = base_cod * 4 + seasonal * 1.5 + noise_cod * 3
            influent_tss = base_tss * 3 + seasonal + noise_tss * 2
            
            # Effluent values (treated, lower)
            treatment_efficiency = np.random.uniform(0.85, 0.95)
            effluent_bod = max(0, influent_bod * (1 - treatment_efficiency))
            effluent_cod = max(0, influent_cod * (1 - treatment_efficiency * 0.9))
            effluent_tss = max(0, influent_tss * (1 - treatment_efficiency * 0.85))
            
            # Nutrients
            nh4 = np.random.uniform(0.5, 3.0) + seasonal * 0.3
            no3 = np.random.uniform(2.0, 8.0) + seasonal * 0.5
            po4 = np.random.uniform(0.3, 2.0) + seasonal * 0.2
            
            # Operational parameters
            flow = np.random.uniform(1000, 5000)  # m3/day
            temperature = 15 + seasonal * 5 + np.random.normal(0, 2)
            aeration = np.random.uniform(50, 200)  # kWh
            energy_kwh = flow * 0.5 + aeration + np.random.normal(0, 100)
            
            data.append({
                'date': date,
                'site_id': site,
                'influent_bod': round(influent_bod, 2),
                'influent_cod': round(influent_cod, 2),
                'influent_tss': round(influent_tss, 2),
                'effluent_bod': round(effluent_bod, 2),
                'effluent_cod': round(effluent_cod, 2),
                'effluent_tss': round(effluent_tss, 2),
                'nh4': round(nh4, 2),
                'no3': round(no3, 2),
                'po4': round(po4, 2),
                'flow_m3d': round(flow, 2),
                'temperature_c': round(temperature, 2),
                'aeration_kwh': round(aeration, 2),
                'energy_kwh': round(energy_kwh, 2),
            })
    
    df = pd.DataFrame(data)
    
    # Add some missing values (5%)
    missing_indices = np.random.choice(len(df), size=int(len(df) * 0.05), replace=False)
    for col in ['effluent_bod', 'effluent_cod', 'effluent_tss']:
        missing_col = np.random.choice(missing_indices, size=len(missing_indices)//3, replace=False)
        df.loc[missing_col, col] = np.nan
    
    # Save to file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"[OK] Generated dataset: {len(df)} rows, {len(df.columns)} columns")
    print(f"Saved to: {output_path}")
    
    return df


def generate_uci_sample(
    output_path: str = "app/data/raw/uci_sample.csv",
    n_records: int = 500,
) -> pd.DataFrame:
    """Generate synthetic dataset similar to UCI Water Treatment.
    
    Args:
        output_path: Output file path
        n_records: Number of records
        
    Returns:
        Generated DataFrame
    """
    np.random.seed(42)
    
    data = {
        'Q_E': np.random.uniform(500, 2000, n_records),  # Input flow
        'ZN_E': np.random.uniform(0, 5, n_records),  # Zinc
        'PH_E': np.random.uniform(6.5, 8.5, n_records),  # pH
        'DBO_E': np.random.uniform(10, 50, n_records),  # BOD
        'DQO_E': np.random.uniform(50, 200, n_records),  # COD
        'SS_E': np.random.uniform(20, 100, n_records),  # Suspended solids
        'SED_E': np.random.uniform(5, 30, n_records),  # Sediment
        'COND_E': np.random.uniform(500, 2000, n_records),  # Conductivity
        'PH_P': np.random.uniform(6.8, 8.0, n_records),  # pH Primary
        'DBO_P': np.random.uniform(5, 30, n_records),  # BOD Primary
        'SS_P': np.random.uniform(10, 60, n_records),  # SS Primary
    }
    
    df = pd.DataFrame(data)
    
    # Save to file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"[OK] Generated UCI-style dataset: {len(df)} rows, {len(df.columns)} columns")
    print(f"Saved to: {output_path}")
    
    return df


if __name__ == "__main__":
    print("Generating synthetic datasets...")
    
    # Generate WWTP sample
    generate_wwtp_sample(
        n_sites=3,
        n_days=365,
        output_path="app/data/raw/wwtp_sample.csv",
    )
    
    # Generate UCI sample
    generate_uci_sample(
        output_path="app/data/raw/uci_sample.csv",
        n_records=500,
    )
    
    print("\n[OK] All datasets generated successfully!")

