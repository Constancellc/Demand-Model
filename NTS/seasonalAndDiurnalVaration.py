import csv
import matplotlib.pyplot as plt
import numpy as np
import math
from NTSenergyPrediction import EnergyPrediction


y = []

for day in range(1,8):
    run = EnergyPrediction(str(day),month='2')
    energy = 0
    n = 0
    for vehicle in run.energy:
        energy += run.energy[vehicle]
        n += 1

    energy = float(energy)/n
        
    y.append(energy)

    
    
    
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.subplot(2,1,1)
x_ticks = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
plt.bar(range(1,8),y)
plt.xticks(range(1,8),x_ticks)
plt.ylabel('average predicted \n consumption (kWh)')

y = []

for mo in range(1,13):
    run = EnergyPrediction('5',month=str(mo))
    energy = 0
    lst = []
    n = 0
    for vehicle in run.energy:
        energy += run.energy[vehicle]
        n += 1

    energy = float(energy)/n

    y.append(energy)



plt.subplot(2,1,2)
x_ticks = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov',
           'Dec']
plt.bar(range(1,13),y)
plt.xticks(range(1,13),x_ticks)
plt.ylabel('average predicted \n consumption (kWh)')
plt.show()
