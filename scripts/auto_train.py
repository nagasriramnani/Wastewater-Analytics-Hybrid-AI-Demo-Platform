"""Automated training script to run all models programmatically."""

import sys
from pathlib import Path
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.ai.pipeline.ingestion import DataIngestionEngine
from app.ai.pipeline.orchestrator import ModelOrchestrator
from app.ai.pipeline.serving import ServingLayer


def main():
    """Run automated training workflow."""
    print("=" * 60)
    print("Automated Training Workflow")
    print("=" * 60)
    
    # Step 1: Load dataset
    print("\n[Step 1] Loading dataset...")
    data_path = project_root / "app" / "data" / "raw" / "wwtp_sample.csv"
    
    if not data_path.exists():
        print(f"ERROR: Dataset not found at {data_path}")
        print("Please generate sample data first: python scripts/generate_synthetic.py")
        return
    
    ingestion = DataIngestionEngine()
    df = ingestion.load_from_path(str(data_path))
    print(f"✓ Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
    
    # Step 2: Detect schema
    print("\n[Step 2] Detecting schema...")
    schema = ingestion.detect_schema(df)
    print(f"✓ Date column: {schema['date_column']}")
    print(f"✓ Site column: {schema['site_column']}")
    print(f"✓ Target columns: {schema['target_columns']}")
    
    # Step 3: Validate data
    print("\n[Step 3] Validating data quality...")
    stats = ingestion.validate_data(df)
    print(f"✓ Total rows: {stats['rows']}")
    print(f"✓ Missing data: {stats['missing_pct']:.1f}%")
    print(f"✓ Duplicates: {stats['duplicates']}")
    
    # Step 4: Train models
    print("\n[Step 4] Training models...")
    print("This may take 30-90 seconds...")
    
    target_col = "effluent_bod"
    if target_col not in df.columns:
        # Use first numeric column as target
        numeric_cols = df.select_dtypes(include=['number']).columns
        target_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[0]
        print(f"⚠ Using '{target_col}' as target (effluent_bod not found)")
    
    orchestrator = ModelOrchestrator(
        max_rows=5000,  # Limit for demo speed
        early_stopping_rounds=50,
    )
    
    try:
        result = orchestrator.train_all(
            df,
            target=target_col,
            date_col=schema['date_column'],
            site_col=schema['site_column'],
            horizon=30,
        )
        
        print("\n✓ Training complete!")
        print(f"✓ Best model: {result.best_model_key}")
        
        # Step 5: Display metrics
        print("\n[Step 5] Model Performance Metrics:")
        print("-" * 60)
        for model_name, metrics in result.metrics.items():
            if metrics and 'rmse' in metrics:
                print(f"\n{model_name.upper()}:")
                print(f"  RMSE: {metrics['rmse']:.4f}")
                print(f"  MAE:  {metrics['mae']:.4f}")
                if 'r2' in metrics:
                    print(f"  R²:   {metrics['r2']:.4f}")
        
        # Step 6: Save models
        print("\n[Step 6] Saving models to registry...")
        serving = ServingLayer()
        saved_count = 0
        for model_name, model in result.models.items():
            if model is not None:
                metadata = {
                    'target': target_col,
                    'date_col': schema['date_column'],
                    'site_col': schema['site_column'],
                    'metrics': result.metrics.get(model_name, {}),
                }
                path = serving.save_model(model, f"{model_name}_{target_col}", metadata)
                print(f"✓ Saved {model_name}: {Path(path).name}")
                saved_count += 1
        
        print(f"\n✓ Successfully saved {saved_count} models")
        
        print("\n" + "=" * 60)
        print("Training Complete! All models are ready to use.")
        print("=" * 60)
        print(f"\n📊 Next steps:")
        print(f"  1. Start Streamlit: streamlit run app/streamlit_app.py")
        print(f"  2. Navigate to 'AI Training Studio' to view results")
        print(f"  3. Use 'Forecasting Hub' to generate predictions")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())



