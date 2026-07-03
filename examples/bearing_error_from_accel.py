import math as m
import constants as c
import veclib as vl

ba = vl.toVector(10, 10, 10)  # mg
ba_ms = ba * c.g / 1000
bx, by, bz = vl.toValue(ba_ms)

s_phi = -bx / c.g
print("Lagefehler phi = ", s_phi * 180 / m.pi, "deg")
s_theta = bz / c.g
print("Lagefehler theta = ", s_theta * 180 / m.pi, "deg")