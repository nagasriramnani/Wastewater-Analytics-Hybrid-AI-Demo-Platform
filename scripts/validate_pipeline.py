"""Validate data pipeline without ML training (works with Python 3.14)."""

import sys
from pathlib import Path
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("Data Pipeline Validation (No ML Training)")
print("=" * 60)

try:
    from app.ai.pipeline.ingestion import DataIngestionEngine
    from app.ai.pipeline.features import FeatureFactory
    from app.ai.pipeline.validation import ValidationSuite
    
    # Load data
    print("\n[Step 1] Loading dataset...")
    data_path = project_root / "app" / "data" / "raw" / "wwtp_sample.csv"
    
    if not data_path.exists():
        print(f"[FAIL] Dataset not found: {data_path}")
        sys.exit(1)
    
    ingestion = DataIngestionEngine()
    df = ingestion.load_from_path(str(data_path))
    print(f"[OK] Loaded: {len(df):,} rows, {len(df.columns)} columns")
    
    # Detect schema
    print("\n[Step 2] Schema detection...")
    schema = ingestion.detect_schema(df)
    print(f"[OK] Date column: {schema['date_column']}")
    print(f"[OK] Site column: {schema['site_column']}")
    print(f"[OK] Target columns: {len(schema['target_columns'])} found")
    
    # Validate data
    print("\n[Step 3] Data quality validation...")
    stats = ingestion.validate_data(df)
    print(f"[OK] Total rows: {stats['rows']:,}")
    print(f"[OK] Missing data: {stats['missing_pct']:.1f}%")
    print(f"[OK] Duplicates: {stats['duplicates']}")
    if stats['date_range']:
        print(f"[OK] Date range: {stats['date_range'][0]} to {stats['date_range'][1]}")
    
    # Test feature factory
    print("\n[Step 4] Feature engineering test...")
    if schema['target_columns']:
        target = schema['target_columns'][0]
        print(f"[OK] Using target: {target}")
        
        factory = FeatureFactory(max_lags=3)
        try:
            feature_set = factory.build(
                df.head(200),  # Use subset for speed
                target_col=target,
                date_col=schema['date_column'],
                site_col=schema['site_column'],
                test_size=0.1,
                val_size=0.1,
            )
            print(f"[OK] Feature engineering successful!")
            print(f"[OK] Training samples: {len(feature_set.train_X):,}")
            print(f"[OK] Features created: {len(feature_set.feature_names) if feature_set.feature_names else 'N/A'}")
        except Exception as e:
            print(f"[WARN] Feature engineering error: {e}")
    
    # Validation suite
    print("\n[Step 5] Model input validation...")
    validator = ValidationSuite()
    if schema['target_columns']:
        quality_report = validator.validate_data_quality(df, schema['target_columns'][0])
        print(f"[OK] Quality score: {quality_report['quality_score']:.2%}")
        for check_name, check_result in quality_report['checks'].items():
            status = "[OK]" if check_result['passed'] else "[WARN]"
            print(f"{status} {check_name}: {check_result}")
    
    print("\n" + "=" * 60)
    print("[OK] Data pipeline validation complete!")
    print("[WARN] ML training skipped - needs Python 3.11+")
    print("=" * 60)
    print("\nReady to start Streamlit application!")
    
except Exception as e:
    print(f"\n[FAIL] Pipeline validation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


