import unittest
import filemanager as fm


class filemanager_test(unittest.TestCase):
    # IMU files (10Hz)
    def test_10min_calib_360(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\10min_calib_360.csv"))

    def test_1hr_Bias_stability_fast(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\1hr_Bias_stability_fast.csv"))

    def test_20min_sample(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\20min_sample.csv"))

    def test_40min_mag_fixed(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\40min_mag_fixed.csv"))

    def test_linie_dach_imu(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\linie_dach_imu.csv"))

    def test_sample_brueckenmodell(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\sample_brueckenmodell.csv"))

    def test_sample_dach_imu(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\sample_dach_imu.csv"))

    def test_sample_Hubarm(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\sample_Hubarm.csv"))

    def test_sample_imu_beuth_0801(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\10hz\\sample_imu_beuth_0801.csv"))

    # IMU files (100Hz)
    def test_10min_calib_wTilt(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\100hz\\10min_calib_wTilt.csv"))

    def test_gyroBias_wTilt(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\100hz\\gyroBias_wTilt.csv"))
    
    def test_sample_gyroBias(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\100hz\\sample_gyroBias.csv"))

    def test_slowTilt(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\100hz\\slowTilt.csv"))

    def test_Tilt180_w100Hz(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\100hz\\Tilt180_w100Hz.csv"))

    def test_Tilt_w100Hz(self):
        self._assertImuDataOk(fm.ImuDataImporter("data\\adafruit10DOF\\100hz\\Tilt_w100Hz.csv"))

    # GPS files
    def test_ultimate_20min_sample(self):
        self._assertGpsDataOk(fm.GpsDataImporter("data\\UltimateGPS\\20min_sample.csv"))

    def test_ultimate_linie_dach_gps(self):
        self._assertGpsDataOk(fm.GpsDataImporter("data\\UltimateGPS\\linie_dach_gps.csv"))

    def test_ultimate_sample_dach_gps(self):
        self._assertGpsDataOk(fm.GpsDataImporter("data\\UltimateGPS\\sample_dach_gps.csv"))

    def test_ultimate_sample_gps_beuth_0801(self):
        self._assertGpsDataOk(fm.GpsDataImporter("data\\UltimateGPS\\sample_gps_beuth_0801.csv"))


    def _assertImuDataOk(self, data):
        self.assertGreater(data.length, 0)
        self.assertAlmostEqual(data.dt, 0.010, delta=0.01)

    def _assertGpsDataOk(self, data):
        self.assertGreater(data.length, 0)
        self.assertAlmostEqual(data.dt, 1, delta=0.1)


if __name__ == "__main__":
    unittest.main()
