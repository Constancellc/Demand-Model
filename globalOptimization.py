# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import copy

from cvxopt import matrix, spdiag, solvers, sparse

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle
from vehicleOriented import Vehicle, JourneyPool, Agent, Fleet, Simulation, ChargingScheme

regionType = 'Urban City and Town'
region = ''
month = 'June' # don't use december, i only have 6 days of ng data for it
day = 'Wednesday' # using sunday dodge as next day assumptions very bad
population = 150200

outFile = 'chargingDemand.csv'
fleetSize = 40
scale = float(fleetSize)/25800000
timeInterval = 10 # mins
pMax = 4.0 # kW

nHours = 24+4 # the number of hours I want to simulate

# CHOSE OBJECTIVE 1 - VALLEY FILLING, 2 - LOAD FLATTENING, 3 - SOLAR
obj = 3

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
# GETTING PV DATA
# ------------------------------------------------------------------------------

times = []
powers = []

months = {'January':'01','February':'02','March':'03','April':'04','May':'05',
          'June':'06','July':'07','August':'08','September':'09',
          'October':'10','November':'11','December':'12'}

with open('../Documents/av_solar.csv','rU') as csvfile:
    # this data is at 10 min intervals
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            print row[0]
        except:
            continue

        if row[0] == months[month]:
            rawData = row[1:]

oneDayPV = [0.0]*(24*60/timeInterval)

f = float(144)/(24*60/timeInterval)

for i in range(0,(24*60/timeInterval)):
    oneDayPV[i] = float(rawData[int(i*f)])*fleetSize

pv = oneDayPV[4*(60/timeInterval):]+oneDayPV[:(nHours-20)*(60/timeInterval)]

'''

pvDay = str(calender[month][day])
months = {'January':'01','February':'02','March':'03','April':'04','May':'05',
          'June':'06','July':'07','August':'08','September':'09',
          'October':'10','November':'11','December':'12'}
pvMonth = months[month]

if obj == 3:
    with open('pv/GBPV_data.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'substation_id':
                continue
            
            if row[1][8:10] != pvDay:
                continue
            elif row[1][5:7] != pvMonth:
                continue
            
            hour = int(row[1][11:13])-4
            mins = int(row[1][14:16])
            time = hour*(60/timeInterval)+int(mins/timeInterval)
            times.append(time)
            powers.append(scale*1000*float(row[2]))

    pv = [0.0]*t

    for i in range(0,t):
        if i < times[0]:
            continue
        elif i > times[-1]:
            continue

        gap = times[1]-times[0]

        j = 0
        while times[j] < i and j < t-1:
            j += 1

        distance = times[j] - i
        f = float(distance)/gap

        pv[i] = float(int(100*(powers[j]+f*(powers[j-1]-powers[j]))))/100
'''
# ------------------------------------------------------------------------------
# SETTING UP THE OPTIMIZATION PROBLEM
# ------------------------------------------------------------------------------

def optimize(obj):
    # constraints
    # The equality constraint ensures the required amount of energy is delivered 
    A1 = matrix(0.0,(n,t*n))
    A2 = matrix(0.0,(n,t*n))
    b = matrix(0.0,(2*n,1))

    for j in range(0,n):
        b[j] = float(results[j][1]) 
        for i in range(0,t):
            A1[n*(t*j+i)+j] = float(timeInterval)/60 # kWh -> kW
            if i < results[j][0] or i > results[j][2]:
                A2[n*(t*j+i)+j] = 1.0

    A = sparse([A1,A2])

    A3 = spdiag([-1]*(t*n))
    A4 = spdiag([1]*(t*n))

    # The inequality constraint ensures powers are positive and below a maximum
    G = sparse([A3,A4])

    h = []
    for i in range(0,2*t*n):
        if i<t*n:
            h.append(0.0)
        else:
            h.append(pMax)
    h = matrix(h)

    # objective

    if obj == 1:
        q = []
        for i in range(0,n):
            for j in range(0,len(baseLoad)):
                q.append(baseLoad[j])

        q = matrix(q)
    elif obj == 2:
        q = matrix([0.0]*(t*n))

    if obj == 3:
        q = []
        for i in range(0,n):
            for j in range(0,len(baseLoad)):
                q.append(baseLoad[j]-pv[j])

        q = matrix(q)

    if obj == 1 or obj == 2 or obj == 3:
        I = spdiag([1]*t)
        P = sparse([[I]*n]*n)

    sol=solvers.qp(P, q, G, h, A, b)
    X = sol['x']

    return X

# ------------------------------------------------------------------------------
# GRAPH PLOTTING SECTION
# ------------------------------------------------------------------------------

X = optimize(obj)
X0 = optimize(2)

x = np.linspace(4,nHours+4,num=nHours*60/timeInterval)

averageProfile = [0.0]*t

plt.figure(1)


plt.subplot(312)
summed = [0.0]*t
if obj == 3:
    summed2 = [0.0]*t
    pvcopy = copy.copy(pv)
for i in range(0,n):
    data = []
    for j in range(0,t):
        data.append(X[i*t+j])
        summed[j] += X0[i*t+j]
        if obj == 3:
            summed2[j] += X[i*t+j]
            if pvcopy[j] > 0:
                if pvcopy[j] >= X[i*t+j]:
                    pvcopy[j] -= X[i*t+j]
                    summed2[j] -= X[i*t+j]
                else:
                    pvcopy[j] = 0
                    summed2[j] -= pvcopy[j]
                    
        averageProfile[j] += X[i*t+j]/n
    plt.plot(x,data)
xaxis = np.linspace(6,30,num=7)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00','06:00']
plt.xticks(xaxis, my_xticks)
plt.xlim((4,4+nHours))
plt.ylim((0,5.5))
plt.ylabel('Power (kW)')
plt.title('Individual Charge Profiles for Smart Charging',y=0.8)

plt.subplot(311)

for j in range(0,t):
    summed[j] += baseLoad[j]
    if obj == 3:
        summed2[j] += baseLoad[j]
    dumbCharging[j] += baseLoad[j]

plt.plot(x,summed,label='Smart Charging')
if obj == 3:
    plt.plot(x,summed2,label='Smart Charging with Solar')
plt.plot(x,baseLoad,label='Scaled Base Load')
plt.plot(x,dumbCharging,label='Dumb Charging')
if obj ==3:
    plt.plot(x,pv,label='PV')

plt.xticks(xaxis, my_xticks)
plt.xlim((4,4+nHours))
plt.ylabel('Power (kW)')
plt.legend(loc='upper left')
plt.title('Aggregate Power Demand')

plt.subplot(313)
plt.plot(x,averageProfile)
plt.xticks(xaxis, my_xticks)
plt.xlim((4,4+nHours))
plt.ylim((0,1.5))
plt.ylabel('Power (kW)')
plt.title('Average Charge Profile',y=0.8)
plt.xlabel('time')


plt.show()
