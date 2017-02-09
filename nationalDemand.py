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

month = 'January'
day = 'Wednesday'

totalPopulation = 53010000
regionBreakdown = {'Urban Conurbation':0.369,'Urban City and Town':0.446,
                   'Rural Town and Fringe':0.092,
                   'Rural Village, Hamlet and Isolated Dwelling':0.093}

demand = [0]*(24*60)

for region in regionBreakdown:
    population = regionBreakdown[region]*totalPopulation
    simulation = Simulation(region, month, day, population, 0)
    
    test = ChargingScheme(simulation.fleet,24*60)
    test.allHomeCharge(4,simulation.factor)
    for i in range(0,24*60):
        demand[i] += test.powerDemand[i]/1000

plt.figure(1)

t1 = np.linspace(4,28,num=24*60)
#plt.plot(t1,demand,label='EV Charging')

data = []

# find right date for day of the week
calender = {'January':{'Monday':11,'Tuesday':12,'Wednesday':13,'Thursday':14,
                       'Friday':15,'Saturday':16,'Sunday':17},
            'February':{'Monday':15,'Tuesday':16,'Wednesday':17,'Thursday':18,
                       'Friday':19,'Saturday':20,'Sunday':21},
            'March':{'Monday':14,'Tuesday':15,'Wednesday':16,'Thursday':17,
                       'Friday':18,'Saturday':19,'Sunday':20},
            'April':{'Monday':11,'Tuesday':12,'Wednesday':13,'Thursday':14,
                       'Friday':15,'Saturday':16,'Sunday':17},
            'May':{'Monday':16,'Tuesday':17,'Wednesday':18,'Thursday':19,
                       'Friday':20,'Saturday':21,'Sunday':22},
            'June':{'Monday':13,'Tuesday':14,'Wednesday':15,'Thursday':16,
                       'Friday':17,'Saturday':18,'Sunday':19},
            'July':{'Monday':11,'Tuesday':12,'Wednesday':13,'Thursday':14,
                       'Friday':15,'Saturday':16,'Sunday':17},
            'August':{'Monday':15,'Tuesday':16,'Wednesday':17,'Thursday':18,
                       'Friday':19,'Saturday':20,'Sunday':21},
            'September':{'Monday':12,'Tuesday':13,'Wednesday':14,'Thursday':15,
                       'Friday':16,'Saturday':17,'Sunday':18},
            'October':{'Monday':17,'Tuesday':18,'Wednesday':19,'Thursday':20,
                       'Friday':21,'Saturday':22,'Sunday':23},
            'November':{'Monday':14,'Tuesday':15,'Wednesday':16,'Thursday':17,
                       'Friday':18,'Saturday':19,'Sunday':20},
            'December':{'Monday':12,'Tuesday':13,'Wednesday':14,'Thursday':15,
                       'Friday':16,'Saturday':17,'Sunday':18}}

with open('ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #print str(calender[month][day])+'-'+month[:3]+'-16'
        if row[0] == str(calender[month][day])+'-'+month[:3]+'-16':
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


per10 = [0]*(24*60)
per20 = [0]*(24*60)
per30 = [0]*(24*60)
per40 = [0]*(24*60)

for i in range(0,24*60):
    per10[i] = demand[i]*0.1+interpolated[i]
    per20[i] = demand[i]*0.2+interpolated[i]
    per30[i] = demand[i]*0.3+interpolated[i]
    per40[i] = demand[i]*0.4+interpolated[i]


t2 = np.linspace(4,28,num=24*2)
plt.plot(t2,nd,label='National Demand')

#plt.plot(t1,summed,label='With EV Charging')
plt.plot(t1,per10,label='10%')
plt.plot(t1,per20,label='20%')
plt.plot(t1,per30,label='30%')
plt.plot(t1,per40,label='40%')
plt.plot(t1,summed,label='100%')

x = np.linspace(6,26,num=6)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(x, my_xticks)
plt.xlim((4,28))
plt.ylim((0,70000))
plt.xlabel('time')
plt.ylabel('power demand (MW)')
plt.legend(loc='lower left')
plt.show()
