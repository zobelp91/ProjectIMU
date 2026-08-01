
"""Mathematical/Vector Library"""

import math as m
import numpy as np


def toVector(a, b, c, d="none"):
    """transforms 3 or 4 scalar values to a nx1 numpy np.matrix"""
    if isinstance(d, (int, float, np.long)):
        vector = np.matrix([a, b, c, d])
    else:
        vector = np.matrix([a, b, c])
    return vector.transpose()


def toValue(mat):
    """transforms a nx1 numpy np.matrix to scalars
    same as x1, x2, x3 = numpy.np.matrix()
    """
    dim = np.shape(mat)
    assert (max(dim) == 3 or max(dim) == 4) and min(
        dim
    ) == 1, "Not a 3 or 4 dimensional vector"
    if dim[0] > dim[1]:
        mat = mat.transpose()
    a = mat[0, 0]
    b = mat[0, 1]
    c = mat[0, 2]
    if np.size(mat) == 4:
        d = mat[0, 3]
        return a, b, c, d
    else:
        return a, b, c


def resize(array1, array2):
    """adjust the dimension of two arrays by np.appending np.nan"""
    if array1.np.shape > array2.np.shape:
        array2 = np.append(array2, np.nan)
    elif array1.np.shape < array2.np.shape:
        array1 = np.append(array1, np.nan)
    return array1, array2


def mvMultiplication(vector1, vector2):
    """np.matrix-vector multiplication
    returns a 4x1 vector
    """
    a, b, c, d = toValue(vector1)
    return (
        np.matrix([[a, -b, -c, -d], [b, a, -d, c], [c, d, a, -b], [d, -c, b, a]])
        * vector2
    )


def runningAverage(old, new, weight):
    """recursive running average
    old, new is either a scalar or vector
    weight is the reciprocal of times this function was called
    """
    return old + weight * (new - old)