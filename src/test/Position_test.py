import unittest
import numpy as np
import veclib as vl
from Position import Position, EllipsoidPosition
from Velocity import Velocity

class PositionTest(unittest.TestCase):
    def test_position_update(self):
        """Test that Position updates correctly based on velocity and time"""
        # Create initial position at origin
        pos = Position()

        # Create velocity (1 m/s in North direction)
        velocity = Velocity(1, 0, 0)

        # Update position over 10 seconds
        pos.update(velocity, 10)

        # Verify position moved 10 meters North
        updated_x, updated_y, updated_z = pos()
        self.assertAlmostEqual(updated_x, 10.0)
        self.assertAlmostEqual(updated_y, 0.0)
        self.assertAlmostEqual(updated_z, 0.0)

    def test_ellipsoid_position_initialization(self):
        """Test that EllipsoidPosition initializes correctly with GRS80 ellipsoid"""
        # Create position at equator (0 lat, 0 lon, 0 height)
        ell_pos = EllipsoidPosition()

        # Verify values are stored
        lat, lon, h = ell_pos()
        self.assertEqual(lat, 0.0)
        self.assertEqual(lon, 0.0)
        self.assertEqual(h, 0.0)

    def test_ellipsoid_position_correct(self):
        """Test that EllipsoidPosition corrects position with NED vector"""
        # Create position at a known location
        ell_pos = EllipsoidPosition(np.radians(45), np.radians(10), 100, "GRS80")

        # Store initial values
        initial_lat, _, _ = ell_pos()

        # Apply correction in NED frame (1m North, 0m East, 0m Down)
        correction = vl.Vector(1, 0, 0)
        ell_pos.correct(correction)

        # Verify position was corrected
        corrected_lat, _, _ = ell_pos()
        # Position should have changed
        self.assertNotEqual(corrected_lat, initial_lat)

    def test_ellipsoid_position_update(self):
        """Test that EllipsoidPosition updates correctly with velocity"""
        # Create position at a known location
        ell_pos = EllipsoidPosition(np.radians(45), np.radians(10), 100, "GRS80")

        # Store initial values
        initial_lat, _, _ = ell_pos()

        # Create velocity in NED frame (1 m/s North, 0 m/s East, 0 m/s Down)
        velocity = Velocity(1, 0, 0)

        # Update position over 10 seconds
        ell_pos.update(velocity, 10)

        # Verify position was updated
        updated_lat, _, _ = ell_pos()
        # Position should have changed
        self.assertNotEqual(updated_lat, initial_lat)

    def test_position_correct(self):
        """Test that Position corrects position with NED vector"""
        # Create initial position at origin
        pos = Position(10, 5, 20)

        # Store initial values
        initial_x, initial_y, initial_z = pos()

        # Apply correction (1m North, 2m East, 0m Down)
        correction = vl.Vector(1, 2, 0)
        pos.correct(correction)

        # Verify position was corrected
        corrected_x, corrected_y, corrected_z = pos()
        self.assertAlmostEqual(corrected_x, initial_x + 1.0)
        self.assertAlmostEqual(corrected_y, initial_y + 2.0)
        self.assertAlmostEqual(corrected_z, initial_z + 0.0)

if __name__ == '__main__':
    unittest.main()