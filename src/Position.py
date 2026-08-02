import numpy as np
import math as m
import veclib as vl
import geolib as gl

class Position():
    """class representing the current NED-position. Propagated by velocity
    unit in m
    """

    def __init__(self, vector=vl.Vector()):
        self.values = vector

    def __str__(self):
        px, py, pz = vl.toValue(self.values)
        return "N: {:9.3f} m, E: {:9.3f} m, D: {:9.3f} m".format(px, py, pz)

    def update(self, velocity, dt):
        """updates current position based on previous position and velocity
        velocity-object has attribute values in m/s
        """
        self.values += dt * velocity.values

    def correct(self, vector):
        """vector is defined as (N, E, D) in meter"""
        self.values += vector


class EllipsoidPosition(object):
    """class representing the position on a ellipsoid in LLH. Propagated by velocity
    unit in radian and m
    """

    def __init__(self, vector=vl.Vector()):
        self.values = vector  # (rad, rad, m)
        self.earthParameter = gl.Earth()
        self.ellipsoid = "GRS80"

    def __str__(self):
        lat, lon, h = self.values()
        return "Lat: {:4.6f} deg, Lon: {:4.6f} deg, H: {:4.3f} m".format(
            np.rad2deg(lat), np.rad2deg(lon), h)

    def update(self, velocity, dt):
        """updates current position based on previous position and velocity
        velocity-object has attribute values in m/s
        """
        self.values += np.dot(dt * self._NED2ECEF(), velocity.values)

    def correct(self, vector):
        """vector is defined as (N, E, D) in meter"""
        self.values += np.dot(self._NED2ECEF(), vector)

    def _NED2ECEF(self):
        lat, _, h = self.values()
        Rn, Re = self.earthParameter.curvature(lat, self.earthParameter.GRS80)
        M = np.eye(3, 3)
        M[0, 0] = 1.0 / (Rn - h)
        M[1, 1] = 1.0 / ((Re - h)) * m.cos(lat)
        M[2, 2] = 1.0
        return M