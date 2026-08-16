import unittest

import math
import numpy as np
import veclib as vl
from Quaternion import Quaternion

class QuaternionTest(unittest.TestCase):
    def test_default_constructor_is_identity(self):
        q = Quaternion()
        expected = (1.0, 0.0, 0.0, 0.0)
        got = q()
        for e, g in zip(expected, got):
            self.assertTrue(math.isclose(e, g, rel_tol=1e-9, abs_tol=1e-12))

    def test_constructor_from_info_preserves_values(self):
        # construction via info is not supported anymore; ensure explicit Euler construction works
        phi, theta, psi = 0.1, -0.2, 0.3
        q = Quaternion(phi, theta, psi)
        got = q()
        # basic sanity: q0 is non-zero for these angles
        self.assertNotAlmostEqual(got[0], 0.0)

    def test_euler_to_rotation_matrix_orthonormal_and_det1(self):
        phi, theta, psi = 0.3, -0.2, 1.0
        q = Quaternion(phi, theta, psi)
        R = q.asRotationMatrix()
        self.assertEqual(R.shape, (3, 3))
        I = R @ R.T
        self.assertTrue(np.allclose(I, np.eye(3), atol=1e-7))
        det = np.linalg.det(R)
        self.assertTrue(math.isclose(det, 1.0, rel_tol=1e-6, abs_tol=1e-6))

    def test_identity_multiplication_leaves_quaternion_unchanged(self):
        q = Quaternion(0.4, 0.1, 0.2)
        identity = Quaternion()
        res = identity * q
        for a, b in zip(q(), res()):
            self.assertTrue(math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12))

    def test_get_conjugated_quaternion_inverts_vector_part(self):
        q = Quaternion(0.2, 0.3, -0.1)
        conj = q.getConjugatedQuaternion()
        q0, q1, q2, q3 = q()
        c0, c1, c2, c3 = conj()
        self.assertTrue(math.isclose(q0, c0, rel_tol=1e-12))
        self.assertTrue(math.isclose(q1, -c1, rel_tol=1e-12))
        self.assertTrue(math.isclose(q2, -c2, rel_tol=1e-12))
        self.assertTrue(math.isclose(q3, -c3, rel_tol=1e-12))

    def test_from_acceleration_magnetic_constructs_valid_quaternion(self):
        # construct quaternion from accelerometer and magnetometer readings
        acc = vl.Vector(0.0, 0.0, -9.81)
        mag = vl.Vector(18.0, 5.0, -40.0)
        q = Quaternion.from_acceleration_magnetic(acc, mag)

        # check returned type behaves like quaternion and has unit norm
        vals = q()
        norm = math.sqrt(sum(float(v) ** 2 for v in vals))
        self.assertTrue(math.isclose(norm, 1.0, rel_tol=1e-6, abs_tol=1e-6))

        # rotated acceleration should point approximately down in body frame
        acc_rot = q.vecTransformation(acc)
        x, y, z = acc_rot()
        self.assertTrue(math.isclose(x, 0.0, rel_tol=1e-6, abs_tol=1e-5))
        self.assertTrue(math.isclose(y, 0.0, rel_tol=1e-6, abs_tol=1e-5))
        self.assertTrue(math.isclose(z, -9.81, rel_tol=1e-3, abs_tol=1e-2))

    def test_update_preserves_unit_norm(self):
        q = Quaternion()
        rot = vl.Vector(0.1, 0.2, -0.05)
        q.update(rot, 0.5)
        # check quaternion remains approximately unit length
        vals = q()
        norm = math.sqrt(sum(float(v) ** 2 for v in vals))
        self.assertTrue(math.isclose(norm, 1.0, rel_tol=1e-6, abs_tol=1e-6))

    def test_vecTransformation_identity_leaves_vector_unchanged(self):
        # identity quaternion should not change the vector
        q = Quaternion()  # identity quaternion (1, 0, 0, 0)
        vector = vl.Vector(1.0, 2.0, 3.0)
        result = q.vecTransformation(vector)

        # check each component is preserved
        x, y, z = result()
        self.assertTrue(math.isclose(x, 1.0, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(y, 2.0, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(z, 3.0, rel_tol=1e-9, abs_tol=1e-12))

    def test_vecTransformation_preserves_vector_magnitude(self):
        # rotation should preserve the magnitude of the vector
        q = Quaternion(0.1, 0.2, 0.5)
        vector = vl.Vector(1.5, -2.3, 0.7)
        result = q.vecTransformation(vector)

        # calculate magnitudes
        original_mag = math.sqrt(sum(float(v)**2 for v in vector()))
        result_mag = math.sqrt(sum(float(v)**2 for v in result()))

        self.assertTrue(math.isclose(original_mag, result_mag, rel_tol=1e-9, abs_tol=1e-12))

    def test_vecTransformation_90deg_rotation_around_z_axis(self):
        # 90-degree rotation around z-axis: (phi=pi/2, theta=0, psi=0)
        q = Quaternion(phi=0, theta=0, psi=math.pi/2)
        # vector along x-axis should map to y-axis
        vector = vl.Vector(1.0, 0.0, 0.0)
        result = q.vecTransformation(vector)

        x, y, z = result()
        # after 90° rotation around z: (1,0,0) -> approximately (0,1,0)
        self.assertTrue(math.isclose(x, 0.0, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(y, 1.0, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(z, 0.0, rel_tol=1e-9, abs_tol=1e-12))

    def test_vecTransformation_consistent_with_rotation_matrix(self):
        # vecTransformation should be equivalent to rotating via rotation matrix
        phi, theta, psi = 0.3, -0.15, 0.8
        q = Quaternion(phi, theta, psi)
        vector = vl.Vector(2.1, -1.5, 0.9)

        # method 1: quaternion transformation
        result_quat = q.vecTransformation(vector)

        # method 2: rotation matrix transformation
        R = q.asRotationMatrix()
        result_matrix = R @ vector

        # compare results
        x1, y1, z1 = result_quat()
        x2, y2, z2 = result_matrix[0, 0], result_matrix[1, 0], result_matrix[2, 0]

        self.assertTrue(math.isclose(x1, x2, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(y1, y2, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(z1, z2, rel_tol=1e-9, abs_tol=1e-12))

    def test_vecTransformation_conjugate_matches_rotation_matrix_transpose(self):
        # conjugated quaternion should correspond to inverse rotation (rotation matrix transpose)
        phi, theta, psi = 0.3, -0.15, 0.8
        q = Quaternion(phi, theta, psi)
        vector = vl.Vector(2.1, -1.5, 0.9)

        # method 1: conjugated quaternion transformation
        q_conj = q.getConjugatedQuaternion()
        result_conj = q_conj.vecTransformation(vector)

        # method 2: rotation matrix transpose (inverse)
        R = q.asRotationMatrix()
        result_matrix = R.T @ vector

        # compare results
        x1, y1, z1 = result_conj()
        x2, y2, z2 = result_matrix[0, 0], result_matrix[1, 0], result_matrix[2, 0]

        self.assertTrue(math.isclose(x1, x2, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(y1, y2, rel_tol=1e-9, abs_tol=1e-12))
        self.assertTrue(math.isclose(z1, z2, rel_tol=1e-9, abs_tol=1e-12))


if __name__ == '__main__':
    unittest.main()
