import veclib as vl
import constants as c
import math as m
import Quaternion as quat
import numpy as np


class Euler(object):

    def __init__(self, acceleration=-c.G, magneticField=c.EARTHMAGFIELD):
        """calculates the bearing from raw acceleration and magnetometer values
        accelaration in m/s2 and magnetic field in gauss
        angles are saved in radians
        calling w/o arguments creates a vector with phi, theta, psi = 0
        """
        ax, ay, az = vl.toValue(acceleration)
        mx, my, mz = vl.toValue(magneticField)
        if m.isclose(m.hypot(ax, ay, az), 0.0, abs_tol=0.001):
            raise ValueError("Acceleration is not significant")
        if m.isclose(m.hypot(mx, my, mz), 0.0, abs_tol=0.001):
            raise ValueError("MagneticFlux is not significant")

        phi = -m.atan2(ay, -az)  # phi = asin(-ay/g*cos(theta))
        theta = m.asin(ax / c.g)

        # transformation to horizontal coordinate system - psi = 0
        q = quat.Quaternion(vl.toVector(phi, theta, 0.0))
        mHor = q.vecTransformation(magneticField)
        mxh, myh, _ = vl.toValue(mHor)

        psi = m.atan2(myh, mxh) - c.DECANGLE

        self.values = vl.toVector(phi, theta, psi)

    def __str__(self):
        return "{:deg}".format(self)

    def __format__(self, f):
        phi, theta, psi = vl.toValue(self.values)
        if f == "deg":
            return "Roll: {:4.3f} deg, Pitch: {:4.3f} deg, Yaw: {:4.3f} deg".format(
                np.rad2deg(phi), np.rad2deg(theta), np.rad2deg(psi)
            )
        elif f == "rad":
            return "Roll: {:4.3f} rad, Pitch: {:4.3f} rad, Yaw: {:4.3f} rad".format(
                phi, theta, psi
            )


def main():
    E = Euler()
    E.values = vl.toVector(m.pi / 2, m.pi / 4, m.pi / 6)
    print("{:rad}".format(E))
    print(E)


if __name__ == "__main__":
    main()