# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('../NTS')

# my code
from NTSenergyPrediction import EnergyPrediction

profiles = []

for i in range(0,1000):
    profiles.append([0.0]*1440)

i = 0
with open('../../Documents/household_demand_pool.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for j in range(0,1000):
            profiles[j][i] = float(row[j])
        i += 1

run = EnergyPrediction('3','7')

vehicleProfiles = run.returnDumbChargingProfiles(1000,3.5)


# assume we have some number of profiles
aggregation = [50,20,10,5,2]#,1]

#penetrationLevel = np.arange(0,1.1,0.1)
penetrationLevel = [0,0.1,0.3,1.0]

timeScale = 10 # mins


#mean = []

numMC = 100 # number of nonte carlo samples



y_ticks = []
for i in range(0,len(aggregation)):
    y_ticks.append(str(aggregation[i]))

x_ticks = []
for i in range(2,24,2):
    x_ticks.append(str(i)+':00')
        

plt.figure(1)

for pl in range(0,len(penetrationLevel)):
    level = penetrationLevel[pl]
    ADMD = []
    
    for a in range(0,len(aggregation)):
        ADMD.append([0]*int(1440/timeScale))
        #mean.append([0]*int(1440/timeScale))
        n = aggregation[a]

        for mc in range(0,numMC):
            if level == 0:
                nVehicles = 0
            else:
                nVehicles = np.random.poisson(n*level)
            summed = [0.0]*1440

            # first pick household profiles
            chosen = []

            while len(chosen) < n:
                index = int(1000*random.random())
                if index not in chosen:
                    chosen.append(index)

            # then pick vehicle profiles
            chosenV = []

            while len(chosenV) < nVehicles:
                index = int(1000*random.random())
                if index not in chosenV:
                    chosenV.append(index)

            for i in range(0,n):
                for j in range(0,1440):
                    summed[j] += profiles[chosen[i]][j]/n
            for i in range(0,nVehicles):
                for j in range(0,1440):
                    summed[j] += vehicleProfiles[chosenV[i]][j]/n

            # then downsample

            ds = [0.0]*int(1440/timeScale)

            for i in range(0,len(summed)):
                ds[int(i/timeScale)] += summed[i]/timeScale

            for i in range(0,len(ds)):
                #mean[a][i] += ds[i]/numMC
                if ds[i] >= ADMD[a][i]:
                    ADMD[a][i] = ds[i]

    plt.subplot(len(penetrationLevel),1,pl+1)
    plt.title(str(int(100*level))+'%')
    plt.imshow(ADMD,aspect=5,cmap='inferno')#,vmin=0,vmax=8)
    plt.yticks(range(0,len(aggregation)),y_ticks)
    plt.xticks(np.linspace(2*60/timeScale,22*60/timeScale,num=len(x_ticks)),x_ticks)
    plt.colorbar()
    plt.ylabel('number of houses')
'''
plt.subplot(2,1,2)

plt.imshow(mean,aspect=5)
plt.yticks(range(0,len(aggregation)),y_ticks)
plt.xticks(np.linspace(2*60/timeScale,22*60/timeScale,num=len(x_ticks)),x_ticks)
plt.colorbar()
'''
plt.xlabel('time')
plt.show()
