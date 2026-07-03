import veclib as vl
import math as m
import matplotlib.pyplot as plt
from matplotlib.pyplot import title, xlabel, ylabel

g = 9.81
phi = 0 * m.pi / 180
theta = 1 * m.pi / 180
psi = 0 * m.pi / 180

# bw = ml.toVector((theta), -(phi), 0)  # 5degree/s
bw = ml.toVector(m.sin(phi) * m.sin(psi) + m.cos(phi) * m.sin(theta) * m.cos(psi),
            - m.sin(phi) * m.cos(psi) + m.cos(phi) * m.sin(theta) * m.sin(psi) ,
            1 - m.cos(phi) * m.cos(theta))

ba = ml.toVector(10, 10, 10)  # mg
ba_ms = ba * g / 1000

for t in range(60):

    dr1 = (1 / 6) * g * (bw) * t ** 3

    dr2 = (1 / 2) * ba_ms * t ** 2

    x, y, z = ml.toValue(dr1)

    red_dot, = plt.plot(t, x, "ro")
    blue_dot, = plt.plot(t, y, "bo")
    green_dot, = plt.plot(t, z, "go")


plt.legend([red_dot, blue_dot, green_dot], ["X-Pos", "Y-Pos", "Z-Pos"])
title('Positionsfehler durch Drehratenbias')

xlabel('Zeit in [sek]')
ylabel('Positionsfehler in [m]')
plt.show()

