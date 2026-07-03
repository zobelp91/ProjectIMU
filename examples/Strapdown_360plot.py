""" class Strapdown generates bearing, velocity and position from 9 degree IMU readings
"""
import Euler as eu
import veclib as vl
import Position as pos
import Quaternion as quat
import Velocity as vel
import Kalman as k
import filemanager as fm
import plothelper as ph
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from datetime import datetime 
import numpy as np
import math as m

class Strapdown(object):
    def __init__(self):
        """ creates Strapdown object which includes the current bearing, velocity and position
            bearing (phi, theta, psi) in degrees, velocity (ax, ay, az) in m/s, position (x,y,z) in m
        """             
        self.quaternion = Quaternion()
        self.velocity = Velocity()  # vector (if known)
        self.position = Position()  # or GNSS.getPos()
        # toVector(52.521918/180*pi, 13.413215\180*pi, 100.)
        self.isInitialized = False
        
    def Initialze(self, acceleration, magneticField):
        self.quaternion = Quaternion(Euler(acceleration,magneticField).values)
        self.isInitialized = True
        #self.position = (toVector(n,e,d)) if GNSS measurement is icluded  
        
    def getOrientation(self):
        return self.quaternion.getEulerAngles()
    
    def getVelocity(self):
        return self.velocity.values
    
    def getPosition(self):
        return self.position.values
    
def main():
    s = Strapdown()
    K = Kalman()
    rot_mean = toVector(0.,0.,0.)
    acc_mean = toVector(0.,0.,0.)
    mag_mean = toVector(0.,0.,0.)
    
    # read sensors
    filePath = "data\\adafruit10DOF\\10min_calib_360.csv"
    d = CSVImporter(filePath, columns=range(0,10), skip_header = 7, hasTime = True)
    accelArray, rotationArray, magneticArray = convArray2IMU(d.values)
    
    # variable sample rate test
    time = d.values[:,0]
    diff = ([x - time[i - 1] for i, x in enumerate(time)][1:])
    diff.insert(0,0.0134981505504)
    
    # realtime 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.ion()
    
    start = datetime.now()
    phi_list = []
    theta_list = []
    psi_list = []
    for i in range(1,int(47999)):   #62247
        dt = diff[i]
        # for 10 - 15 minutes
        if not s.isInitialized:
            rot_mean = runningAverage(rot_mean, rotationArray[:,i], 1/i)
            acc_mean = runningAverage(acc_mean, accelArray[:,i], 1/i)
            mag_mean = runningAverage(mag_mean, magneticArray[:,i], 1/i)
            if i >= 45500:#100*60*7.5 :    
                s.Initialze(acc_mean, mag_mean)
                gyroBias = rot_mean#toVector(0.019686476,-0.014544547,0.002910090)
        
                print('STRAPDOWN INITIALIZED with %i values\n' % (i,))    
                print('Initial bearing\n', s.getOrientation()*180/pi)
                print('Initial velocity\n', s.getVelocity())
                print('Initial position\n', s.getPosition())
                print('Initial gyro Bias\n', gyroBias*180/pi)
        else:
            if i%10 == 0: # plot area
                plt.cla()
                fig.texts = []
                plot3DFrame(s,ax)
                plt.draw()
                plt.pause(0.01)

            phi,theta,psi = rad2deg(s.getOrientation()) 
            phi_list.append(phi)
            theta_list.append(theta)
            psi_list.append(psi)
               
            acceleration = accelArray[:,i]
            rotationRate = rotationArray[:,i]-gyroBias
            magneticField = magneticArray[:,i]
            
            s.quaternion.update(rotationRate, dt)
            s.velocity.update(acceleration, s.quaternion, dt)
            s.position.update(s.velocity, dt)
                
            K.timeUpdate(s.quaternion, dt)
#             if i%10 == 0:
#                 K.measurementUpdate(acceleration, magneticField, s.quaternion)
#                                          
#                 bearingOld = s.getOrientation()        
#                 errorQuat = Quaternion(K.bearingError)
#                 s.quaternion *= errorQuat
#                 #s.quaternion.update(K.bearingError/DT) #angle = rate*DT
# #                 print(s.quaternion.values)
#                 bearingNew = s.getOrientation()
# #                 print("Differenz zwischen neuer und alter Lage \n",rad2deg(bearingNew-bearingOld))
#                 gyroBias = gyroBias+K.gyroBias 
#                 K.resetState()
    
    print("Differenz zwischen x Bias End-Start: %E" % rad2deg(gyroBias[0]-rot_mean[0]))  
    print("Differenz zwischen y Bias End-Start: %E" % rad2deg(gyroBias[1]-rot_mean[1]))
    print("Differenz zwischen z Bias End-Start: %E\n" % rad2deg(gyroBias[2]-rot_mean[2]))      
    print("RMS_dphi = %f deg" % rad2deg(sqrt(K.P[0,0])))
    print("RMS_dthe = %f deg" % rad2deg(sqrt(K.P[1,1])))
    print("RMS_dpsi = %f deg" % rad2deg(sqrt(K.P[2,2])))
    print("RMS_bx = %f deg/s" % rad2deg(sqrt(K.P[3,3])))
    print("RMS_by = %f deg/s" % rad2deg(sqrt(K.P[4,4])))
    print("RMS_bz = %f deg/s\n" % rad2deg(sqrt(K.P[5,5])))
    print('final orientation\n', s.getOrientation()*180/pi)
    end = datetime.now()
    diff = end - start
    print('Time needed = ', diff.total_seconds())
    print("RMS_phi = %f deg, max = %f, min = %f\n" % (std(phi_list),max(phi_list), min(phi_list)))
    print("RMS_theta = %f deg, max = %f, min = %f\n" % (std(theta_list),max(theta_list), min(theta_list)))
    print("RMS_psi = %f deg, max = %f, min = %f\n" % (std(psi_list),max(psi_list), min(psi_list)))
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

def convArray2IMU(array): #arduino 10DOF
    acceleration = toVector(array[:,4],array[:,5],array[:,6])*-9.80665
    rotationRate = toVector(array[:,1],array[:,2],array[:,3])#*pi/180
    magneticField = toVector(array[:,7],array[:,8],array[:,9])*1
    return acceleration.transpose(), rotationRate.transpose(), magneticField.transpose()

if __name__ == "__main__":
    main()         
        

    
        
