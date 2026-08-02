import unittest
import math as m
import numpy as np
import geolib as gl


class GeoLibTest(unittest.TestCase):
    """Test cases for the Earth class"""

    def setUp(self):
        """Set up test fixtures"""
        self.earth = gl.Earth()

    def test_earth_initialization(self):
        """Test Earth class initialization with correct parameter values

        Verifies that all Earth parameters are properly initialized with
        expected values for Berlin, Germany.
        """
        # Test gravity acceleration
        self.assertAlmostEqual(self.earth.g, 9.81262, places=5)

        # Test that G is a Vector with correct shape
        self.assertIsInstance(self.earth.G, np.ndarray)
        self.assertEqual(self.earth.G.shape, (3, 1))

        # Test G vector components (should be [0, 0, g])
        g_components = self.earth.G()
        self.assertAlmostEqual(float(g_components[0]), 0, places=5)
        self.assertAlmostEqual(float(g_components[1]), 0, places=5)
        self.assertAlmostEqual(float(g_components[2]), 9.81262, places=5)

        # Test magnetic field is a Vector
        self.assertIsInstance(self.earth.magfield, np.ndarray)
        self.assertEqual(self.earth.magfield.shape, (3, 1))

        # Test declination is in radians and reasonable for Berlin
        # 3° 40' 34" ≈ 0.0636 radians
        expected_declination = np.deg2rad(3.0 + 40.0/60.0 + 34.0/3600.0)
        self.assertAlmostEqual(self.earth.declination, expected_declination, places=5)

        # Test GRS80 ellipsoid parameters
        self.assertAlmostEqual(self.earth.GRS80_a, 6378137.0, places=1)
        self.assertAlmostEqual(self.earth.GRS80_b, 6356752.314, places=1)
        self.assertGreater(self.earth.GRS80_f, 0)
        self.assertLess(self.earth.GRS80_f, 0.01)  # Flattening should be small

    def test_curvature_at_equator(self):
        """Test radius of curvature at the equator

        At the equator (lat=0), the radius of curvature in the North direction
        should equal the semi-minor axis radius, and in the East direction
        should equal the semi-major axis minus a small amount.
        """
        lat_equator = 0.0  # Latitude at equator in radians
        Rn, Re = self.earth.curvature(lat_equator)

        # At equator: Rn should be approximately calculated value
        # and Re should be approximately GRS80_a
        self.assertAlmostEqual(Rn, 6335439.33, places=0)  # Expected Rn at equator
        self.assertAlmostEqual(Re, self.earth.GRS80_a, places=0)

        # Radius of curvature must be positive
        self.assertGreater(Rn, 0)
        self.assertGreater(Re, 0)

        # At equator, Rn should be less than Re
        self.assertLess(Rn, Re)

    def test_curvature_at_poles(self):
        """Test radius of curvature at the poles

        At the poles (lat=±π/2), the radius of curvature in North and East
        should approach a specific value based on GRS80 parameters.
        """
        lat_north_pole = m.pi / 2.0  # North pole
        Rn_pole, Re_pole = self.earth.curvature(lat_north_pole)

        # At poles, both Rn and Re should be close to each other
        # and approximately equal to GRS80_a / sqrt(1 - e2)
        expected_radius = self.earth.GRS80_a / m.sqrt(1.0 - self.earth.e2)

        self.assertAlmostEqual(Rn_pole, expected_radius, places=0)
        self.assertAlmostEqual(Re_pole, expected_radius, places=0)

        # At poles, Rn should be greater than at equator
        Rn_eq, _ = self.earth.curvature(0.0)
        self.assertGreater(Rn_pole, Rn_eq)

    def test_curvature_berlin_latitude(self):
        """Test radius of curvature at Berlin's latitude

        Berlin is at approximately 52.52° N latitude.
        Verifies that curvature calculation is reasonable for this location.
        """
        lat_berlin = np.deg2rad(52.52)  # Berlin latitude
        Rn, Re = self.earth.curvature(lat_berlin)

        # Radii should be positive
        self.assertGreater(Rn, 0)
        self.assertGreater(Re, 0)

        # At Berlin's latitude, Rn should be between GRS80_b and GRS80_a; Re is the prime vertical radius (>= GRS80_a)
        self.assertGreater(Rn, self.earth.GRS80_b)
        self.assertLess(Rn, self.earth.GRS80_a)
        self.assertGreater(Re, self.earth.GRS80_a)

        # At this latitude, Re should be greater than Rn
        self.assertGreater(Re, Rn)

    def test_ellipsoidal_to_cartesian_transformation(self):
        """Test WGS84/GRS80 ellipsoidal to Cartesian coordinate transformation

        Tests the ell2xyz conversion using known reference points:
        - Point at equator, prime meridian with zero height
        - Point at North Pole
        Verifies that the returned object is a Vector and values are reasonable.
        """
        # Test 1: Point at equator (0°, 0°, 0m)
        x_eq, y_eq, z_eq = self.earth.ell2xyz(0.0, 0.0, 0.0)()

        # At equator and prime meridian with zero height:
        # x should be approximately GRS80_a (semi-major axis)
        # y should be approximately 0
        # z should be approximately 0
        self.assertAlmostEqual(float(x_eq), self.earth.GRS80_a, places=-1)
        self.assertAlmostEqual(float(y_eq), 0, places=0)
        self.assertAlmostEqual(float(z_eq), 0, places=0)

        # Test 2: Point at North Pole (90°, any longitude, 0m)
        lat_pole = m.pi / 2.0
        x_pole, y_pole, z_pole = self.earth.ell2xyz(lat_pole, 0.0, 0.0)()

        # At North Pole:
        # x and y should be approximately 0
        # z should be approximately GRS80_b (semi-minor axis)
        self.assertAlmostEqual(float(x_pole), 0, places=0)
        self.assertAlmostEqual(float(y_pole), 0, places=0)
        self.assertAlmostEqual(float(z_pole), self.earth.GRS80_b, places=-1)

        # Test 3: Verify return type is Vector
        result = self.earth.ell2xyz(np.deg2rad(52.52), np.deg2rad(13.40), 0.0)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (3, 1))

        # Test 4: Point with non-zero height
        height = 100.0  # 100 meters above ellipsoid
        x_h, y_h, z_h = self.earth.ell2xyz(lat_pole, 0.0, height)()
        x_h0, y_h0, z_h0 = self.earth.ell2xyz(lat_pole, 0.0, 0.0)()

        # Height increase should increase z-coordinate at pole
        self.assertGreater(float(z_h), float(z_h0))
        self.assertAlmostEqual(float(z_h) - float(z_h0), height, places=0)


if __name__ == "__main__":
    unittest.main()