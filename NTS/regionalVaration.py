import csv
import matplotlib.pyplot as plt
import numpy as np
import math
from NTSenergyPrediction import EnergyPrediction


y = []

for r in range(1,5):
    run = EnergyPrediction('3',regionType=str(r))
    energy = 0
    n = 0
    print len(run.energy)
    for vehicle in run.energy:
        energy += run.energy[vehicle]
        n += 1

    energy = float(energy)/n
        
    y.append(energy)

    
    
    
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
x_ticks = ['Urban\n Conurbation','Urban City\n & Town','Rural\n Town &\n Fringe','Rural\n Village,\n Hamlet &\n Isolated Dwelling']
plt.bar(range(1,5),y)
plt.xticks(range(1,5),x_ticks)
plt.ylabel('average predicted \n consumption (kWh)')

plt.show()
