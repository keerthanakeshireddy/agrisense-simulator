# tests/test_integration.py
import pandas as pd
from agrisense.simulator import run_sim

def test_run_sim_30_days():
    df = run_sim(days=30)  # run simulation for 30 days
    
    # Check no missing values
    assert not df.isna().any().any(), "DataFrame contains NaNs"
    
    # Check expected columns
    expected_cols = ["Day", "Temperature", "Soil Moisture", "Rainfall"]
    for col in expected_cols:
        assert col in df.columns, f"{col} missing from DataFrame"
