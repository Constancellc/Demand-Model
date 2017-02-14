# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle
from vehicleOriented import Vehicle, JourneyPool, Agent, Fleet, Simulation, ChargingScheme

"""
I THINK THIS FILE IS GOING TO CONTAIN ALL OF THE OPTIMIZATION DATA COLLECTION
"""
regionType = 'Urban City and Town'
region = ''
month = 'May'
day = 'Wednesday'
population = 150200

outFile = 'chargingDemand.csv'
fleetSize = 10
timeInterval = 15

# starting with the charging demand
simulation = Simulation(regionType,month,day,population,0)
results = simulation.getSubsetFinalArrivalandEnergy(fleetSize,timeInterval)

print results
with open(outFile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(results)

# now baseLoad
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

# offset the day to 4AM
nd = data[8:]+data[0:8]

# ok lets turn this 30 minute data into the correct resolution...

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
