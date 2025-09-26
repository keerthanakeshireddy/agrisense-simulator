# agrisense/crop.py
class Crop:
    def __init__(self, name="maize", base_temp=10.0, gdd_to_maturity=1800, kc=1.05, daily_n_demand_kg_ha=1.0):
        """
        base_temp: base temperature for GDD calc
        gdd_to_maturity: cumulative GDD for maturity
        kc: baseline crop coefficient (or a schedule can be used)
        """
        self.name = name
        self.base_temp = base_temp
        self.gdd_to_maturity = gdd_to_maturity
        self.kc = kc
        self.daily_n_demand_kg_ha = daily_n_demand_kg_ha
        self.gdd = 0.0

    def step(self, tmin, tmax):
        tmean = (tmin + tmax) / 2.0
        gdd_today = max(0.0, tmean - self.base_temp)
        self.gdd += gdd_today
        # simple growth stage:
        frac = min(1.0, self.gdd / self.gdd_to_maturity)
        if frac < 0.2:
            stage = "Establishment"
        elif frac < 0.6:
            stage = "Vegetative"
        elif frac < 0.95:
            stage = "Reproductive"
        else:
            stage = "Maturity"
        return {"gdd": self.gdd, "frac": frac, "stage": stage, "kc": self.kc}
