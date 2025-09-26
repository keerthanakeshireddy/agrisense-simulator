# agrisense/weather_gen.py
import math, random
import pandas as pd
from datetime import date, timedelta

def generate_synthetic_weather(start_date: date, days: int, lat=17.0, seed=None):
    if seed is not None:
        random.seed(seed)
    rows = []
    for i in range(days):
        d = start_date + timedelta(days=i)
        # seasonal temp using sine wave
        seasonal = 6 * math.sin(2 * math.pi * (d.timetuple().tm_yday) / 365.0)
        t_mean = 26 + seasonal
        tmax = round(t_mean + random.uniform(2,6), 1)
        tmin = round(t_mean - random.uniform(3,6), 1)
        rain = 0.0
        # simple rainy season probability
        rain_prob = 0.15 + 0.25 * (1 if 6 <= d.month <= 9 else 0)  # heavier Jun-Sep
        if random.random() < rain_prob:
            rain = round(random.uniform(5, 80), 1)
        rows.append({"date": d.isoformat(), "tmax_C": tmax, "tmin_C": tmin, "rainfall_mm": rain})
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    df = generate_synthetic_weather(date.today(), 120, seed=42)
    df.to_csv("data/weather.csv", index=False)
    print("Wrote data/weather.csv")
