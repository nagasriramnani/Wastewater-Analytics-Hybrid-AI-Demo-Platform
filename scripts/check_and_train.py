"""Check dependencies and run training if available."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("Wastewater AI Platform - Pre-Flight Check & Training")
print("=" * 60)

# Check dependencies
print("\n[1/3] Checking dependencies...")
missing = []

try:
    import pandas as pd
    print("[OK] Pandas:", pd.__version__)
except ImportError:
    print("[FAIL] Pandas NOT installed")
    missing.append("pandas")

try:
    import numpy as np
    print("[OK] NumPy:", np.__version__)
except ImportError:
    print("[FAIL] NumPy NOT installed")
    missing.append("numpy")

try:
    import lightgbm
    print("[OK] LightGBM: Available")
except ImportError:
    print("[WARN] LightGBM: NOT available (needs Python 3.11)")
    missing.append("lightgbm")

try:
    import prophet
    print("[OK] Prophet: Available")
except ImportError:
    print("[WARN] Prophet: NOT available (needs Python 3.11)")
    missing.append("prophet")

try:
    from sklearn.ensemble import RandomForestRegressor
    print("[OK] scikit-learn: Available")
except ImportError:
    print("[WARN] scikit-learn: NOT available (needs Python 3.11)")
    missing.append("scikit-learn")

# Check data
print("\n[2/3] Checking sample data...")
data_path = project_root / "app" / "data" / "raw" / "wwtp_sample.csv"
if data_path.exists():
    print(f"[OK] Sample data found: {data_path}")
    import pandas as pd
    df = pd.read_csv(data_path)
    print(f"  - Rows: {len(df):,}")
    print(f"  - Columns: {len(df.columns)}")
else:
    print(f"[FAIL] Sample data NOT found: {data_path}")
    print("  Generating sample data...")
    try:
        from scripts.generate_synthetic import generate_wwtp_sample
        generate_wwtp_sample(output_path=str(data_path))
        print("[OK] Sample data generated!")
    except Exception as e:
        print(f"[FAIL] Failed to generate: {e}")

# Run training if ML libraries available
print("\n[3/3] Running ML Training...")

if "lightgbm" not in missing and "prophet" not in missing and "scikit-learn" not in missing:
    print("All ML libraries available! Starting training...")
    try:
        from scripts.auto_train import main as train_main
        result = train_main()
        if result == 0:
            print("\n[OK] Training completed successfully!")
        else:
            print("\n[WARN] Training completed with warnings")
    except Exception as e:
        print(f"\n[FAIL] Training failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("[WARN] ML libraries not available. Skipping training.")
    print("\nTo enable ML training:")
    print("  1. Install Python 3.11 or 3.13")
    print("  2. Create new venv: py -3.11 -m venv venv311")
    print("  3. Install: pip install -r requirements.txt")
    print("\nCurrent UI features will work without ML libraries.")

print("\n" + "=" * 60)
print("Pre-flight check complete!")
print("=" * 60)

