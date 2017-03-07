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
month = 'January' # don't use december, i only have 6 days of ng data for it
day = 'Wednesday' # using sunday dodge as next day assumptions very bad
population = 150200
fleetSize = 100

simulation = Simulation(regionType,month,day,population,1,f=int(400/fleetSize))
test = ChargingScheme(simulation.fleet)
test.allHomeCharge(3.5,1)

results = simulation.fleet.generateChargeProfiles(55,3.5)

plt.figure(1)
for i in range(0,55):
    plt.plot(results[i])
    with open('evprofiles/'+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(results[i])

plt.show()
