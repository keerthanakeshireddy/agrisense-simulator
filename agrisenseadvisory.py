# agrisense/advisory.py
def irrigation_advisory(soil, crop, min_interval_days=3, last_irrigation_day=None, threshold_frac=0.5, target_frac=0.8, max_depth_mm=50):
    """
    soil: SoilState
    crop: Crop
    last_irrigation_day: int days since start or None
    Returns dict advisory
    """
    frac = soil.avail_fraction()
    advice = {"action": "no_action", "depth_mm": 0.0, "reason": ""}
    if frac < threshold_frac:
        # if recently irrigated (within min interval) skip
        if last_irrigation_day is not None and last_irrigation_day < min_interval_days:
            advice["reason"] = f"low_avail={frac:.2f} but recent irrigation ({last_irrigation_day}d) prevents immediate repeat"
            return advice
        # compute depth to reach target_frac
        needed_mm = max(0.0, target_frac * soil.total_pa_mm - soil.avail_mm)
        depth = min(max_depth_mm, round(needed_mm / 0.7, 1))  # adjust for efficiency
        if depth > 0:
            advice.update({"action": "irrigate", "depth_mm": depth, "reason": f"avail_frac={frac:.2f} below {threshold_frac}"})
    else:
        advice["reason"] = f"avail_frac={frac:.2f} >= {threshold_frac}"
    return advice

def fertiliser_advisory(soil, crop, horizon_days=7):
    """
    If soil.n < expected demand over horizon -> suggest application
    """
    expected = crop.daily_n_demand_kg_ha * horizon_days
    if soil.n_kg_ha < expected:
        required = round(max(0.0, expected - soil.n_kg_ha), 1)
        return {"action": "apply_n", "kg_per_ha": required, "reason": f"soil N {soil.n_kg_ha:.1f} < demand {expected}"}
    return {"action": "no_action", "reason": f"soil N {soil.n_kg_ha:.1f} sufficient for {horizon_days}d"}
