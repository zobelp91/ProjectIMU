import unittest
from numpy import shape, matrix, linalg
from veclib import toVector, toValue, mvMultiplication, runningAverage
from math import hypot

class MathLib_test(unittest.TestCase):
    def test_pythagoras_2D(self):
        c = hypot(3.0, 4.0)
        self.assertEqual(c, 5.0)

    def test_pythagoras_3D(self):
        c = hypot(3.0, 4.0, 5.0)
        self.assertAlmostEqual(c, 7.0711, delta=0.0001)

    def test_pythagoras_5D(self):
        c = hypot(3.0, 4.0, 5.0, 6.0, 7.0)
        self.assertAlmostEqual(c, 11.6190, delta=0.0001)

    def test_toVector_3D(self):
        vector = toVector(1, 2, 3)
        self.assertEqual(vector[0].item(), 1)
        self.assertEqual(vector[1].item(), 2)
        self.assertEqual(vector[2].item(), 3)
        self.assertEqual(shape(vector), (3, 1))

    def test_toVector_4D(self):
        vector = toVector(1, 2, 3, 4)
        self.assertEqual(vector[0].item(), 1)
        self.assertEqual(vector[1].item(), 2)
        self.assertEqual(vector[2].item(), 3)
        self.assertEqual(vector[3].item(), 4)
        self.assertEqual(shape(vector), (4, 1))

    def test_toValue_3D(self):
        a, b, c = toValue(matrix([1, 2, 3]))
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)

    def test_toValue_4D(self):
        a, b, c, d = toValue(matrix([1, 2, 3, 4]))
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)

    def test_mvMultplication(self):
        vec1 = toVector(1, 2, 3, 4)
        vec2 = toVector(1, -2, -3, -4)
        res = mvMultiplication(vec1, vec2)
        self.assertEqual(res[0].item(), 30)
        self.assertEqual(res[1].item(), 0)
        self.assertEqual(res[2].item(), 0)
        self.assertEqual(res[3].item(), 0)

    def test_runningAverage(self):
        v = 0.0
        i = 1
        for new in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            v = runningAverage(v, new, 1 / i)
            i += 1
        self.assertEqual(i, 11)
        self.assertEqual(v, 5.5)

    def test_runningAverage_negativ(self):
        v = 0.0
        i = 1
        for new in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            v = runningAverage(v, -new, 1 / i)
            i += 1
        self.assertEqual(i, 11)
        self.assertEqual(v, -5.5)


if __name__ == "__main__":
    unittest.main()