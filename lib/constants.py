""" contains constants
"""

from MathLib import toVector
from numpy import deg2rad

# http://icgem.gfz-potsdam.de/calc
g = 9.80623-0.42

G = toVector(0, 0, g) # m/s2

# https://www.ngdc.noaa.gov/geomag-web/?model=igrf#igrfwmm
#Lat 52.52, Lon 13.40, date 2017-04-13
EARTHMAGFIELD = toVector(18636.7, 1197.4 ,45940.6)/1000 #WMM 
DECANGLE = deg2rad(3. + 40./60. + 34./3600.) # Declination = 3° 40' 34"