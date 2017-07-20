# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

day = '3'
month = '1'

# This is going to be only 1 month, telling the story for the policy paper

nHours = 36
t = np.linspace(0,nHours,nHours*60)

x = np.linspace(8,32,num=5)
my_xticks = ['08:00 \n Wed','14:00','20:00','02:00','08:00 \n Thu']

pointsPerHour = 1

run = NationalEnergyPrediction(day,month)

dumb = run.getDumbChargingProfile(3.5,nHours)
psuedo = run.getPsuedoOptimalProfile(7.0,deadline=10)
optimal_individuals = run.getOptimalChargingProfiles(7.0,deadline=10,
                                                     allowOverCap=False)

base = run.baseLoad

summed = [0.0]*36

for vehicle in optimal_individuals['']:
    for i in range(0,36):
        summed[i] += optimal_individuals[''][vehicle][i]

for i in range(0,36):
    summed[i] += base[int(60*i)]
    summed[i] = summed[i]/1000000
    
for i in range(0,len(dumb)):
    dumb[i] += base[i]
    psuedo[i] += base[i]

    dumb[i] = dumb[i]/1000000
    base[i] = base[i]/1000000
    psuedo[i] = psuedo[i]/1000000

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.plot(t,base,ls=':',c='g',label='Base Load')
plt.plot(t,dumb,label='Uncontrolled Charging')
plt.plot(summed,ls='--',label='Optimal Charging')
plt.grid()
plt.legend(ncol=2,loc=[-0.1,1.05])

plt.xticks(x, my_xticks)
plt.xlabel('time')
plt.ylabel('Power Demand (GW)')
plt.xlim(6,34)
plt.ylim(20,85)

plt.figure(2)
plt.rcParams["font.family"] = 'serif'
plt.plot(t,base,ls=':',c='g',label='Base Load')
plt.plot(t,psuedo,label='Approximation')
plt.plot(summed,ls='--',label='Optimal')

plt.grid()
plt.legend(ncol=2,loc=[0.1,1.05])

plt.xticks(x, my_xticks)
plt.xlabel('time')
plt.ylabel('Power Demand (GW)')
plt.xlim(6,34)


plt.show()
