# agrisense/et.py
import math

def hargreaves_et0(tmin_C, tmax_C, lat=17.0):
    """
    Simplified Hargreaves ET0 (mm/day). Good enough for prototyping.
    """
    tmean = (tmax_C + tmin_C) / 2.0
    td = max(0.0, tmax_C - tmin_C)
    # Ra (extraterrestrial radiation) approx — we keep it simple: use a small constant factor
    # For production, replace with FAO-56 calculation (use pyeto or implement Ra by latitude & day-of-year)
    Ra = 20.0
    et0 = 0.0023 * Ra * (tmean + 17.8) * math.sqrt(td)
    return max(0.0, et0)

def crop_et(et0, kc):
    return et0 * kc
