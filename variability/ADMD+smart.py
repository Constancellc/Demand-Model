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

avHH = [0.0]*1440
for i in range(0,1000):
    for j in range(0,1440):
        avHH[j] += profiles[i][j]/1000

iAvHH = [0.0]*1440
for i in range(0,1440):
    iAvHH[i] = max(avHH)-avHH[i]

iAvHH += iAvHH[:12*60] # extend to 36 hours

run = EnergyPrediction('3','7')

vehicleProfiles = run.returnDumbChargingProfiles(1000,3.5)

# get psuedo optimal versions of the profiles 
deadline = 32*60 # 8AM next day

POvehicleProfiles = []
for profile in vehicleProfiles:
    p36hrs = [0.0]*36*60
    p24hrs = [0.0]*24*60
    # need to find start time and energy consumption
    energy = sum(profile)

    if energy == 0:
        POvehicleProfiles.append(p24hrs)
        continue

    start = 0
    if profile[0] != 0:
        while profile[start] != 0:
            start += 1
    while profile[start] == 0:
        start += 1

    for i in range(start,len(p36hrs)):
        p36hrs[i] = iAvHH[i]

    sf = energy/sum(p36hrs)

    for i in range(0,len(p36hrs)):
        if i < 1440:
            p24hrs[i] = p36hrs[i]*sf
        else:
            p24hrs[i-1440] = p36hrs[i]*sf

    POvehicleProfiles.append(p24hrs)              

plt.figure(3)
for i in range(0,3):
    plt.plot(vehicleProfiles[i])

aggregation = [300,100,30]

penetrationLevel = [0,0.1,0.3,1.0]

timeScale = 30 # mins

numMC = 100 # number of nonte carlo samples

y_ticks = []
for i in range(0,len(aggregation)):
    y_ticks.append(str(aggregation[i]))

x_ticks = []
for i in range(2,24,2):
    x_ticks.append(str(i)+':00')
        
fig = plt.figure(1)        
fig2 = plt.figure(2)
for pl in range(0,len(penetrationLevel)):

    level = penetrationLevel[pl]
    
    ADMD = [] # dumb
    ADMD2 = [] # psuedo-optimal

    #var = []
    avProfiles = []
    avProfiles2 = []

    for a in range(0,len(aggregation)):
        n = aggregation[a]
        
        for mc in range(0,numMC):
            if level == 0:
                nVehicles = 0
            else:
                nVehicles = np.random.poisson(n*level*1.04) # 1.04 = nVehicles per household

            summed = [0.0]*1440
            summed2 = [0.0]*1440

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
                    summed2[j] += profiles[chosen[i]][j]/n
            for i in range(0,nVehicles):
                for j in range(0,1440):
                    summed[j] += vehicleProfiles[chosenV[i]][j]/n
                    summed2[j] += POvehicleProfiles[chosenV[i]][j]/n

            # then downsample

            ds = [0.0]*int(1440/timeScale)
            ds2 = [0.0]*int(1440/timeScale)

            for i in range(0,len(summed)):
                ds[int(i/timeScale)] += summed[i]/timeScale
                ds2[int(i/timeScale)] += summed2[i]/timeScale

            avProfiles.append(ds)
            avProfiles2.append(ds2)

        # find mean
        mean = [0]*int(1440/timeScale)
        for i in range(0,len(avProfiles)):
            for j in range(0,len(avProfiles[0])):
                mean[j] += avProfiles[i][j]/numMC

        # find ADMD
        ADMD.append([0]*int(1440/timeScale))
        ADMD2.append([0]*int(1440/timeScale))
        for i in range(0,len(avProfiles)):
            for j in range(0,len(avProfiles[0])):
                if avProfiles[i][j] > ADMD[-1][j]:
                    ADMD[-1][j] = avProfiles[i][j]
                if avProfiles2[i][j] > ADMD2[-1][j]:
                    ADMD2[-1][j] = avProfiles2[i][j]
    '''
        # find variance
        var.append([0]*int(1440/timeScale))
        for i in range(0,len(avProfiles)):
            for j in range(0,len(avProfiles[0])):
                var[-1][j] += np.power(avProfiles[i][j]-mean[j],2)/numMC
    '''        
    plt.figure(1)
    ax = fig.add_subplot(len(penetrationLevel),1,pl+1)
    plt.title(str(int(100*level))+'%')
    plt.imshow(ADMD,aspect=7*(10/timeScale),cmap='inferno',vmin=0,vmax=2.2)
    plt.yticks(range(0,len(aggregation)),y_ticks)
    
    plt.ylabel('number of houses')
    plt.xticks(np.linspace(2*60/timeScale,22*60/timeScale,num=len(x_ticks)),x_ticks)
    if pl == 0:
        cbaxes = fig.add_axes([0.92, 0.08, 0.03, 0.8]) 
        plt.colorbar(ax=ax,cax=cbaxes)

    plt.figure(2)
    ax = fig2.add_subplot(len(penetrationLevel),1,pl+1)
    plt.title(str(int(100*level))+'%')
    plt.imshow(ADMD2,aspect=7*(10/timeScale),cmap='inferno',vmin=0,vmax=2.2)
    plt.yticks(range(0,len(aggregation)),y_ticks)
    
    plt.ylabel('number of houses')
    plt.xticks(np.linspace(2*60/timeScale,22*60/timeScale,num=len(x_ticks)),x_ticks)
    if pl == 0:
        cbaxes = fig2.add_axes([0.92, 0.08, 0.03, 0.8]) 
        plt.colorbar(ax=ax,cax=cbaxes)


    #plt.xlabel('time')
'''
    plt.figure(2)
    ax = fig2.add_subplot(len(penetrationLevel),1,pl+1)
    plt.title(str(int(100*level))+'%')
    plt.imshow(var,aspect=5*(10/timeScale),cmap='inferno',vmin=0,vmax=18)
    plt.yticks(range(0,len(aggregation)),y_ticks)
    
    plt.ylabel('number of houses')
    plt.xticks(np.linspace(2*60/timeScale,22*60/timeScale,num=len(x_ticks)),x_ticks)
    if pl == 0:
        cbaxes = fig2.add_axes([0.92, 0.08, 0.03, 0.8]) 
        plt.colorbar(ax=ax,cax=cbaxes)
'''


plt.show()