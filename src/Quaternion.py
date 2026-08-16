import veclib as vl
import math as m
import numpy as np
import geolib as gl

class Quaternion(np.ndarray):
    """Derived class for handling 4x1-arrays"""

    def __new__(cls, phi=0, theta=0, psi=0, info=None):
        """Quaternion is constructed from Euler angles. The angles are given in radians using ZYX-convention
        """
        q0, q1, q2, q3 = cls._euler2quaternion(phi, theta, psi)

        # create a new instance as a column vector
        obj = np.asarray(list(map(float, [q0, q1, q2, q3]))).reshape(-1,1).view(cls)
        obj.info = info # custom metadata
        return obj

    # 2. Alternative Constructor Option
    @classmethod
    def from_list(cls, array, info=None):
        # view-cast it into our subclass
        obj = np.asarray(list(map(float, array))).reshape(-1,1).view(cls)
        # Attach the metadata
        obj.info = info
        return obj

    # 3. Alternative Constructor Option
    @classmethod
    def from_array(cls, array, info=None):
        # view-cast it into our subclass
        obj = array.reshape(-1,1).view(cls)
        # Attach the metadata
        obj.info = info
        return obj

    # 4. Alternative Constructor Option
    @classmethod
    def from_acceleration_magnetic(cls, acc, mag, info=None):
        earthParam = gl.Earth()
        ax, ay, az = acc()
        mx, my, mz = mag()
        # sanity check
        if m.isclose(m.hypot(ax, ay, az), 0.0, abs_tol=0.001):
            raise ValueError("Acceleration is not significant")
        if m.isclose(m.hypot(mx, my, mz), 0.0, abs_tol=0.001):
            raise ValueError("MagneticFlux is not significant")

        # calculate roll and pitch from acceleration
        phi = -m.atan2(ay, -az)
        theta = m.asin(ax / earthParam.g)

        # transformation to horizontal coordinate system - psi = 0
        q = Quaternion(phi, theta, 0.0)
        mHor = q.vecTransformation(mag)
        mxh, myh, _ = mHor()

        psi = m.atan2(myh, mxh) - earthParam.declination
        q0, q1, q2, q3 = cls._euler2quaternion(phi, theta, psi)

        # create a new instance as a column vector
        obj = np.asarray(list(map(float, [q0, q1, q2, q3]))).reshape(-1,1).view(cls)
        obj.info = info # custom metadata
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        # copies attributes from the original object to the new one
        self.info = getattr(obj, 'info', None)

    def __call__(self):
        return self[0,0], self[1,0], self[2,0], self[3,0]

    def __str__(self):
        q0, q1, q2, q3 = self()
        return "q0: {:2.3f}, q1: {:2.3f}, q2: {:2.3f}, q3: {:2.3f}".format(q0, q1, q2, q3)

    def __mul__(self, other):
        """multiplication operator for quaternion multiplication
        https://de.mathworks.com/help/aeroblks/quaternionmultiplication.html
        """
        a, b, c, d = self()
        res = np.dot(np.array([[a, -b, -c, -d], [b, a, -d, c], [c, d, a, -b], [d, -c, b, a]]), other)
        return Quaternion.from_array(res)

    def _euler2quaternion(phi, theta, psi):
        """https://www.firgelliauto.com/blogs/engineering-calculators/euler-angle-to-quaternion-converter
        """
        #find half angles
        phBy2 = phi / 2.0     #roll
        thBy2 = theta / 2.0   #pitch
        psBy2 = psi / 2.0     #yaw

        cosPhBy2 = m.cos(phBy2)
        sinPhBy2 = m.sin(phBy2)
        cosThBy2 = m.cos(thBy2)
        sinThBy2 = m.sin(thBy2)
        cosPsBy2 = m.cos(psBy2)
        sinPsBy2 = m.sin(psBy2)

        q0 = cosPhBy2 * cosThBy2 * cosPsBy2 + sinPhBy2 * sinThBy2 * sinPsBy2
        q1 = sinPhBy2 * cosThBy2 * cosPsBy2 - cosPhBy2 * sinThBy2 * sinPsBy2
        q2 = cosPhBy2 * sinThBy2 * cosPsBy2 + sinPhBy2 * cosThBy2 * sinPsBy2
        q3 = cosPhBy2 * cosThBy2 * sinPsBy2 - sinPhBy2 * sinThBy2 * cosPsBy2
        return q0, q1, q2, q3

    def asRotationMatrix(self):
        """creates the 3x3 rotation matrix from quaternion parameters
        represents the same relation between coordinate systems
        https://www.firgelliauto.com/es/blogs/engineering-calculators/quaternion-to-rotation-matrix-calculator
        """
        q0, q1, q2, q3 = self()

        q0_2 = q0**2
        q1_2 = q1**2
        q2_2 = q2**2
        q3_2 = q3**2

        r11 = q0_2 + q1_2 - q2_2 - q3_2
        r22 = q0_2 - q1_2 + q2_2 - q3_2
        r33 = q0_2 - q1_2 - q2_2 + q3_2
        r12 = 2 * (q1 * q2 - q0 * q3)
        r13 = 2 * (q1 * q3 + q0 * q2)
        r23 = 2 * (q2 * q3 - q0 * q1)
        r21 = 2 * (q1 * q2 + q0 * q3)
        r31 = 2 * (q1 * q3 - q0 * q2)
        r32 = 2 * (q2 * q3 + q0 * q1)

        return np.array([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])

    def asEulerAngles(self):
        """calculates Euler angles from the current Quaternion
        result is given in a 3x1 vector in radians
        """

        q0, q1, q2, q3 = self()

        try:
            phi = m.atan2(2.0 * (q0 * q1 + q2 * q3), 1.0 - 2.0 * (q1**2 + q2**2))
            st = 2.0 * (q0 * q2 - q3 * q1)
            st = 1.0 if st > 1.0 else st  # gimbal lock
            st = -1.0 if st < -1.0 else st
            theta = m.sin(st)
            psi = m.atan2(2.0 * (q0 * q3 + q1 * q2), 1.0 - 2.0 * (q2**2 + q3**2))
        except ValueError:
            raise ValueError("Quaternion is invalid", self())

        return vl.Vector(phi, theta, psi) #TODO make this a euler class

    def update(self, rotationRate, dt):
        """updates the quaternion via the rotation of the last period
        the rotation rate is a 3x1 vector - wx, wy, wz
        approximated quaternion differential equation
        """
        w = rotationRate * dt
        wx, wy, wz = w()
        norm = m.hypot(wx, wy, wz)

        # series expansion
        norm2 = norm**2
        norm4 = norm**4
        norm6 = norm**6
        r1 = 1.0 - (1.0 / 8.0) * norm2 + (1.0 / 384.0) * norm4 - (1.0 / 46080.0) * norm6
        factor = (0.5 - (1.0 / 48.0) * norm2 + (1.0 / 3840.0) * norm4 - (1.0 / 645120.0) * norm6)
        r234 = w * factor
        r = np.insert(r234, 0, r1)
        res = self * Quaternion.from_array(r)

        self[range(4),0] = res[range(4),0]

    def vecTransformation(self, vector):
        """transformation via quaternion like q . vector . q*
        the vector has the dimension 3x1
        return a 3x1 vector
        """
        vector = np.insert(vector, 0, 0)
        vector = Quaternion.from_array(vector)

        # quaternion multiplication
        res = self * vector * self.getConjugatedQuaternion()
        return vl.Vector.from_array(res[1:4])

    def getConjugatedQuaternion(self):
        """returns the conjugated quaternion"""
        q0, q1, q2, q3 = self()
        return Quaternion.from_list([q0, -q1, -q2, -q3])