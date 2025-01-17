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
month = 'January'
day = 'Wednesday'
population = 150200



outFile = 'chargingDemand.csv'
fleetSize = 20
scale = float(fleetSize)/25800000
timeInterval = 15 # mins
pMax = 4.0 # kW

# starting with the charging demand
simulation = Simulation(regionType,month,day,population,0)
results = simulation.getSubsetFinalArrivalandEnergy(fleetSize,timeInterval)

n = len(results)
t = 24*(60/timeInterval)

# it would be nice to be able to compare to the unoptimized case
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

A1 = matrix(0.0,(n,t*n))
A2 = matrix(0.0,(n,t*n))
b1 = matrix(0.0,(2*n,1))

for j in range(0,n):
    b1[j] = float(results[j][1]) 
    for i in range(0,t):
        A1[n*(t*j+i)+j] = float(timeInterval)/60 # kWh -> kW
        if i < results[j][0]:
            A2[n*(t*j+i)+j] = 1.0
            #A2[n*i+j*(t*n+1)] = 1.0

# the first inequality constraint prevents negative powers, the second limits
# the size of the charging power

A3 = spdiag([-1]*(t*n))
A4 = spdiag([1]*(t*n))

print results

Aeq = sparse([A1,A2])
#beq = sparse([b1,b2])

Aineq = sparse([A3,A4])


# if u want 2 store results

#with open(outFile,'w') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerows(results)


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

data = []

with open('ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #print str(calender[month][day])+'-'+month[:3]+'-16'
        if row[0] == str(calender[month][day])+'-'+month[:3]+'-16':
            data.append(scale*1000*float(row[4]))

# offset the day to 4AM
nd = data[8:]+data[0:8]

# ok lets turn this 30 minute data into the correct resolution...

baseLoad = []

for i in range(0,t):
    r = i%(30/timeInterval)
    if r == 0:
        if i*timeInterval/30 == 48:
            i -= 1
        baseLoad.append(float(int(100*nd[i*timeInterval/30]))/100)
    else:
        f = float(r)/(30/timeInterval)

        p1 = int(i*timeInterval/30)
        p2 = p1+1
        if p2 == 48: # this is a hack
            p2 -= 1

        # rounding to integer just because I feel like it
        baseLoad.append(float(int(100*(nd[p1]+f*(nd[p2]-nd[p1]))))/100)

print baseLoad
b = []
for i in range(0,n):
    for j in range(0,len(baseLoad)):
        b.append(baseLoad[j])

q = matrix(b)

I = spdiag([1]*t)
P = sparse([[I]*n]*n)

A = Aeq
b = b1

G = Aineq

bineq = []
for i in range(0,2*t*n):
    if i<t*n:
        bineq.append(0.0)
    else:
        bineq.append(pMax)
h = matrix(bineq)

sol=solvers.qp(P, q, G, h, A, b)
X = sol['x']
#print X

x = np.linspace(4,28,num=24*60/timeInterval)

plt.figure(1)

plt.subplot(212)
summed = [0.0]*t
for i in range(0,n):
    data = []
    for j in range(0,t):
        data.append(X[i*t+j])
        summed[j] += X[i*t+j] 
    plt.plot(x,data)
xaxis = np.linspace(6,26,num=6)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(xaxis, my_xticks)
plt.xlim((4,28))
plt.xlabel('time')
plt.ylabel('Power (kW)')
plt.title('Individual Charge Profiles for Smart Charging')

plt.subplot(211)

for j in range(0,t):
    summed[j] += baseLoad[j]
    dumbCharging[j] += baseLoad[j]

plt.plot(x,summed,label='Smart Charging')
plt.plot(x,baseLoad,label='Scaled Base Load')
plt.plot(x,dumbCharging,label='Dumb Charging')

plt.xticks(xaxis, my_xticks)
plt.xlim((4,28))
plt.ylabel('Power (kW)')
plt.legend(loc='upper left')
plt.title('Aggregate Power Demand')


plt.show()
