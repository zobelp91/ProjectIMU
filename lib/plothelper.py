import matplotlib.pyplot as plt
import numpy as np
import veclib as vl

def plotVector(x, vector):
    """plots 3x1 vector using subplots"""
    y1, y2, y3 = vector()
    symbol = "ro"
    plt.subplot(311)
    plt.plot(x, y1, symbol)
    plt.subplot(312)
    plt.plot(x, y2, symbol)
    plt.subplot(313)
    plt.plot(x, y3, symbol)


def plotVectorRGB(x, vector):
    """plots 3x1 vector in 1 axis"""
    y1, y2, y3 = vector()
    (handle1,) = plt.plot(x, y1, "ro")
    (handle2,) = plt.plot(x, y2, "go")
    (handle3,) = plt.plot(x, y3, "bo")
    plt.grid(True)
    plt.legend([handle1, handle2, handle3], ["X", "Y", "Z"])
