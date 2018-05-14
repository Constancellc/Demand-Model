# packages
import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster as clst
import sys
from cvxopt import matrix, spdiag, solvers, sparse

# my code
sys.path.append('../')
from vehicleModel import Drivecycle, Vehicle

# these are the csv files containing the data
trips = '../../Documents/UKDA-5340-tab/constance-trips.csv'
households = '../../Documents/UKDA-5340-tab/constance-households.csv'

pool = {}
car = Vehicle(1647.7,29.61,0.0738,0.02195,0.86,30.0)
car.load = 100

# I think I'm going to need to do two passes, one finding commuters and one
# filling in details

with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if int(row[6]) != 3: # day of week
            continue
        if row[5] != '8': # region
            continue
        if row[4] not in ['2','3','4']: # region type
            continue
 
        if row[12] != '1' and row[13] != '1': # commute?
            continue

        vehicle = row[2]

        if vehicle not in pool:
            pool[vehicle] = [0,0,0,0]
            
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[2] not in pool: # commuters
            continue
        if int(row[6]) > 5: # day of week
            continue

        vehicle = row[2]
        purposeFrom = row[12]
        purposeTo = row[13]
        
        tripDistance = float(row[11])*1609.34 # miles -> m
        
        if tripDistance > 10000:
            cycle = Drivecycle(tripDistance,'motorway')
        elif row[4] == '2':
            cycle = Drivecycle(tripDistance,'urban')
        else:
            cycle = Drivecycle(tripDistance,'rural')
            
        energy = car.getEnergyExpenditure(cycle,0.5)
        
        try:
            start = int(row[9])
            end = int(row[10])
        except:
            continue

        if purposeFrom == '1':
            pool[vehicle][1] = start
            
        elif purposeTo == '1':
            pool[vehicle][0] = end
            pool[vehicle][3] = energy

        pool[vehicle][2] += energy

with open('../../Documents/simulation_results/eynsham.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['arrival','departure','daily energy','commute energy'])

    for vehicle in pool:
        if pool[vehicle][0] == 0 or pool[vehicle][1] == 0:
            continue
        writer.writerow(pool[vehicle])
    
starts = [0]*1440
ends = [0]*1440
energy = [0]*200

for vehicle in pool:
    if pool[vehicle][0] == 0 or pool[vehicle][1] == 0:
        continue
    try:
        starts[pool[vehicle][0]] += 1
        ends[pool[vehicle][1]] += 1
        energy[int(pool[vehicle][2])] += 1
    except:
        continue

plt.figure(1)
plt.subplot(3,1,1)
plt.plot(starts)
plt.subplot(3,1,2)
plt.plot(ends)
plt.subplot(3,1,3)
plt.plot(energy)
plt.show()
