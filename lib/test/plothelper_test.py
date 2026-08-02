import unittest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import veclib as vl
import plothelper as ph


class PlotHelperTest(unittest.TestCase):
    def test_plotVector(self):
        plt.close('all')

        x = 0
        v = vl.Vector(1.0, 2.0, 3.0)

        ph.plotVector(x, v)

        fig = plt.gcf()
        axes = fig.get_axes()
        self.assertEqual(len(axes), 3)

        for idx, ax in enumerate(axes):
            lines = ax.get_lines()
            self.assertEqual(len(lines), 1)
            line = lines[0]
            np.testing.assert_array_equal(line.get_xdata(), x)
            expected_y = float(v()[idx])
            np.testing.assert_array_equal(line.get_ydata(), np.array([expected_y]))

    def test_plotVectorRGB(self):
        plt.close('all')

        x = 1
        v = vl.Vector(10.0, 20.0, 30.0)

        ph.plotVectorRGB(x, v)

        fig = plt.gcf()
        axes = fig.get_axes()
        self.assertGreaterEqual(len(axes), 1)
        ax = axes[0]

        lines = ax.get_lines()
        self.assertEqual(len(lines), 3)
        colors = [line.get_color() for line in lines]
        self.assertIn('r', colors)
        self.assertIn('g', colors)
        self.assertIn('b', colors)

        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        legend_texts = [t.get_text() for t in legend.get_texts()]
        self.assertListEqual(sorted(legend_texts), sorted(["X", "Y", "Z"]))

if __name__ == "__main__":
    unittest.main()