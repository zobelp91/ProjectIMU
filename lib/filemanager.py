
"""File import library"""

import numpy as np
import pathlib as pl

SEPSYM = ","

class FileImporter:
    """base class for importing data from a csv file"""

    def __init__(self, fileStr):
        """intializes the class fields and checks if the file exists"""
        self.path = pl.Path(fileStr).resolve()
        self.numCol = self._getNumCol()
        self.values = self._read() 
        self.length = len(self.values)
        self.time = self.values[:, 0]
        self.dt = self._getSampleRate()

    def _read(self):
        """reads the file and populates class fields"""
        pass

    def _getSampleRate(self):
        """gets median time step size"""
        return np.median(np.diff(self.time))

    def _getNumCol(self):
        """gets the number of columns in the file"""
        with open(self.path) as f:
            sepCount = f.readlines()[self.skipHeader].count(SEPSYM)
        return sepCount + 1

class ImuDataImporter(FileImporter):
    """ class for importing IMU data from a CSV file """

    def __init__(self, fileStr):
        self.skipHeader = 7
        super().__init__(fileStr) 
        self.gyroX = self.values[:,1]
        self.gyroY = self.values[:,2]
        self.gyroZ = self.values[:,3]
        self.accelX = self.values[:,4]
        self.accelY = self.values[:,5]
        self.accelZ = self.values[:,6]
        self.magX = self.values[:,7]
        self.magY = self.values[:,8]
        self.magZ = self.values[:,9]
        self.phi = self.values[:,10]
        self.theta = self.values[:,11]
        self.psi = self.values[:,12]

    def _read(self):
        return np.genfromtxt(
            self.path,
            delimiter=SEPSYM,
            invalid_raise=True,
            usecols=range(self.numCol),
            skip_header=self.skipHeader)

class GpsDataImporter(FileImporter):
    """ class for importing GPS data from a CSV file"""

    def __init__(self, fileStr):
        self.skipHeader = 1
        super().__init__(fileStr)
        self.latitude = self.values[:,1] #deg
        self.longitude = self.values[:,2] #deg
        self.height = self.values[:,3] #m
        self.vx = self.values[:,4] #m/s
        self.vy = self.values[:,5] #m/s
        self.vz = self.values[:,6] #m/s
        if self.numCol > 7:
            self.stdX = self.values[:,7] #m 95% confidence
            self.stdY = self.values[:,8] #m 95% confidence
            self.stdZ = self.values[:,9] #m 95% confidence
            self.numSats = self.values[:,10]

    def _read(self):
        return np.genfromtxt(
            self.path,
            delimiter=SEPSYM,
            invalid_raise=True,
            usecols=range(self.numCol),
            skip_header=self.skipHeader)