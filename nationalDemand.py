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



# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------

month = 'May'
day = 'Wednesday'

totalPopulation = 53010000
regionBreakdown = {'Urban Conurbation':0.369,'Urban City and Town':0.446,
                   'Rural Town and Fringe':0.092,
                   'Rural Village, Hamlet and Isolated Dwelling':0.093}

demand = [0]*(24*60)

for region in regionBreakdown:
    population = regionBreakdown[region]*totalPopulation
    simulation = Simulation(region, month, day, population)
    
    test = ChargingScheme(simulation.fleet)
    test.allHomeCharge(4,simulation.factor)
    for i in range(0,24*60):
        demand[i] += test.powerDemand[i]/1000

plt.figure(1)

t1 = np.linspace(4,28,num=24*60)
plt.plot(t1,demand,label='EV Charging')

data = []

with open('ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == '18-May-16':
            data.append(float(row[4]))

nd = data[8:]+data[0:8]

# ok lets turn this 30 minute data into 1min data...

interpolated = []
summed = []

for i in range(0,24*60):
    if i%30 == 0:
        interpolated.append(nd[i/30])
    else:
        f = float((i%30))/30
        p1 = int(i/30)
        p2 = p1+1
        if p2 == 48: # this is a hack
            p2 -= 1
        interpolated.append(nd[p1]+f*(nd[p2]-nd[p1]))
    summed.append(demand[i]+interpolated[i])

t2 = np.linspace(4,28,num=24*2)
plt.plot(t2,nd,label='National Demand')

plt.plot(t1,summed,label='With EV Charging')
x = np.linspace(6,26,num=6)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(x, my_xticks)
plt.xlim((4,28))
plt.xlabel('time')
plt.ylabel('power demand (MW)')
plt.legend(loc='upper left')
plt.show()
