
"""Geodetic Library"""

import math as m
import numpy as np
import veclib as vl


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

        """GRS80 ellipsoid parameters
        constants from https://en.wikipedia.org/wiki/GRS_80
        """
        self.GRS80_a = 6378137.0  # m
        self.GRS80_b = 6356752.314  # m
        self.GRS80_f = (self.GRS80_a - self.GRS80_b) / self.GRS80_a
        self.e2 = m.sqrt(self.GRS80_f * (2.0 - self.GRS80_f))**2.0  # first eccentricity squared

    def curvature(self, lat):
        """calculates radius of curvature in North and East for a given latitude
        """
        sinLat2 = m.sin(lat) ** 2.0
        Rn = self.GRS80_a * ((1.0 - self.e2) / (1.0 - self.e2 * sinLat2) ** (1.5))
        Re = self.GRS80_a / m.sqrt(1.0 - self.e2 * sinLat2)
        return Rn, Re

    def ell2xyz(self, lat, lon, he):
        """transformation of geographic coordinates to cartesian coordinates
        input are latitude, longitude, height in radian and meter
        returns a 3x1 vector
        """
        _, N = self.curvature(lat)
        cosLat = m.cos(lat)
        sinLat = m.sin(lat)
        x = (N + he) * cosLat * m.cos(lon)
        y = (N + he) * cosLat * m.sin(lon)
        z = N * sinLat * (self.GRS80_b**2 / self.GRS80_a**2) + he * sinLat
        return vl.Vector(x, y, z)
