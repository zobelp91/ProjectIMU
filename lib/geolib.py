
"""Geodetic Library"""

import math as m
import numpy as np
import veclib as vl
import ellipsoid as el

class Earth:
    def __init__(self):
        """ https://www.ptb.de/cms/ptb/fachabteilungen/abt1/fb-11/fb-11-sis/g-extractor.html
        local earth gravity acceleration at Berlin, Germany 
        """
        self.g = 9.81262  # m/s2
        self.G = vl.Vector(0, 0, self.g)  # m/s2

        """https://www.ngdc.noaa.gov/geomag-web/?model=igrf#igrfwmm
        Lat 52.52, Lon 13.40, date 2017-04-13
        local earth magnetic field at Berlin, Germany
        """
        self.magfield = vl.Vector(18636.7, 1197.4, 45940.6) / 1000  # WMM
        self.declination = np.deg2rad(3.0 + 40.0 / 60.0 + 34.0 / 3600.0)  # Declination = 3 40 34

        """ellipsoid parameters
        """
        self.GRS80 = el.GRS80
        self.WGS84 = None  # WGS84 not implemented yet

    def curvature(self, lat, ellipsoid=el.GRS80):
        """calculates radius of curvature in North and East for a given latitude
        """
        sinLat2 = m.sin(lat) ** 2.0
        Rn = ellipsoid.a * ((1.0 - ellipsoid.e2) / (1.0 - ellipsoid.e2 * sinLat2) ** (1.5))
        Re = ellipsoid.a / m.sqrt(1.0 - ellipsoid.e2 * sinLat2)
        return Rn, Re

    def ell2xyz(self, lat, lon, he, ellipsoid=el.GRS80):
        """transformation of geographic coordinates to cartesian coordinates
        input are latitude, longitude, height in radian and meter
        returns a 3x1 vector
        """
        _, N = self.curvature(lat)
        cosLat = m.cos(lat)
        sinLat = m.sin(lat)
        x = (N + he) * cosLat * m.cos(lon)
        y = (N + he) * cosLat * m.sin(lon)
        z = N * sinLat * (ellipsoid.b**2 / ellipsoid.a**2) + he * sinLat
        return vl.Vector(x, y, z)
