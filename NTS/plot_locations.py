# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

from NTSvehicleLocation import LocationPrediction

run = LocationPrediction('3')
locs = run.getVehicleLocations()

home = [0]*48
shops = [0]*48
work = [0]*48

for i in range(0,1440):
    home[int(i/30)] += locs['home'][i]*100/30
    work[int(i/30)] += locs['work'][i]*100/30
    shops[int(i/30)] += locs['shops'][i]*100/30

x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
x = np.linspace(2*2,22*2,num=6)

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
plt.plot(home,label='home')
plt.plot(shops,label='shops')
plt.plot(work,label='work')
plt.xlim(0,47)
plt.ylim(0,100)
plt.ylabel('Percentage of vehicles')
plt.xlabel('Time')
plt.xticks(x,x_ticks)
plt.grid()
plt.legend(ncol=3,loc=[0.1,1.05])
plt.show()
