import numpy as np
import math as m
import veclib as vl
import geolib as gl

class Position(vl.Vector):
    """class representing the current NED-position. Propagated by velocity
    unit in m
    """

    def __str__(self):
        px, py, pz = self()
        return "N: {:9.3f} m, E: {:9.3f} m, D: {:9.3f} m".format(px, py, pz)

    def update(self, velocity, dt):
        """updates current position based on previous position and velocity
        velocity-object has attribute values in m/s
        """
        self += dt * velocity

    def correct(self, vector):
        """vector is defined as (N, E, D) in meter"""
        self += vector


class EllipsoidPosition(vl.Vector):
    """class representing the position on a ellipsoid in LLH. Propagated by velocity
    unit in radian and m
    """

    def __str__(self):
        lat, lon, h = self()
        return "Lat: {:4.6f} deg, Lon: {:4.6f} deg, H: {:4.3f} m".format(
            np.rad2deg(lat), np.rad2deg(lon), h)

    def update(self, velocity, dt):
        """updates current position based on previous position and velocity
        velocity-object has attribute values in m/s
        """
        self += np.dot(dt * self._NED2ECEF(), velocity)

    def correct(self, vector):
        """vector is defined as (N, E, D) in meter"""
        self += np.dot(self._NED2ECEF(), vector)

    def _NED2ECEF(self):
        earthParam = self._getEllipsoidParameter()
        lat, _, h = self()
        Rn, Re = gl.Earth().curvature(lat, earthParam)
        M = np.eye(3, 3)
        M[0, 0] = 1.0 / (Rn - h)
        M[1, 1] = 1.0 / ((Re - h)) * m.cos(lat)
        M[2, 2] = 1.0
        return M

    def _getEllipsoidParameter(self):
        """returns the ellipsoid parameter object"""
        match self.info:
            case "GRS80":
                return gl.Earth().GRS80
            case "WGS84":
                return gl.Earth().WGS84
            case _:
                return gl.Earth().GRS80
