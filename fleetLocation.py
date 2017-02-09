# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle
from vehicleOriented import Vehicle, JourneyPool, Agent, Fleet, ChargingScheme, Simulation

# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------

class VariedPower:

    def __init__(self,simulation):
        self.fleet = simulation.fleet
        self.factor = simulation.factor
        
    def atHomeCharge(self,powers):

        test = ChargingScheme(self.fleet)

        t = np.linspace(4,28,num=24*60)
        plt.figure(1)
        for power in powers:           
            demand = test.allHomeCharge(power,self.factor)
            
            plt.plot(t,demand,label=str(power)+' kW')
            test.resetTest()

        x = np.linspace(6,26,num=6)
        my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
        plt.xticks(x, my_xticks)
        plt.xlim((4,28))
        plt.xlabel('time')
        plt.ylabel('power demand /kW')

        plt.legend(loc=1)
        plt.show()

class VariedScheme:

    def __init__(self,simulation):
        self.fleet = simulation.fleet
        self.factor = simulation.factor

    def fixedPower(self,power):
        test = ChargingScheme(self.fleet)

        t = np.linspace(4,28,num=24*60)
        plt.figure(1)
        
        homeOnly = test.allHomeCharge(power,self.factor)
        plt.plot(t,homeOnly,label='Home Only')

        test.resetTest()
        homeAndWork = test.allHomeandWorkCharge(power,self.factor)
        plt.plot(t,homeAndWork,label='Home and Work')
        
        x = np.linspace(6,26,num=6)
        my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
        plt.xticks(x, my_xticks)
        plt.xlim((4,28))
        plt.xlabel('time')
        plt.ylabel('power demand /kW')

        plt.legend(loc='upper left')
        plt.show()
# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------
regionType = 'Urban City and Town'
region = ''
month = 'May'
day = 'Wednesday'
population = 150200


# varied scheme experiment
"""
simulation = Simulation(regionType, month, population)
variedScheme = VariedScheme(simulation)
variedScheme.fixedPower(4)
"""

# varied power experiment
'''
simulation = Simulation(regionType, month, population)
variedPower = VariedPower(simulation)
variedPower.atHomeCharge([11,4,2])
'''
# repeatability experiment
'''
results = []

for i in range(0,3):
    simulation = Simulation(regionType, month, population)
    results.append(simulation.fleet.getFleetExpenditure(simulation.factor))

t = np.linspace(4,28,num=24*60)
plt.figure(1)
for i in range(0,3):
    plt.plot(t,results[i],label='run'+str(i))

x = np.linspace(6,26,num=6)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(x, my_xticks)
plt.xlim((4,28))
plt.xlabel('time')
plt.ylabel('total energy consumed /kWh')

plt.legend(loc='upper left')
plt.show()
'''
# ------------------------------------------------------------------------------
# PLOT FLEET LOCATION VARIATION WITH TIME
# ------------------------------------------------------------------------------
 
t = np.linspace(4,28,num=24*60)
simulation = Simulation(regionType, month, day, population, 0)


test = ChargingScheme(simulation.fleet,24*60)
homeOnly = test.allHomeCharge(2,simulation.factor)
n = simulation.fleet.getFleetLocations(1.0/simulation.fleet.n)

# Generating figure and lines
plt.figure(1)
plt.plot(t,n[0],label='Home')
plt.plot(t,n[2],label='Work')
plt.plot(t,n[3],label='Other')
plt.plot(t,n[1],label='In Transit')
plt.plot(t,n[4],label='Charging')

# sort out the y axis
#plt.ylim((0,1))
plt.ylabel('percentage of vehicles')

# and x axis
x = np.linspace(6,26,num=6)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(x, my_xticks)
plt.xlim((4,28))
plt.xlabel('time')

# Finally, add legend
plt.legend(loc=1)
plt.show()
