import constants
import geolib
import veclib as vl
import plothelper
import filemanager as fm

import Euler
import Quaternion
import Position
import Velocity
import Kalman
import Strapdown

if __name__ == "__main__":
    s = Strapdown.Strapdown()
    K = Kalman.KalmanPVO()

    # approximate values for gyro bias
    rot_mean = vl.toVector(0.0184, -0.0146, 0.003)

    accelBias = vl.toVector(0.0, 0.0, 0.0)
    acc_mean = vl.toVector(0.0, 0.0, 0.0)
    mag_mean = vl.toVector(0.0, 0.0, 0.0)

    pos_mean = s.getPosition()

    dt_mean = 0.01

    # import IMU data
    dImu = fm.ImuDataImporter("data\\adafruit10DOF\\linie_dach_imu.csv")
    dGps = fm.GpsDataImporter("data\\UltimateGPS\\linie_dach_gps.csv") 

    dIMU = fm.CSVImporter("data\\adafruit10DOF\\linie_dach_imu.csv", columns=range(0, 13), skip_header=7, hasTime=True)
    # accelArray, rotationArray, magneticArray = Strapdown.convArray2IMU(dIMU.values)
    # tIMU, deltaArray = Strapdown.convArray2time(dIMU.values)

    # # import GPS
    # dGPS = fm.CSVImporter(
    #     "data\\UltimateGPS\\linie_dach_gps.csv", skip_header=1, columns=range(7)
    # )
    # posArray, velArray = Strapdown.convArray2PV(dGPS.values)
    # tGPS, _ = Strapdown.convArray2time(dGPS.values)
    # PDOP = Strapdown.convArray2err(dGPS.values)
