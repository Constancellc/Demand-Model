# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
#from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import NationalEnergyPrediction

day = '3'
pointsPerHour = 1
nHours = 36

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plotMonths = {'1':1,'4':2,'7':3,'10':4}
titles = {'1':'January','4':'April','7':'July','10':'October'}

t = np.linspace(0,nHours,nHours*60)
t_smart = np.arange(0.5/pointsPerHour,nHours+0.5/pointsPerHour,1)
x = np.linspace(8,32,num=5)
my_xticks = ['08:00 \n Wed','14:00','20:00','02:00','08:00 \n Thu']

for month in ['1','4','7','10']:
    run = NationalEnergyPrediction(day,month)
    dumbProfile = run.getDumbChargingProfile(3.5,nHours) # kW
    smart = run.getOptimalChargingProfiles(4,deadline=9)
    psuedo = run.getgetPsuedoOptimalProfile(7.0,deadline=9)

    smartProfile = [0.0]*nHours*pointsPerHour
    for vehicle in smart['']:
        for i in range(0,nHours*pointsPerHour):
            smartProfile[i] += smart[''][vehicle][i]

    base = run.baseLoad

    for i in range(0,len(dumbProfile)):
        dumbProfile[i] += base[i]
        psuedo[i] += base[i]
        dumbProfile[i] = dumbProfile[i]/1000000 # kW -> GW
        psuedo[i] = psuedo[i]/1000000

        if i%(60/pointsPerHour) == 0:
            smartProfile[int(i*pointsPerHour/60)] += base[i]
            smartProfile[int(i*pointsPerHour/60)] = smartProfile[int(i*pointsPerHour/60)]\
                                               /1000000 # kW -> GW
        base[i] = base[i]/1000000 # kW -> GW

    plt.subplot(2,2,plotMonths[month])
    plt.plot(t,base,ls=':',c='g',label='Base Load')
    plt.plot(t,dumbProfile,label='Uncontrolled Charging')
    plt.plot(t_smart,smartProfile,label='Optimal')
    plt.plot(t,psuedo,c='b',ls='-.',label='Approximation')
    
    if month == '1':
        plt.legend(loc=[-0.2,1.1],ncol=4)
        
    plt.xticks(x, my_xticks)
    plt.xlabel('time')
    plt.ylabel('Power Demand (GW)')
    plt.xlim(6,34)
    plt.ylim(20,85)
    plt.title(titles[month],y=0.8)
    plt.grid()

plt.show()
    
