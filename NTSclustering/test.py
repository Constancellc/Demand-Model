import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from newChargingModel import Simulation

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
        if row[2] == test:
            hh.append(row[0])

s = Simulation(hh)
c1 = s.uncontrolledCharge(3.5,30)
c2 = s.dumbCharge(3.5,30)

plt.figure()
plt.plot(c1)
plt.plot(c2)
plt.show()
