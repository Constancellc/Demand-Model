# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

from cvxopt import matrix, spdiag, solvers, sparse

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle, Vehicle
from vehicleOriented import JourneyPool, Agent, Fleet, Simulation, ChargingScheme

"""
I THINK THIS FILE IS GOING TO CONTAIN ALL OF THE OPTIMIZATION DATA COLLECTION
"""
month = 'July' # don't use december, i only have 6 days of ng data for it
day = 'Wednesday' # using sunday dodge as next day assumptions very bad
population = 150200

outFile = 'chargingDemand.csv'
timeInterval = 15 # mins
pMax = 4.0 # kW

nHours = 48 # the number of hours I want to simulate


# CHOSE OBJECTIVE 1 - VALLEY FILLING, 2 - LOAD FLATTENING, 3 - SOLAR
obj = 1

t = nHours*(60/timeInterval)

# starting with the charging demand


regionBreakdown = {'Urban Conurbation':37,'Urban City and Town':45,
                   'Rural Town and Fringe':9,
                   'Rural Village, Hamlet and Isolated Dwelling':9}

plotMonths = ['January','April','July','October']
plt.figure(1)

for k in range(0,4):
    month = plotMonths[k]
    results = []

    for regionType in regionBreakdown:
        fleetSize = regionBreakdown[regionType]
        simulation = Simulation(regionType,month,day,population,1,
                                f=int(400/fleetSize))
        results += simulation.getSubsetBookendTimesandEnergy(fleetSize,t,
                                                            timeInterval)
        
    scale = 100.0/25800000
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
    dayThree = []

    with open('ng-data/Demand_Data2016.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print str(calender[month][day])+'-'+month[:3]+'-16'
            if row[0] == str(calender[month][day])+'-'+month[:3]+'-16':
                dayOne.append(scale*1000*float(row[4]))
            elif row[0] == str(calender[month][day]+1)+'-'+month[:3]+'-16':
                dayTwo.append(scale*1000*float(row[4]))
            elif row[0] == str(calender[month][day]+2)+'-'+month[:3]+'-16':
                dayTwo.append(scale*1000*float(row[4]))
                
    # 4AM on first day to 8AM on second
    nd = dayOne[8:]+dayTwo+dayThree[0:8]

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

    # ------------------------------------------------------------------------------
    # SETTING UP THE OPTIMIZATION PROBLEM
    # ------------------------------------------------------------------------------


    # constraints
    # The equality constraint ensures the required amount of energy is delivered 
    A1 = matrix(0.0,(n,t*n))
    A2 = matrix(0.0,(n,t*n))
    b = matrix(0.0,(2*n,1))

    for j in range(0,n):
        b[j] = float(results[j][1]) 
        for i in range(0,t):
            A1[n*(t*j+i)+j] = float(timeInterval)/60 # kWh -> kW
            if i < results[j][0] or (i > results[j][2] and i < (results[j][0]+t/2)):
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
                q.append(pv[j]+baseLoad[j])

        q = matrix(q)

    if obj == 1 or obj == 2 or obj == 3:
        I = spdiag([1]*t)
        P = sparse([[I]*n]*n)

    sol=solvers.qp(P, q, G, h, A, b)
    X = sol['x']

    # ------------------------------------------------------------------------------
    # GRAPH PLOTTING SECTION
    # ------------------------------------------------------------------------------

    x = np.linspace(4,nHours+4,num=nHours*60/timeInterval)

    averageProfile = [0.0]*t
    numPluggedIn = [0.0]*t

    plt.subplot(2,2,k+1)
    summed = [0.0]*t
    for i in range(0,n):
        for j in range(0,t):
            summed[j] += X[i*t+j]
            if X[i+t+j] >= 0.1:
                numPluggedIn[j] += 1
            averageProfile[j] += X[i*t+j]/n

    xaxis = np.linspace(6,54,num=13)
    my_xticks = ['06:00','10:00 \n Wed','16:00','18:00','22:00','02:00','06:00','10:00 \n Thur','16:00','18:00','22:00','02:00','06:00']



    for j in range(0,t):
        summed[j] += baseLoad[j]
        dumbCharging[j] += baseLoad[j]

    scale = scale*1000000
    
    for j in range(0,t):
        dumbCharging[j] = dumbCharging[j]/scale
        summed[j] = summed[j]/scale
        baseLoad[j] = baseLoad[j]/scale
        

    plt.plot(x,baseLoad,label='Scaled Base Load')
    plt.plot(x,dumbCharging,label='Dumb Charging')
    plt.plot(x,summed,label='Smart Charging')
    if obj ==3:
        plt.plot(x,pv,label='PV')

    plt.xticks(xaxis, my_xticks)
    plt.xlim((9,40))
    plt.ylabel('Power (GW)')
    if k == 0:
        plt.legend(loc=[0.5,-1.5],ncol=3)
    plt.title(month,y=0.85)
    plt.ylim(20,80)
    plt.xlabel('time')
    plt.grid()
#plt.title('Aggregate Power Demand')



#plt.figure(2)
#plt.plot(x,numPluggedIn)
#plt.xticks(xaxis, my_xticks)
#plt.xlim((10,40))

plt.show()
