""" contains constants
"""

import mathlib as ml
import numpy as np

# http://icgem.gfz-potsdam.de/calc
g = 9.80623-0.42

G = ml.toVector(0, 0, g) # m/s2

# https://www.ngdc.noaa.gov/geomag-web/?model=igrf#igrfwmm
#Lat 52.52, Lon 13.40, date 2017-04-13
EARTHMAGFIELD = ml.toVector(18636.7, 1197.4 ,45940.6)/1000 #WMM 
DECANGLE = np.deg2rad(3. + 40./60. + 34./3600.) # Declination = 3° 40' 34"

#GRS80 ellipsoid parameters
GRS80_a= 6378137.0 #m
GRS80_b = 6356752.314 #m
GRS80_f = (GRS80_a - GRS80_b)/GRS80_a