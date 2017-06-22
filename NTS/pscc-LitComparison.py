# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModelCopy import Drivecycle
from vehicleOriented import Vehicle, JourneyPool, Agent, Fleet, ChargingScheme, Simulation
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

month = 'January'
day = 'Wednesday'

totalPopulation = 53010000
regionBreakdown = {'Urban Conurbation':0.369,'Urban City and Town':0.446,
                   'Rural Town and Fringe':0.092,
                   'Rural Village, Hamlet and Isolated Dwelling':0.093}
numbers = {'Urban Conurbation':196,'Urban City and Town':236,
                   'Rural Town and Fringe':48,
                   'Rural Village, Hamlet and Isolated Dwelling':49}
demand = [0]*(24*60)
energy = [0]*200

for region in regionBreakdown:
    population = regionBreakdown[region]*totalPopulation
    simulation = Simulation(region, month, day, population, 1)

    for i in simulation.fleet.fleet:
        total = 0
        #print i 
        #print simulation.fleet.fleet[i]
        for j in i.energyLog:
            total += j[1]

        energy[int(total)] += numbers[region]

run2 = EnergyPrediction('3','1',model='linear')
energy3 = run2.plotEnergyConsumption(returnResults=True, newFigure=False,wait=True)

# normalise
nEnergy3 = []
for i in range(0,len(energy3)):
    nEnergy3.append(float(energy3[i])/sum(energy3))
    
# normalise
nEnergy = []
for i in range(0,len(energy)):
    nEnergy.append(float(energy[i])/sum(energy))
        
run = EnergyPrediction('3','1')
energy2 = run.plotEnergyConsumption(returnResults=True, newFigure=False,wait=True)

# normalise
nEnergy2 = []
for i in range(0,len(energy2)):
    nEnergy2.append(float(energy2[i])/sum(energy2))

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.subplot(2,1,1)
width = 0.4

plt.bar(np.arange(-width/2,len(nEnergy3)-width/2,1),nEnergy3,width,
        label='Affine Mileage-Energy')


plt.xlim(-1,40)

plt.bar(np.arange(width/2,len(nEnergy2)+width/2,1),nEnergy2,width,
        label='Proposed Vehicle Model',hatch='//')
#plt.xlabel('Predicted Daily Consumption (kWh)')
plt.ylabel('Probability')
plt.legend()

plt.subplot(2,1,2)
plt.bar(np.arange(-width/2,len(nEnergy)-width/2,1),nEnergy,width,
        label='Monte Carlo Simulation')


plt.xlim(-1,40)

plt.bar(np.arange(width/2,len(nEnergy2)+width/2,1),nEnergy2,width,
        label='Bottom-Up Predictions',hatch='//')
plt.xlabel('Predicted Daily Consumption (kWh)')
plt.ylabel('Probability')
plt.legend()
plt.show()
