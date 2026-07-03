import numpy as np
import math as m

Lat = 52.5  # deg
Lat_rad = np.deg2rad(Lat)

Omega = 7.292115 * 10 ** (-5)  # rad/s IERS - mittlere Winkelgeschwindigkeit der Erde

# Erddrehrate
wex = Omega * m.cos(Lat_rad)
wey = 0
wez = -Omega * m.sin(Lat_rad)

print("Einfluss der Erddrehrate am 52.5 Breitengrad = ", wex, wey, wez, "rad/s")
print(
    "Einfluss der Erddrehrate am 52.5 Breitengrad = ",
    np.rad2deg(wex),
    np.rad2deg(wey),
    np.rad2deg(wez),
    "deg/h",
)

print("Maximaler Drehrate der Erdrotation = ", np.rad2deg(Omega), "deg/s")