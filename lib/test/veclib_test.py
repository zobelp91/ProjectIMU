import unittest
import numpy as np
import veclib as vl


class VeclibTest(unittest.TestCase):
    def test_constructor_basic(self):
        """Test basic Vector construction with three values"""
        v = vl.Vector(1, 2, 3)
        self.assertIsNotNone(v)
        self.assertEqual(v.shape, (3, 1))

    def test_constructor_values(self):
        """Test that Vector stores correct values"""
        v = vl.Vector(1.5, 2.5, 3.5)
        a, b, c = v()
        self.assertAlmostEqual(float(a), 1.5)
        self.assertAlmostEqual(float(b), 2.5)
        self.assertAlmostEqual(float(c), 3.5)

    def test_constructor_negative_values(self):
        """Test Vector construction with negative values"""
        v = vl.Vector(-1, -2, -3)
        a, b, c = v()
        self.assertAlmostEqual(float(a), -1)
        self.assertAlmostEqual(float(b), -2)
        self.assertAlmostEqual(float(c), -3)

    def test_constructor_zero_values(self):
        """Test Vector construction with zero values"""
        v = vl.Vector(0, 0, 0)
        a, b, c = v()
        self.assertEqual(float(a), 0)
        self.assertEqual(float(b), 0)
        self.assertEqual(float(c), 0)

    def test_constructor_large_values(self):
        """Test Vector construction with large values"""
        v = vl.Vector(1e6, 1e7, 1e8)
        a, b, c = v()
        self.assertAlmostEqual(float(a), 1e6)
        self.assertAlmostEqual(float(b), 1e7)
        self.assertAlmostEqual(float(c), 1e8)

    def test_call_method_returns_tuple(self):
        """Test that __call__ returns a tuple of three values"""
        v = vl.Vector(4, 5, 6)
        result = v()
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result, tuple)

    def test_column_vector_shape(self):
        """Test that Vector is a column vector (3x1)"""
        v = vl.Vector(1, 2, 3)
        self.assertEqual(v.shape[0], 3)
        self.assertEqual(v.shape[1], 1)

    def test_vector_is_ndarray(self):
        """Test that Vector is an instance of ndarray"""
        v = vl.Vector(1, 2, 3)
        self.assertIsInstance(v, np.ndarray)

    def test_info_attribute_initialization(self):
        """Test that info attribute is initialized to None"""
        v = vl.Vector(1, 2, 3)
        self.assertIsNone(v.info)

    def test_vector_dtype(self):
        """Test Vector data type (should be float)"""
        v = vl.Vector(1, 2, 3)
        self.assertTrue(np.issubdtype(v.dtype, np.floating))

    def test_vector_float_values(self):
        """Test Vector with float and int mixed"""
        v = vl.Vector(1, 2.5, 3)
        a, b, c = v()
        self.assertAlmostEqual(float(a), 1)
        self.assertAlmostEqual(float(b), 2.5)
        self.assertAlmostEqual(float(c), 3)

    def test_constructor_none(self):
        """Test LowPassFilter initialization with None"""
        lpf = vl.LowPassFilter()
        self.assertIsNone(lpf.prev)

    def test_constructor_with_value(self):
        """Test LowPassFilter initialization with a value"""
        lpf = vl.LowPassFilter(initialvalue=10)
        self.assertEqual(lpf.prev, 10)

    def test_constructor_with_zero(self):
        """Test LowPassFilter initialization with zero"""
        lpf = vl.LowPassFilter(initialvalue=0)
        self.assertEqual(lpf.prev, 0)

    def test_constructor_with_negative(self):
        """Test LowPassFilter initialization with negative value"""
        lpf = vl.LowPassFilter(initialvalue=-5)
        self.assertEqual(lpf.prev, -5)

    def test_filter_single_step(self):
        """Test a single filtering step"""
        lpf = vl.LowPassFilter(initialvalue=0)
        lpf(10, 0.5)
        # After one step: 0 + 0.5 * (10 - 0) = 5
        self.assertAlmostEqual(lpf.prev, 5)

    def test_filter_multiple_steps(self):
        """Test multiple filtering steps"""
        lpf = vl.LowPassFilter(initialvalue=0)
        weight = 0.1
        lpf(100, weight)
        # After step 1: 0 + 0.1 * (100 - 0) = 10
        self.assertAlmostEqual(lpf.prev, 10)
        lpf(100, weight)
        # After step 2: 10 + 0.1 * (100 - 10) = 19
        self.assertAlmostEqual(lpf.prev, 19)

    def test_filter_convergence(self):
        """Test that filter converges to input value"""
        lpf = vl.LowPassFilter(initialvalue=0)
        target = 50
        weight = 0.2
        # Run multiple iterations
        for _ in range(100):
            lpf(target, weight)
        # Should converge close to target
        self.assertAlmostEqual(lpf.prev, target, places=5)

    def test_filter_weight_validation_too_low(self):
        """Test that weight < 0 raises AssertionError"""
        lpf = vl.LowPassFilter(initialvalue=0)
        with self.assertRaises(AssertionError):
            lpf(10, -0.1)

    def test_filter_weight_validation_too_high(self):
        """Test that weight >= 1 raises AssertionError"""
        lpf = vl.LowPassFilter(initialvalue=0)
        with self.assertRaises(AssertionError):
            lpf(10, 1.0)

    def test_filter_weight_validation_zero(self):
        """Test that weight = 0 raises AssertionError"""
        lpf = vl.LowPassFilter(initialvalue=0)
        with self.assertRaises(AssertionError):
            lpf(10, 0)

    def test_filter_weight_valid_bounds(self):
        """Test valid weight values (between 0 and 1)"""
        lpf = vl.LowPassFilter(initialvalue=0)
        # Should not raise with 0.5
        try:
            lpf(10, 0.5)
            success = True
        except AssertionError:
            success = False
        self.assertTrue(success)

    def test_filter_weight_small_value(self):
        """Test filter with small weight (low pass)"""
        lpf = vl.LowPassFilter(initialvalue=0)
        weight = 0.01
        lpf(100, weight)
        # With small weight, should change slowly
        self.assertLess(lpf.prev, 5)
        self.assertGreater(lpf.prev, 0)

    def test_filter_weight_large_value(self):
        """Test filter with large weight (fast response)"""
        lpf = vl.LowPassFilter(initialvalue=0)
        weight = 0.99
        lpf(100, weight)
        # With large weight, should respond quickly
        self.assertGreater(lpf.prev, 90)
        self.assertLess(lpf.prev, 100)

    def test_filter_no_change(self):
        """Test filter when input equals previous value"""
        lpf = vl.LowPassFilter(initialvalue=50)
        lpf(50, 0.5)
        # Output should remain 50 since input = previous
        self.assertAlmostEqual(lpf.prev, 50)

    def test_filter_negative_values(self):
        """Test filter with negative input values"""
        lpf = vl.LowPassFilter(initialvalue=0)
        lpf(-50, 0.5)
        self.assertAlmostEqual(lpf.prev, -25)

    def test_filter_with_integer_vector_input(self):
        """Test filter behavior with vector input"""
        lpf = vl.LowPassFilter(vl.Vector(10, 20, 30))
        arr = vl.Vector(30, 40, 50)
        # The filter should work with Vector class
        lpf(arr, 0.5)
        self.assertTrue((lpf.prev == vl.Vector(20.0, 30.0, 40.0)).all())

    def test_filter_with_float_vector_input(self):
        """Test filter behavior with vector input"""
        lpf = vl.LowPassFilter(vl.Vector(10.0, 20.0, 30.0))
        arr = vl.Vector(30.0, 40.0, 50.0)
        # The filter should work with Vector class
        lpf(arr, 0.5)
        self.assertTrue((lpf.prev == vl.Vector(20.0, 30.0, 40.0)).all())

    def test_filter_state_preservation(self):
        """Test that filter state is preserved between calls"""
        lpf = vl.LowPassFilter(initialvalue=10)
        lpf(20, 0.5)
        state_after_first = float(lpf.prev)
        lpf(30, 0.5)
        state_after_second = float(lpf.prev)
        # State should change with each call
        self.assertNotEqual(state_after_first, 10)
        self.assertNotEqual(state_after_second, state_after_first)


if __name__ == "__main__":
    unittest.main()
