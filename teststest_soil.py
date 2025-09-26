# tests/test_soil.py
from agrisense.soil import SoilState

def test_soil_water_balance():
    # Initialize soil with 50% available water
    s = SoilState(init_frac=0.5)
    
    before = s.avail_mm
    
    # Apply rain and check water increased
    s.apply_rain(20.0)
    assert s.avail_mm > before, "Soil water should increase after rain"
    
    # Evapotranspire some water and check non-negative
    s.evapotranspire(5.0)
    assert s.avail_mm >= 0, "Soil water should not go below zero"
