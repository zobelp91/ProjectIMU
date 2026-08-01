import veclib as vl
import math as m
import numpy as np


class Quaternion(object):
    """class Quaternion describes the transformation between 2 coordinate systems using 4 parameters"""

    def __init__(self, euler=vl.toVector(0.0, 0.0, 0.0)):
        """Quaternion is initiated by Euler angles
        the angles are given in radians um.sing ZYX-convention
        """
        phi, theta, psi = vl.toValue(euler)

        ph2 = phi / 2
        th2 = theta / 2
        ps2 = psi / 2

        q0 = m.cos(ph2) * m.cos(th2) * m.cos(ps2) + m.sin(ph2) * m.sin(th2) * m.sin(ps2)
        q1 = m.sin(ph2) * m.cos(th2) * m.cos(ps2) - m.cos(ph2) * m.sin(th2) * m.sin(ps2)
        q2 = m.cos(ph2) * m.sin(th2) * m.cos(ps2) + m.sin(ph2) * m.cos(th2) * m.sin(ps2)
        q3 = m.cos(ph2) * m.cos(th2) * m.sin(ps2) - m.sin(ph2) * m.sin(th2) * m.cos(ps2)

        self.values = vl.toVector(q0, q1, q2, q3)

    def __str__(self):
        q0, q1, q2, q3 = vl.toValue(self.values)
        return "q0: {:2.3f}, q1: {:2.3f}, q2: {:2.3f}, q3: {:2.3f}".format(
            q0, q1, q2, q3
        )

    def __mul__(self, value):
        """multiplicates self with another Quaternionen combining both rotations
        return is a new Quaternion-object
        """
        new_quat = Quaternion()
        if isinstance(value, Quaternion):
            new_quat.values = vl.mvMultiplication(self.values, value.values)
            return new_quat
        elif isinstance(value, (int, np.long, float)):
            print("scalar multiplication is not implemented yet")

    def getRotationMatrix(self):
        """creates the 3x3 rotation matrix from quaternion parameters
        represents the same relation between coordinate systems
        return a numpy.matrix
        """
        q0, q1, q2, q3 = vl.toValue(self.values)

        r11 = q0**2 + q1**2 - q2**2 - q3**2
        r22 = q0**2 - q1**2 + q2**2 - q3**2
        r33 = q0**2 - q1**2 - q2**2 + q3**2
        r12 = 2 * (q1 * q2 - q0 * q3)
        r13 = 2 * (q1 * q3 + q0 * q2)
        r23 = 2 * (q2 * q3 - q0 * q1)
        r21 = 2 * (q1 * q2 + q0 * q3)
        r31 = 2 * (q1 * q3 - q0 * q2)
        r32 = 2 * (q2 * q3 + q0 * q1)

        return np.matrix([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])

    def getEulerAngles(self):
        """calculates Euler angles from the current Quaternion
        result is given in a 3x1 vector in radians
        """

        q0, q1, q2, q3 = vl.toValue(self.values)

        try:
            phi = m.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1**2 + q2**2))
            st = 2 * (q0 * q2 - q3 * q1)
            st = 1 if st > 1 else st  # gimbal lock
            st = -1 if st < -1 else st
            theta = m.sin(st)
            psi = m.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2**2 + q3**2))
        except ValueError:
            raise ValueError("Quaternion is invalid", q0, q1, q2, q3)

        return vl.toVector(phi, theta, psi)

    def update(self, rotationRate, DT):
        """updates the quaternion via the rotation of the last period
        the rotation rate is a 3x1 vector - wx, wy, wz
        approximated quaternion differential equation
        """
        w = rotationRate * DT
        wx, wy, wz = vl.toValue(w)
        norm = m.hypot(wx, wy, wz)

        # series expansion
        r1 = 1 - (1 / 8) * norm**2 + (1 / 384) * norm**4 - (1 / 46080) * norm**6
        factor = (
            0.5 - (1 / 48) * norm**2 + (1 / 3840) * norm**4 - (1 / 645120) * norm**6
        )
        r234 = w * factor
        r = np.insert(r234, 0, r1)

        self.values = vl.mvMultiplication(self.values, r.transpose())

    def vecTransformation(self, vector):
        """transformation via quaternion like q . vector . q*
        the vector has the dimension 3x1
        return a 3x1 vector
        """
        vector = np.insert(vector, 0, 0)
        vector = vector.transpose()

        f1 = vl.mvMultiplication(self.values, vector)

        conjQuat = self.getConjugatedQuaternion()
        res = vl.mvMultiplication(f1, conjQuat.values)
        return res[1:4]

    def getConjugatedQuaternion(self):
        """returns the conjugated quaternion"""
        conjQuat = Quaternion()
        q0, q1, q2, q3 = vl.toValue(self.values)
        conjQuat.values = vl.toVector(q0, -q1, -q2, -q3)
        return conjQuat


def main():
    q = Quaternion()
    q2 = Quaternion()
    z = q * q2
    print(z)


if __name__ == "__main__":
    main()

    #TODO: move to quaternion.py
# def mvMultiplication(vector1, vector2):
#     """np.matrix-vector multiplication
#     returns a 4x1 vector
#     """
#     a, b, c, d = toValue(vector1)
#     return (
#         np.matrix([[a, -b, -c, -d], [b, a, -d, c], [c, d, a, -b], [d, -c, b, a]])
#         * vector2
#     )