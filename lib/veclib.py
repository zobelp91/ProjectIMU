
"""Mathematical/Vector Library"""

import math as m
import numpy as np

class Vector(np.ndarray):
    """Derived class for handling 1-dimensional arrays"""

    def __new__(cls, a=0, b=0, c=0, info=None):
        # create a new instance as a column vector
        obj = np.asarray(list(map(float, [a, b, c]))).reshape(-1,1).view(cls)
        obj.info = info # custom metadata
        return obj
    
    # Alternative Constructor Option
    @classmethod
    def from_array(cls, array, info=None):
        # view-cast it into our subclass
        obj = array.reshape(-1,1).view(cls)
        # Attach the metadata
        obj.info = info
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        # copies attributes from the original object to the new one
        self.info = getattr(obj, 'info', None)

    def __call__(self):
        return self[0,0], self[1,0], self[2,0]

class LowPassFilter:
    def __init__(self, initialvalue = None):
        self.prev = initialvalue

    def __call__(self, new, weight):
        assert 0 < weight < 1, "weight must be between 0 and 1"
        self.prev += weight * (new - self.prev)