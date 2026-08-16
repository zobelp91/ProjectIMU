import unittest

import numpy as np
import math

from Kalman import EKF, getVarianceMatrix, AttitudeEstimator, PositionEstimator
from Quaternion import Quaternion

class KalmanTest(unittest.TestCase):
    def test_getVarianceMatrix_squares_elements(self):
        rms = [1.0, 2.0, 3.0]
        V = getVarianceMatrix(rms)
        self.assertEqual(V.shape, (3, 3))
        self.assertTrue(np.allclose(np.diag(V), np.array(rms)**2))
        self.assertTrue(np.allclose(V, np.diag(np.array(rms)**2)))

    def test_EKF_timeUpdate_applies_Q_term(self):
        ekf = EKF(2)
        ekf.P = np.zeros((2,2))
        ekf.Q = np.eye(2)
        B = np.eye(2)
        F = np.zeros((2,2))
        ekf.timeUpdate(B, F, dt=1.0)
        # with F==0, f == I and P should become B @ Q @ B.T * dt == I
        self.assertTrue(np.allclose(ekf.P, np.eye(2)))

    def test_EKF_measUpdate_updates_state_and_P(self):
        ekf = EKF(2)
        ekf.P = np.eye(2)
        ekf.R = np.zeros((2,2))
        ekf.errorState = np.zeros((2,1))
        H = np.eye(2)
        innov = np.array([[1.0],[2.0]])
        ekf.measUpdate(H, innov)
        # With P=I, R=0, H=I, gain K = I and new errorState == innov and P == 0
        self.assertTrue(np.allclose(ekf.errorState, innov))
        self.assertTrue(np.allclose(ekf.P, np.zeros((2,2))))

    def test_AttitudeEstimator_timeUpdate_runs_and_sets_P_shape(self):
        att = AttitudeEstimator()
        q = Quaternion()  # identity quaternion
        # ensure method runs without exception and P has correct shape
        att.timeUpdate(q, dt=0.1)
        self.assertEqual(att.P.shape, (6,6))
        self.assertTrue(np.isfinite(att.P).all())

    def test_PositionEstimator_setGainToZero_masks_correct_entries(self):
        pos = PositionEstimator()
        K = np.random.randn(15,15)
        K_masked = pos._setGainToZero(K.copy())
        # columns 0:6 and rows 0:6 should be zero
        self.assertTrue(np.allclose(K_masked[:, 0:6], 0.0))
        self.assertTrue(np.allclose(K_masked[0:6, :], 0.0))
        # rows 9:12 and columns 9:12 should be zero
        self.assertTrue(np.allclose(K_masked[9:12, :], 0.0))
        self.assertTrue(np.allclose(K_masked[:, 9:12], 0.0))


if __name__ == '__main__':
    unittest.main()
