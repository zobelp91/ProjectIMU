import unittest
import veclib as vl
import geolib as gl
from Velocity import Velocity, calcVelocity

class DummyQuat:
    def vecTransformation(self, vector):
        # identity transformation used for tests
        return vector

class VelocityTest(unittest.TestCase):
    def test_str_representation(self):
        v = Velocity(1.234, 2.345, 3.456)
        s = str(v)
        # basic checks: keys and numeric substrings
        self.assertIn('vx:', s)
        self.assertIn('vy:', s)
        self.assertIn('vz:', s)
        # formatted numbers should appear (approximate)
        self.assertIn('1.23', s)
        self.assertIn('2.345', s)

    def test_update_with_identity_quaternion(self):
        v = Velocity()
        q = DummyQuat()
        # zero acceleration -> velocity should become gravity * dt
        v.update(vl.Vector(), q, 1.0)
        vx, vy, vz = v()
        self.assertAlmostEqual(vx, 0.0, places=6)
        self.assertAlmostEqual(vy, 0.0, places=6)
        self.assertAlmostEqual(vz, gl.Earth().g, places=6)

        # non-zero acceleration
        v2 = Velocity()
        accel = vl.Vector(1.0, 0.0, 0.0)
        dt = 2.0
        v2.update(accel, q, dt)
        vx2, vy2, vz2 = v2()
        # expected: dt * (accel + gravity)
        self.assertAlmostEqual(vx2, dt * 1.0, places=6)
        self.assertAlmostEqual(vy2, 0.0, places=6)
        self.assertAlmostEqual(vz2, dt * gl.Earth().g, places=6)

    def test_correct_adds_vector(self):
        v = Velocity()
        v.correct(vl.Vector(0.5, -0.5, 1.0))
        vx, vy, vz = v()
        self.assertAlmostEqual(vx, 0.5, places=6)
        self.assertAlmostEqual(vy, -0.5, places=6)
        self.assertAlmostEqual(vz, 1.0, places=6)

    def test_calcVelocity_basic(self):
        p0 = vl.Vector()
        p1 = vl.Vector(2.0, 0.0, 0.0)
        v = calcVelocity(p1, p0, 2.0, 0.0)
        vx, vy, vz = v()
        self.assertAlmostEqual(vx, 1.0, places=6)
        self.assertAlmostEqual(vy, 0.0, places=6)
        self.assertAlmostEqual(vz, 0.0, places=6)

    def test_calcVelocity_nonpositive_dt(self):
        p0 = vl.Vector()
        p1 = vl.Vector(1.0, 1.0, 1.0)
        v = calcVelocity(p1, p0, 0.0, 1.0)  # dt = -1
        vx, vy, vz = v()
        self.assertAlmostEqual(vx, 0.0, places=6)
        self.assertAlmostEqual(vy, 0.0, places=6)
        self.assertAlmostEqual(vz, 0.0, places=6)

if __name__ == '__main__':
    unittest.main()
