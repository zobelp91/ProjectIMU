import numpy as np
import math as m

import geolib as gl
import veclib as vl

ve = 100  # km/h
vn = 100  # km/h^
v = m.hypot(ve, vn)
print("Mittlere Geschwindigkeit = ", v, "km/h")
ve *= 1000 / 3600
vn *= 1000 / 3600

Lat = 52.5  # deg
Lat_rad = np.deg2rad(Lat)
a = 6378137.0  # WGS84
f = 1.0 / 298.257223563
Rn, Re = gl.earthCurvature(a, f, Lat_rad)
h = -30  # m

wtx = ve / (Re - h)
wty = -vn / (Rn - h)
wtz = (ve * m.tan(Lat_rad)) / (Re - h)
print("Einfluss der Transportrate = ", wtx, wty, wtz, "rad/s")
print(
    "Einfluss der Transportrate = ",
    np.rad2deg(wtx) * 3600,
    np.rad2deg(wty) * 3600,
    np.rad2deg(wtz) * 3600,
    "deg/h",
)