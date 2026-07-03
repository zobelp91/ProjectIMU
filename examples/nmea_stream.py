import pynmea2, time
import veclib as vl
import Position as pos
import geolib as gl
import Velocity as vel
import numpy as np

msg = pynmea2.parse("$GPGGA,132525.000,5233.3292,N,01320.6101,E,2,07,1.38,25.9,M,44.7,M,0000,0000*52")
# msg = pynmea2.parse("GPGSA,A,3,14,12,32,29,24,25,31,,,,,,2.67,1.38,2.29*0D")
print('Time: {:} Lat: {:3.4f} Lon: {:3.4f} H: {:3.4f}'.format(msg.timestamp, msg.latitude,
                                                               msg.longitude, float(msg.altitude) + float(msg.geo_sep)))

p0 = pos.EllipsoidPosition(np.deg2rad(vl.toVector(msg.latitude,msg.longitude,float(msg.altitude) + float(msg.geo_sep))))
p0 = gl.ell2xyz(p0) #xyz

t0 = msg.timestamp
t0 = (t0.hour*3600 + t0.minute*60 + t0.second - 1)

with open('D:\Masterarbeit\Code\Eclipse\ProjectIMU\data\\UltimateGPS\GPRMC_stream.csv','r') as fread:
    streamreader = pynmea2.NMEAStreamReader(fread, 'ignore')
    while 1:
        for msg in streamreader.next():
            if msg.sentence_type == 'GGA':
                he = float(msg.altitude) + float(msg.geo_sep) #m
                lat = np.deg2rad(msg.latitude)
                lon = np.deg2rad(msg.longitude)
                p = pos.EllipsoidPosition(vl.toVector(lat,lon,he))   
                p = gl.ell2xyz(p)
                dp = p - p0
                p0 = p
                t = msg.timestamp
                t = (t.hour*3600 + t.minute*60 + t.second)                    
                dt = (t-t0)
                t0 = t
                v = dp/abs(dt)
                v = vel.Velocity(v)
                p = pos.Position(p)
                print(p, v, msg.timestamp)
            time.sleep(0.1)