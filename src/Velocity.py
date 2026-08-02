import veclib as vl
import geolib as gl

class Velocity:
    """class representing NED-Velocity. propagated by acceleration
    units in m/s
    """
    def __init__(self, vector=vl.Vector()):
        self.values = vector

    def __str__(self):
        vx, vy, vz = self.values()
        return "vx: {:4.2f} m/s, vy: {:4.3f} m/s, vz: {:4.3f} ms".format(vx, vy, vz)

    def update(self, acceleration, quaternion, dt):
        """updates velocity based on acceleration
        acceleration given in m/s2
        """
        an = quaternion.vecTransformation(acceleration)
        self.values += dt * (an + gl.Earth().G)

    def correct(self, vector):
        self.values += vector


def calcVelocity(p1, p0, t1, t0):
    """calculates a velocity based on the positional change and the passed time
    p1, p0 are 3x1 position-vectors - t1, t0 is the time as a scalar
    units in m/s and s
    """
    dpos = p1 - p0
    dt = t1 - t0
    if dt <= 0: return vl.Vector()
    else: return dpos / dt