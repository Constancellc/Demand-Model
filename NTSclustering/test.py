import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from newChargingModel import MC_Simulation

#data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA/'

nV = 50
nMC = 40

test = 'E09000023'
hh = []
with open('../../Documents/UKDA-7553-tab/constance/hh-loc.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if random.random() < 0.05 and len(hh) < 50:#row[2] == test:
            hh.append(row[0])

s = MC_Simulation(hh)
[m,l,u] = s.uncontrolledCharge(3.5,30,100)
c2 = s.dumbCharge(3.5,30)

plt.figure()
plt.plot(m)
plt.plot(c2)
plt.fill_between(range(10080),l,u,alpha=0.2)
plt.xlim(1440*2,1440*3)
plt.grid()
plt.ylabel('Power (kW)')
plt.show()
