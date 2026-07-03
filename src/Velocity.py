import veclib as vl
import constants as c


class Velocity(object):
    def __init__(self, vector=vl.toVector(0.0, 0.0, 0.0)):
        """class Velocity propagates the velocity based on acceleration
        initialized by velocity-vector
        units in m/s
        """
        self.values = vector

    def __str__(self):
        vx, vy, vz = vl.toValue(self.values)
        return "vx: {:4.2f} m/s, vy: {:4.3f} m/s, vz: {:4.3f} ms".format(vx, vy, vz)

    def update(self, acceleration, quaternion, DT):
        """updates velocity based on acceleration
        acceleration given in m/s2
        """
        an = quaternion.vecTransformation(acceleration)
        self.values += DT * (an + c.G)

    def correct(self, vector):
        self.values += vector


def calcVelocity(p1, p0, t1, t0):
    """calculates a velocity-vector based on the positional change and the passed time
    p1, p0 are 3x1 position-vectors - t1, t0 is the time as a scalar
    unit of return value depends on units of arguments
    """
    dp = p1 - p0
    dt = t1 - t0
    if dt == 0:
        v = vl.toVector(0.0, 0.0, 0.0)
    else:
        v = dp / abs(dt)
    return v