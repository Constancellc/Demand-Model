# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

# my code
from NHTSvehicleLocation import LocationPrediction

test = LocationPrediction('3')
loc = test.getVehicleLocations()

x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
x = np.linspace(2,22,num=6)

t = np.arange(0,24,0.5)
plt.figure(1)
plt.plot(t,loc['1'],label='home')
plt.plot(t,loc['10'],label='work')
plt.plot(t,loc['40'],label='shops')
plt.legend()
plt.xlabel('time')
plt.ylabel('percentage of fleet')
plt.grid()
plt.xticks(x,x_ticks)

plt.show()
