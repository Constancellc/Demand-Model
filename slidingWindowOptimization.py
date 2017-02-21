# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

from cvxopt import matrix, spdiag, solvers, sparse

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle
from vehicleOriented import Vehicle, JourneyPool, Agent, Fleet, Simulation, ChargingScheme

"""
I THINK THIS FILE IS GOING TO CONTAIN ALL OF THE OPTIMIZATION DATA COLLECTION
"""
regionType = 'Urban City and Town'
region = ''
month = 'January' # don't use december, i only have 6 days of ng data for it
day = 'Wednesday' # using sunday dodge as next day assumptions very bad
population = 150200

outFile = 'chargingDemand.csv'
fleetSize = 10
scale = float(fleetSize)/25800000
timeInterval = 10 # mins
pMax = 4.0 # kW

nHours = 24+4 # the number of hours I want to simulate

# CHOSE OBJECTIVE 1 - VALLEY FILLING, 2 - LOAD FLATTENING, 3 - SOLAR
obj = 1

t = nHours*(60/timeInterval)

# starting with the charging demand
simulation = Simulation(regionType,month,day,population,1,f=int(400/fleetSize))
results = simulation.getSubsetBookendTimesandEnergy(fleetSize,t,
                                                    timeInterval)

n = len(results)

# ------------------------------------------------------------------------------
# DUMB CHARGING SECTION
# ------------------------------------------------------------------------------

dumbCharging = [0]*t
for j in range(0,n):
    time = results[j][0]
    energy = results[j][1] # kWh
    while energy > 0:
        if energy > (timeInterval/60)*4:
            
            if time == t-1:
                print 'im not fully charged :('
                print energy
                energy = 0
            else:
                dumbCharging[time] += 4
                time += 1
                energy -= (float(timeInterval)/60)*4
        else:
            dumbCharging[time] += energy
            energy = 0
print dumbCharging
# the first equality constraint ensures the right amount of charge is recovered
# the second ensures that only avalible vehicles are plugged in

# ------------------------------------------------------------------------------
# GETTING NATIONAL GRID DATA
# ------------------------------------------------------------------------------

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

dayOne = []
dayTwo = []

with open('ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #print str(calender[month][day])+'-'+month[:3]+'-16'
        if row[0] == str(calender[month][day])+'-'+month[:3]+'-16':
            dayOne.append(scale*1000*float(row[4]))
        elif row[0] == str(calender[month][day]+1)+'-'+month[:3]+'-16':
            dayTwo.append(scale*1000*float(row[4]))
            
# 4AM on first day to 8AM on second
nd = dayOne[8:]+dayTwo[0:(8+(nHours-24)*2)]

# interpolate data to obtain the correct resolution
baseLoad = []

for i in range(0,t):
    r = i%(30/timeInterval)
    if r == 0:
        if i*timeInterval/30 == nHours*2:
            i -= 1
        baseLoad.append(float(int(100*nd[i*timeInterval/30]))/100)
    else:
        f = float(r)/(30/timeInterval)

        p1 = int(i*timeInterval/30)
        p2 = p1+1
        if p2 == nHours*2: # this is a hack
            p2 -= 1

        # rounding to integer just because I feel like it
        baseLoad.append(float(int(100*(nd[p1]+f*(nd[p2]-nd[p1]))))/100)


# ------------------------------------------------------------------------------
# SETTING UP THE OPTIMIZATION PROBLEM
# ------------------------------------------------------------------------------
def optimize(pluggedIn,t0,m):
    # constraints
    # The equality constraint ensures the required amount of energy is delivered 
    A1 = matrix(0.0,(m,(t-t0)*m))
    A2 = matrix(0.0,(m,(t-t0)*m))
    b = matrix(0.0,(2*m,1))

    for j in range(0,m):
        b[j] = float(pluggedIn[j][1]) 
        for i in range(0,t-t0):
            A1[m*((t-t0)*j+i)+j] = float(timeInterval)/60 # kWh -> kW
            if i < pluggedIn[j][0] or i > pluggedIn[j][2]:
                A2[m*((t-t0)*j+i)+j] = 1.0

    A = sparse([A1,A2])

    A3 = spdiag([-1]*((t-t0)*m))
    A4 = spdiag([1]*((t-t0)*m))

    # The inequality constraint ensures powers are positive and below a maximum
    G = sparse([A3,A4])

    h = []
    for i in range(0,2*(t-t0)*m):
        if i<t*m:
            h.append(0.0)
        else:
            h.append(pMax)
    h = matrix(h)

    # objective

    if obj == 1:
        q = []
        for i in range(0,m):
            for j in range(t0,len(baseLoad)):
                q.append(baseLoad[j])

        q = matrix(q)
    elif obj == 2:
        q = matrix([0.0]*((t-t0)*m))

    if obj == 1 or obj == 2 or obj == 3:
        I = spdiag([1]*(t-t0))
        P = sparse([[I]*m]*m)

    sol=solvers.qp(P, q, G, h, A, b)
    X = sol['x']
    return X

# ------------------------------------------------------------------------------
# RUNNING THE OPTIMIZATION
# ------------------------------------------------------------------------------

pluggedIn = []
chargeProfiles = {}

for t0 in range(0,t):
    # add new vehicles to the set we care about
    for i in range(0,n):
        if results[i][0] == t0:
            pluggedIn.append(results[i])
            chargeProfiles[results[i][3]] = [0.0]*t

    # how many vehicles do we currently have plugged in?
    m = len(pluggedIn)

    if m > 0:
        print pluggedIn
        X = optimize(pluggedIn,t0,m)
        # X is a vector with length (t-t0)*m
        for i in range(0,m):
            # update the immediate charging values
            print i*(t-t0)
            chargeProfiles[pluggedIn[i][3]][t0] = X[i*(t-t0)]
            # fill the vehicle battery with the right amount of energy
            pluggedIn[i][1] -= X[i*(t-t0)]*float(timeInterval)/60

            # check if the vehicle is done charging, it is is unplug
            if pluggedIn[i][1] <= 0.1:
                pluggedIn.remove(pluggedIn[i])



# ------------------------------------------------------------------------------
# GRAPH PLOTTING SECTION
# ------------------------------------------------------------------------------


