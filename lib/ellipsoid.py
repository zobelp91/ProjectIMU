from dataclasses import dataclass

@dataclass
class Ellipsoid:
    a: float
    b: float
    f: float = 0.0  # flattening
    e2: float = 0.0 # first eccentricity squared

    def __post_init__(self):
        self.f = (self.a - self.b) / self.a
        self.e2 = self.f * (2.0 - self.f)

GRS80 = Ellipsoid(
    6378137.0, 
    6356752.314)