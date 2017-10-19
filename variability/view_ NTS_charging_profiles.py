# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('../NTS')

profiles = []

with open('../../Documents/vehicle_demand_pool.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        new = []
        for cell in row:
            new.append(float(cell))
        profiles.append(new)

energy = [0]*25
av = [0.0]*1440

for profile in profiles:
    try:
        energy[int(sum(profile)/60)] += 1/1000
    except:
        print('skipped')

    for i in range(0,1440):
        av[i] += profile[i]/1000

plt.figure(1)
plt.subplot(2,1,1)
plt.bar(range(0,len(energy)),energy)
plt.subplot(2,1,2)
plt.plot(av)
plt.show()
