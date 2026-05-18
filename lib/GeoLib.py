""" Geodetic Library
""" 
import math as m
import constants as c
import mathlib as ml

def earthCurvature(a,f,lat):
    """ calculates radius of curvature in North and East
        takes ellipsoidal parameters as argument 
    """
    e = m.sqrt(f*(2-f))
    Rn = a *((1-e**2)/(1-e**2*(m.sin(lat))**2)**(3/2))
    Re = a/m.sqrt(1-e**2*(m.sin(lat))**2)
    return Rn, Re

def ell2xyz(lat, lon, he):
    """ transformation of geographic coordinates to cartesian coordinates
        input are latitude, longitude, height in radian and meter
        returns a 3x1 vector
    """
    _, N = earthCurvature(c.GRS80_a, c.GRS80_f, lat)
    x = (N + he) * m.cos(lat)*m.cos(lon)
    y = (N + he) * m.cos(lat)*m.sin(lon)
    z = N * m.sin(lat)*(c.GRS80_b**2/c.GRS80_a**2) + he*m.sin(lat)
    return ml.toVector(x,y,z)