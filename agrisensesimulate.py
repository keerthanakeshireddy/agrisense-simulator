# agrisense/simulate.py
import pandas as pd
from agrisense.weather_gen import generate_synthetic_weather
from agrisense.et import hargreaves_et0, crop_et
from agrisense.soil import SoilState
from agrisense.crop import Crop
from agrisense.advisory import irrigation_advisory, fertiliser_advisory
from datetime import date

def run_sim(days=30, seed=0):
    start = date.today()
    weather = generate_synthetic_weather(start, days, seed=seed)
    soil = SoilState()
    crop = Crop()
    rows = []
    last_irrigation_days_ago = 999
    for i, r in weather.iterrows():
        tmin, tmax, rain = r["tmin_C"], r["tmax_C"], r["rainfall_mm"]
        et0 = hargreaves_et0(tmin, tmax)
        etc = crop_et(et0, crop.kc)
        # apply rain then ET
        soil.apply_rain(rain)
        soil.evapotranspire(etc)
        # crop consumes N
        soil.n_kg_ha = max(0.0, soil.n_kg_ha - crop.daily_n_demand_kg_ha)
        # advisories
        irr = irrigation_advisory(soil, crop, last_irrigation_day=None if last_irrigation_days_ago>999 else last_irrigation_days_ago)
        fert = fertiliser_advisory(soil, crop)
        # apply irrigation immediately in sim if recommended
        if irr["action"] == "irrigate":
            soil.irrigate(irr["depth_mm"])
            last_irrigation_days_ago = 0
        else:
            last_irrigation_days_ago += 1
        # apply half fertilizer if recommended (simulate partial adoption)
        if fert["action"] == "apply_n":
            applied = fert["kg_per_ha"] * 0.5
            soil.n_kg_ha += applied
        crop_state = crop.step(tmin, tmax)
        rows.append({
            "date": r["date"],
            "tmax": tmax, "tmin": tmin, "rain_mm": rain,
            "et0": round(et0,2), "etc": round(etc,2),
            "avail_mm": round(soil.avail_mm,1), "avail_frac": round(soil.avail_fraction(),2),
            "soil_n": round(soil.n_kg_ha,1),
            "irrigation_adv": irr, "fertiliser_adv": fert, "crop_stage": crop_state["stage"]
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = run_sim(30, seed=42)
    df.to_csv("output/simulation.csv", index=False)
    print("Wrote output/simulation.csv")
