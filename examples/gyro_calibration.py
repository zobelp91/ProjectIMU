import filemanager as fm
import numpy as np
import math as m

filePath = "data\\adafruit10DOF\\sample_Hubarm.csv"
# filePath = "test_sampleRate.csv"
col_gyro = range(0,4) #rad/s
col_accel = range(3,7) #-g
col_mag = range(6,10) #muT
d = fm.CSVImporter(filePath, columns=col_gyro, skip_header = 8, hasTime=True)
v = d.values*180/m.pi#*-9.80665#

start = 0
l = 45779
x = v[start:l,1]
y = v[start:l,2]
z = v[start:l,3]
i = range(start,l)

bx = np.polyfit(i,x,0)[0]
by = np.polyfit(i,y,0)[0]
bz = np.polyfit(i,z,0)[0]

trendx, _ = np.polyfit(i,x,1)
trendy, _ = np.polyfit(i,y,1)
trendz, _ = np.polyfit(i,z,1)

print("sample size : %i, during %.3f sec, sample rate : %f Hz" % (len(x), len(x)*d.sampleRate, 1/d.sampleRate))
print("bx %.9f, by %.9f, bz %.9f" % (bx, by, bz))
print("nx %f, ny %f, nz %f" % (np.std(x),np.std(y),np.std(z)))
print("trendx %.9f, trendy %.9f, trendz %.9f" % (trendx, trendy, trendz))