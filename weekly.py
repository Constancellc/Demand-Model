# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle
from vehicleOriented import Vehicle, JourneyPool, WeekAgent, Fleet, WeekSimulation, ChargingScheme

regionType = 'Urban City and Town'
region = ''
month = 'May'
population = 150200

simulation = WeekSimulation(regionType, month, population, 0)
test = ChargingScheme(simulation.fleet,7*24*60)
test.allHomeCharge(3,simulation.factor)
n = simulation.fleet.getFleetLocations(1.0/simulation.fleet.n,24*60*7)

plt.figure(1)
#for i in range(0,1):
#    profile = simulation.fleet.fleet[i].getChargeProfile()
#    plt.plot(profile)
# Generating figure and lines
t = np.linspace(4,172,num=24*60*7)
#plt.figure(1)
plt.plot(t,n[0],label='Home')
plt.plot(t,n[2],label='Work')
plt.plot(t,n[3],label='Other')
plt.plot(t,n[1],label='In Transit')
plt.plot(t,n[4],label='Charging')

plt.legend(loc=1)
plt.show()
