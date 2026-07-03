import numpy as np
import matplotlib.pyplot as plt

import filemanager as fm
import plothelper as ph
import veclib as vl

import Euler as eu
import Position as pos
import Quaternion as quat
import Velocity as vel
import Kalman as k

# import simplekml


class Strapdown(object):
    """class Strapdown generates bearing, velocity and position from 9 degree IMU"""

    def __init__(self):
        """creates Strapdown object which includes the current bearing, velocity and position
        bearing (phi, theta, psi) in degrees, velocity (ax, ay, az) in m/s, position (x,y,z) in m
        """
        self.quaternion = quat.Quaternion()
        self.velocity = vel.Velocity()
        self.position = (
            pos.EllipsoidPosition()
        )  # navigation system position with Position()
        self.isInitialized = False

    def Initialze(self, acceleration, magneticField, position):
        """calculates attitutde and heading
        sets position to given position vector
        """
        self.quaternion = quat.Quaternion(eu.Euler(acceleration, magneticField).values)
        self.position.values = position
        self.isInitialized = True

    def getOrientation(self):
        return self.quaternion.getEulerAngles()  # vector of euler angles in rad

    def getVelocity(self):
        return self.velocity.values

    def getPosition(self):
        return self.position.values


def main():
    """demo function for measurements saved as CSV file"""
    s = Strapdown()
    K = k.KalmanPVO()
    #     kml = simplekml.Kml()

    rot_mean = vl.toVector(
        0.018461137, -0.01460140625, 0.002765854
    )  # approximate values for gyro bias
    accelBias = vl.toVector(0.0, 0.0, 0.0)
    acc_mean = vl.toVector(0.0, 0.0, 0.0)
    mag_mean = vl.toVector(0.0, 0.0, 0.0)
    pos_mean = s.getPosition()
    dt_mean = 0.01

    # import IMU
    filePath = "data\\adafruit10DOF\\linie_dach_imu.csv"
    dIMU = fm.CSVImporter(filePath, columns=range(0, 13), skip_header=7, hasTime=True)
    accelArray, rotationArray, magneticArray = convArray2IMU(dIMU.values)
    tIMU, deltaArray = convArray2time(dIMU.values)

    # import GPS
    dGPS = fm.CSVImporter(
        "data\\UltimateGPS\\linie_dach_gps.csv", skip_header=1, columns=range(7)
    )
    posArray, velArray = convArray2PV(dGPS.values)
    tGPS, _ = convArray2time(dGPS.values)
    #     PDOP = convArray2err(dGPS.values)

    j = 1  # index for GPS measurements
    for i in range(100, 58164):  # index for IMU measurements
        dt_mean = vl.runningAverage(dt_mean, deltaArray[i], 1)

        # Initialzation
        if not s.isInitialized:
            rot_mean = vl.runningAverage(rot_mean, rotationArray[:, i], 1 / (i + 1))
            acc_mean = vl.runningAverage(acc_mean, accelArray[:, i], 1 / i)
            mag_mean = vl.runningAverage(mag_mean, magneticArray[:, i], 1 / i)
            if tIMU[i] >= tGPS[j]:
                pos_mean = vl.runningAverage(pos_mean, posArray[:, j], 1 / j)
                j += 1
            if i >= 48133:  # for 10 - 15 minutes
                s.Initialze(acc_mean, mag_mean, pos_mean)
                gyroBias = rot_mean

                print(
                    "STRAPDOWN INITIALIZED with %i samples and %i position measurements\n"
                    % (i, j)
                )
                e = eu.Euler()
                e.values = s.getOrientation()
                print("Initial orientation\n", e)
                print("Initial velocity\n", s.velocity)
                print("Initial position\n", s.position)
                e.values = gyroBias
                print("Initial gyro bias\n", e)

        else:
            ###################################### plot area
            if i % 10 == 0:
                plt.figure(1)
                #                 lat, lon, h = s.getPosition()
                #                 plt.plot(i, h, 'ro')
                #                 plt.plot(lon,lat, 'go')
                #                 plotVector(i,s.getVelocity())
                ph.plotVector(i, np.rad2deg(np.rad2deg(s.getOrientation())))
            #                 kml.newpoint(name=str(i), coords=[(rad2deg(lon), rad2deg(lat), h)])
            ######################################

            acceleration = accelArray[:, i] - accelBias
            rotationRate = rotationArray[:, i] - gyroBias
            magneticField = magneticArray[:, i]

            s.quaternion.update(rotationRate, dt_mean)
            s.velocity.update(acceleration, s.quaternion, dt_mean)
            s.position.update(s.velocity, dt_mean)

            K.timeUpdate(acceleration, s.quaternion, dt_mean)
            try:
                gpsAvailable = tIMU[i] >= tGPS[j]
            except:  # end of GPS file reached
                gpsAvailable = False

            #             if 55450 <= i <= 56450: # simulated GPS outage
            #                 gpsAvailable = False
            #
            if (
                gpsAvailable or i % 10 == 0
            ):  # doing either complete update or gyro error and bias update
                if gpsAvailable:
                    pos = posArray[:, j]
                    vel = velArray[:, j]
                    j += 1
                else:
                    pos = vl.toVector(0.0, 0.0, 0.0)
                    vel = vl.toVector(0.0, 0.0, 0.0)
                K.measurementUpdate(
                    s.quaternion,
                    s.position,
                    s.velocity,
                    pos,
                    vel,
                    acceleration,
                    magneticField,
                    gpsAvailable,
                )
                errorQuat = quat.Quaternion(K.oriError)
                s.quaternion = errorQuat * s.quaternion
                s.position.correct(K.posError)
                s.velocity.correct(K.velError)
                gyroBias = gyroBias + K.gyrError
                accelBias = accelBias - K.accError
                K.resetState()

    e.values = s.getOrientation()
    print("\nFinal orientation\n", e)
    print("Final position\n", s.position)

    print("Average sampling rate: {:3.1f}".format(1.0 / dt_mean))
    #         kml.save("export\\linie_dach.kml")
    plt.show()


# def convArray2IMU(array): #MYSTREAM APP
#     acceleration = toVector(array[:,1],array[:,2],array[:,3]+3.05)
#     rotationRate = toVector(array[:,4],array[:,5],array[:,6])*pi/180
#     magneticField = toVector(array[:,7],-array[:,8],array[:,9])
#     return acceleration.transpose(), rotationRate.transpose(), magneticField.transpose()

# def convArray2IMU(array): #ROJEK IMU
#     acceleration = toVector(array[:,3],array[:,4],array[:,5])*-g
#     rotationRate = toVector(array[:,0],array[:,1],array[:,2])*pi/180
#     magneticField = toVector(array[:,6],array[:,7],array[:,8])*100
#     return acceleration.transpose(), rotationRate.transpose(), magneticField.transpose()


def convArray2IMU(array):  # adafruit 10DOF
    acceleration = vl.toVector(array[:, 4], array[:, 5], array[:, 6]) * -9.80665
    rotationRate = vl.toVector(array[:, 1], array[:, 2], array[:, 3])
    magneticField = vl.toVector(array[:, 7], array[:, 8], array[:, 9])
    return acceleration.T, rotationRate.T, magneticField.T


def convArray2time(array):
    t = array[:, 0]
    delta = np.diff(t)
    delta = np.insert(delta, 0, delta[0])
    return t.T, delta.T


def convArray2PV(array):
    pos = vl.toVector(
        np.deg2rad(array[:, 1]), np.deg2rad(array[:, 2]), array[:, 3]
    )  # rad rad m
    vel = vl.toVector(array[:, 4], array[:, 6], array[:, 6])  # ms
    return pos.T, vel.T


def convArray2euler(array):
    """if data includes euler angles"""
    pose = vl.toVector((array[:, 10]), (array[:, 11]), (array[:, 12]))
    return pose.T


def convArray2err(array):
    """if data includes errors"""
    err = vl.toVector(array[:, 8], array[:, 9], array[:, 10])
    return err.T


if __name__ == "__main__":
    main()
