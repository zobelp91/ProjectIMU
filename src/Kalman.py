import math as m
import numpy as np

import geolib as gl

# sensor specifications
GYRO_NOISE = np.deg2rad(0.03)           # rad
GYROBIAS_NOISE = GYRO_NOISE * 0.01      # rad/s
ACCEL_NOISE = 7.0                       # m/s2
ACCELBIAS_NOISE = ACCEL_NOISE * 0.01    # m/s2
MAGNETO_NOISE = 4.0                     # muT
POSITION_NOISE = 3.0                    # m
VELOCITY_NOISE = 0.1                    # m/s

# state init values
POSITION_INIT = 4.3                     # m
VELOCITY_INIT = 1e-2                    # m/s
ATTITUDE_INIT = 0.5                     # rad
ACCELBIAS_INIT = 1e-6                   # m/s2
GYROBIAS_INIT = 0.001                   # rad/s

class EKF():
    def __init__(self, numStates):
        self.numStates = numStates
        self.errorState = np.zeros((numStates, 1))
        self.Q = np.zeros((numStates, numStates))
        self.P = np.zeros((numStates, numStates))
        self.R = np.zeros((numStates, numStates))
    
    def timeUpdate(self, B, F, dt):
        # discretisation
        f = np.eye(*F.shape) + F * dt  # transition-matrix f
        self.P = f @ self.P @ f.T + B @ self.Q @ B.T * dt 

    def measUpdate(self, H, innov):
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)

        self.errorState = self.errorState + K @ innov
        self.P = self.P - K @ H @ self.P

    def resetState(self):
        self.errorState = np.zeros((self.numStates, 1))

class AttitudeEstimator(EKF):
    """6 state Kalman Filter using accelerometer and magnetometer measurements to compensate bearing-error und gyro-bias
    closed-loop-Error-state
    """

    def __init__(self):
        """class contains current state(a priori/a posteriori)
        and system-noise and measurement-noise
        vc-matrix P is initialised as known through prior initialisation
        """
        # attittude error (3) + gyro-bias (3)
        super().__init__(6)
        self.Q = getVarianceMatrix([GYRO_NOISE]  * 3 + [GYROBIAS_NOISE] * 3)
        self.R = getVarianceMatrix([ACCEL_NOISE] * 3 + [MAGNETO_NOISE]  * 3)
        self.P = getVarianceMatrix([ATTITUDE_INIT]   * 3 + [GYROBIAS_INIT ] * 3)

    def timeUpdate(self, quaternion, dt):
        """requires current quaternion to compute linearized system-modell at point x0
        state a priori is propagated w/o noise
        system-noise is uncorrelated
        """
        rotationMatrix = quaternion.asRotationMatrix() # derivation at point x0(current orientation)
        F = np.zeros(shape=(6, 6))
        F[0:3, 3:6] = rotationMatrix    # Jacobi-matrix

        B = np.zeros(shape=(6, 6))      # influence-matrix of noise
        B[0:3, 0:3] = rotationMatrix
        B[3:6, 3:6] = np.eye(3, 3)

        super().timeUpdate(B, F, dt)

    def measurementUpdate(self, acceleration, magneticField, quaternion):
        """acceleration and magneticField-measurements are needed to calculate the measurement-difference dz
        measurement-noise is uncorrelated
        measurement-matrix H is defined at x0
        """
        earthParam = gl.Earth()
        rotationMatrix = quaternion.asRotationMatrix()
        H1 = np.zeros(shape=(3, 6))
        H1[0, 1] = -earthParam.g
        H1[1, 0] = earthParam.g
        H1 = -rotationMatrix.T @ H1

        hn, he, _ = earthParam.magfield()

        H2 = np.zeros(shape=(3, 6))
        H2[0, 2] = he
        H2[1, 2] = -hn
        H2 = rotationMatrix.T @ H2
        H = np.vstack((H1, H2))

        z0 = np.vstack((
            rotationMatrix.T @ -earthParam.G,
            rotationMatrix.T @ earthParam.magfield))
        dz = np.vstack((
            acceleration, magneticField)) - z0  # z(meas) - z(calc)
        innov = dz - H @ self.errorState

        super().measUpdate(H, innov)

class PositionEstimator(EKF):
    """15 state Kalman Filter that estimates position, velocity, orientation, gyro-bias and accelerometer-bias
    based on inertial sensors and positional/velocity measurements
    closed-loop-Error-state
    """

    def __init__(self):
        """class contains current state(a priori/a posteriori)
        and system-noise and measurement-noise
        vc-matrix P is initialised as known through prior initialisation
        """
        # position error (3) + velocity error (3) + attitude error (3) + accelerometer bias (3) + gyro bias (3)
        super().__init__(15)

        self.Q = getVarianceMatrix(
              [ACCEL_NOISE] * 3
            + [GYRO_NOISE] * 3
            + [ACCELBIAS_NOISE] * 3
            + [GYROBIAS_NOISE] * 3)

        self.P = getVarianceMatrix(
              [POSITION_INIT] * 3 
            + [VELOCITY_INIT] * 3 
            + [ATTITUDE_INIT] * 3 
            + [ACCELBIAS_INIT] * 3 
            + [GYROBIAS_INIT] * 3)

        self.R = getVarianceMatrix(
              [POSITION_NOISE] * 3
            + [VELOCITY_NOISE] * 3
            + [ACCEL_NOISE] * 3
            + [MAGNETO_NOISE] * 3)

    def timeUpdate(self, acceleration, quaternion, dt):
        """requires current quaternion to compute linearized system-modell at point x0
        state a priori is propagated w/o noise
        system-noise is uncorrelated
        """
        rotationMatrix = quaternion.asRotationMatrix()  # derivation at point x0(current orientation)
        F = np.zeros(shape=(15, 15))
        subMatrix = np.zeros(shape=(3, 3))
        an, ae, ad = quaternion.vecTransformation(acceleration)()  # an_ib
        subMatrix[0, 1] = ad
        subMatrix[0, 2] = -ae
        subMatrix[1, 0] = -ad
        subMatrix[1, 2] = an
        subMatrix[2, 0] = ae
        subMatrix[2, 1] = -an
        F[0:3, 3:6] = np.eye(3, 3)
        F[3:6, 6:9] = subMatrix
        F[3:6, 9:12] = -rotationMatrix
        F[6:9, 12:15] = -rotationMatrix

        B = np.zeros(shape=(15, 12))  # influence-matrix of noise
        B[3:6, 0:3] = rotationMatrix
        B[6:9, 3:6] = rotationMatrix
        B[9:12, 6:9] = np.eye(3, 3)
        B[12:15, 9:12] = np.eye(3, 3)

        super().timeUpdate(B, F, dt)

    def measurementUpdate(
        self,
        quaternion,
        IMUposition,
        IMUvelocity,
        position,
        velocity,
        acceleration,
        magneticField):
        """if gpsAvailable is True position and velocity measurement is required
        if not measurement-Update can be done only with acceleration and magneticField measurements
        calculating only gyro-error and gyro-bias
        measurement-noise is uncorrelated
        measurement-matrix H is defined at x0
        """
        earthParam = gl.Earth()

        hn, he, _ = earthParam.magfield()
        rotationMatrix = quaternion.asRotationMatrix()

        H = np.zeros(shape=(12, 15))
        subMatrix1 = np.zeros(shape=(3, 3))
        subMatrix1[0, 1] = -earthParam.g
        subMatrix1[1, 0] = earthParam.g
        subMatrix2 = np.zeros(shape=(3, 3))
        subMatrix2[0, 2] = he
        subMatrix2[1, 2] = -hn
        H[0:6, 0:6] = np.eye(6, 6)
        H[6:9, 6:9] = -rotationMatrix.T @ subMatrix1
        H[9:12, 6:9] = rotationMatrix.T @ subMatrix2

        dz = self._getMeasurementVector(
            IMUposition,
            IMUvelocity,
            rotationMatrix,
            position,
            velocity,
            acceleration,
            magneticField)

        innov = dz - H @ self.errorState
        
        super().measUpdate(H, innov)


    def _getMeasurementVector(self, IMUpos, IMUvel, rotMatrix, pos, vel, accel, mag):
        """calculates difference between measured values and calculated values
        ellipsoidal distance has to be transformed into (N,E,D) with metric units
        """
        earthParam = gl.Earth()
        z0 = np.vstack((
                IMUpos,
                IMUvel,
                rotMatrix.T @ -earthParam.G,
                rotMatrix.T @ earthParam.magfield))
        dz = np.vstack((pos, vel, accel, mag)) - z0
        lat, _, h = IMUpos()
        Rn, Re = earthParam.curvature(lat)
        dz[0] = dz[0] * (Rn - h)
        dz[1] = dz[1] * (Re - h) * m.cos(lat)
        return dz

    def _setGainToZero(self, K):
        """set lines and columns concerning position, velocity and accel-bias to zero
        no influence on estimation
        """
        K[:, 0:6] = 0.0
        K[9:12, :] = 0.0
        K[:, 9:12] = 0.0
        K[0:6, :] = 0.0
        return K

def getVarianceMatrix(rms):
    """creates a diagonal variance matrix from a list of rms values
    """
    nn = np.power(rms, 2)
    return np.array(np.diag(nn))