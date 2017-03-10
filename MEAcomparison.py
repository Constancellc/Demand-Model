# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle
from vehicleOriented import Vehicle, JourneyPool, Agent, Fleet, ChargingScheme, Simulation


regionType = 'Urban City and Town'
region = ''


months = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']

days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
population = 800
fleetSize = 488

t = np.linspace(0,24,num=24*60)
xaxis = np.linspace(2,22,num=6)
my_xticks = ['02:00','06:00','10:00','16:00','18:00','22:00']
    
plt.figure(1)
for i in range(0,12):
    print 'running simulation for ' + months[i]
    plt.subplot(4,3,i+1)
    for j in range(0,7):
        simulation = Simulation(regionType,months[i],days[j],population,1,
                                supressText=True)
        test = ChargingScheme(simulation.fleet)
        test.allHomeCharge(3.5,1,supressText=True)
        results = simulation.fleet.generateChargeProfiles(fleetSize,3.5)
        charge = [0.0]*24*60
        for profile in results:
            for k in range(0,24*60):
                charge[k] += profile[k]/fleetSize
        plt.plot(t,charge,label=days[j])
    plt.title(months[i],y=0.8)
    plt.xlim(0,24)
    plt.ylim(0,1)
    plt.xticks(xaxis, my_xticks)
    if i == 0:
        plt.legend(loc=[0,-4.1],ncol=7)

plt.show()
