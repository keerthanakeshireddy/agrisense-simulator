# agrisense/soil.py
class SoilState:
    def __init__(self, fc=0.30, pwp=0.12, root_zone_mm=600, init_frac=0.6, initial_n=80.0, percolation_rate=0.1):
        """
        fc, pwp: volumetric fractions (0-1)
        root_zone_mm: root zone thickness in mm
        init_frac: initial fraction of plant-available water (0-1)
        initial_n: kg/ha available nitrogen
        percolation_rate: fraction of water exceeding field capacity that percolates
        """
        self.fc = fc
        self.pwp = pwp
        self.root_zone_mm = root_zone_mm
        self.total_pa_mm = (self.fc - self.pwp) * self.root_zone_mm  # plant-available mm
        self.avail_mm = max(0.0, init_frac * self.total_pa_mm)
        self.n_kg_ha = initial_n
        self.percolation_rate = percolation_rate

    def apply_rain(self, rain_mm):
        """Add fraction of rain to root zone (assume infiltration efficiency 0.9)."""
        self.avail_mm += 0.9 * rain_mm
        self._handle_overflow()

    def irrigate(self, depth_mm, efficiency=0.7):
        """Apply irrigation; efficiency < 1 accounts for losses."""
        self.avail_mm += depth_mm * efficiency
        self._handle_overflow()

    def evapotranspire(self, et_mm):
        """Subtract ET (crop ET applied to soil)."""
        self.avail_mm -= et_mm
        if self.avail_mm < 0:
            self.avail_mm = 0.0

    def _handle_overflow(self):
        """If avail exceeds total PA, extra percolates away."""
        if self.avail_mm > self.total_pa_mm:
            excess = self.avail_mm - self.total_pa_mm
            percolated = excess * self.percolation_rate
            self.avail_mm = self.total_pa_mm  # soil can't hold above FC
            # note: percolated amount could be logged, used for leaching N
            return percolated
        return 0.0

    def avail_fraction(self):
        return 0.0 if self.total_pa_mm <= 0 else self.avail_mm / self.total_pa_mm
