
"""Constants"""

import veclib as vl
import numpy as np

""" https://www.ptb.de/cms/ptb/fachabteilungen/abt1/fb-11/fb-11-sis/g-extractor.html
local earth gravity acceleration at Berlin, Germany 
"""
g = 9.81262  # m/s2

G = vl.toVector(0, 0, g)  # m/s2

"""https://www.ngdc.noaa.gov/geomag-web/?model=igrf#igrfwmm
Lat 52.52, Lon 13.40, date 2017-04-13
local earth magnetic field at Berlin, Germany
"""
EARTHMAGFIELD = vl.toVector(18636.7, 1197.4, 45940.6) / 1000  # WMM
DECANGLE = np.deg2rad(3.0 + 40.0 / 60.0 + 34.0 / 3600.0)  # Declination = 3 40 34

"""GRS80 ellipsoid parameters
constants from https://en.wikipedia.org/wiki/GRS_80
"""
GRS80_a = 6378137.0  # m
GRS80_b = 6356752.314  # m
GRS80_f = (GRS80_a - GRS80_b) / GRS80_a