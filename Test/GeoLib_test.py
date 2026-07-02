import unittest
from geolib import earthCurvature, ell2xyz
from math import pi
from Position import EllipsoidPosition
from veclib import toVector, toValue
from numpy import deg2rad

class GeoLib_test(unittest.TestCase):
    def test_earthCurvature(self):
        a = 6378137.0
        f = 1/298.257223563
        Rn, Re = earthCurvature(a,f,pi/4)
        self.assertAlmostEqual(Re, 6388838.2901, delta=0.0001)
        self.assertAlmostEqual(Rn, 6367381.8156, delta=0.0001)
        
    def test_ell2xyz(self):
        llh = EllipsoidPosition(deg2rad(toVector(52.52,13.40,0.)))
        xyz = ell2xyz(llh) 
        x,y,z = toValue(xyz)
        self.assertAlmostEqual(x, 3783323.72435, delta = 0.0001)
        self.assertAlmostEqual(y, 901314.84651, delta = 0.0001)
        self.assertAlmostEqual(z, 5038219.09955, delta = 0.0001)
        
if __name__ == '__main__':
    unittest.main() 