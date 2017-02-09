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



# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------

month = 'December'
day = 'Wednesday'
population = 527612 # this is the city Manchester, the borough has more people
regionType = 'Urban City and Town'

colours = ['#42cef4','#42a4f4','#4256f4']
t1 = np.linspace(4,28,num=24*60)
for i in range(0,3):
    simulation = Simulation(regionType,month,day,population,2)
    test = ChargingScheme(simulation.fleet,24*60)
    test.getFleetSubset(100)
    demand = test.allHomeCharge(3,1)

    if i == 0:
        plt.figure(1)
    plt.plot(t1,demand,colours[i],label='Simulation #'+str(i+1))

predictedEnergy = 0

for value in demand:
    predictedEnergy += value/60

print 'the simulation predicted ' + str(predictedEnergy) + 'kWh of expenditure'

observedEnergy = 0

measured = []
with open('enwl-data/Winter_EV_Profiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        total = 0
        for item in row:
            total += int(item)
        measured.append(total)
        
for value in measured:
    observedEnergy += value/12

print 'the data observed ' + str(observedEnergy) + 'kWh of expenditure'

measured = measured[48:]+measured[:48]
t2 = np.linspace(4,28,num=288)
plt.plot(t2,measured,'r',label='ENWL Model')
x = np.linspace(6,26,num=6)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(x, my_xticks)
plt.xlim((4,28))
plt.xlabel('time')
plt.ylabel('power (kW)')
plt.legend(loc='upper left')
plt.show()
