import filemanager as fm
import matplotlib.pyplot as plt

filePath = "data\\UltimateGPS\\sample_dach_gps.csv"
dgps = fm.CSVImporter(filePath, columns=range(7), skip_header = 1, hasTime=False)

plt.plot(dgps.values[:,2], dgps.values[:,1],'b-')
plt.grid(True)
plt.show()