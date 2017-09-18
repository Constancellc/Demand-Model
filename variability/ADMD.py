# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

profiles = []

for i in range(0,1000):
    profiles.append([0.0]*1440)

i = 0
with open('../../Documents/household_demand_pool.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for j in range(0,1000):
            profiles[j][i] = row[j]
        i += 1

vehicleProfiles = []



# assume we have some number of profiles
aggregation = [1,2,5,10,20,30]

#penetrationLevel = np.arange(0,1.1,0.1)
penetrationLevel = [0,0.1,0.3,1.0]

timeScale = 10 # mins

for i in range(0,len(aggregation)):
    n = aggregation[i]

    for j in range(0,1000):
        nVehicles = np.random.poisson(n*penetration)

        aggr = [0.0]*1440

        # first pick household profiles

        # then pick vehicle profiles

        # then downsample

        ds = [0.0]*int(1440/timeScale)

        for i in range(0,len(aggr)):
            ds[int(i/timeScale)] += aggr[i]/timeScale


plt.figure(1)
plt.plot(profiles[2])
plt.plot(profiles[456])
plt.show()
