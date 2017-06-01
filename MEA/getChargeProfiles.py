import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
from cvxopt import matrix, spdiag, solvers, sparse

# ok, i'm re-booting this script
# it will now:
# - select 55 random MEA profiles from the same feeder
# - work out the nationally valley filling version of their profiles     
# - work out their household valley filling profiles
# - work out their network valley filling profiles
# - save the results into a csv files

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges2.csv'
rangeData =  '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'

# define the location for the output csv files to be stored
dumbStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/unchanged/'
nationalStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/national/'
householdStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/household/'
networkStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/network/'

# create dictionaries to store the final profiles
dumbProfiles = {}
nationalProfiles = {}
householdProfiles = {}
networkProfiles = {}

power = 3.5 # kW
pMax = 4.0 # kW
#pDiffMax = 1.0 # kW
deadline = 9 # AM
interval = 1 # minutes, for the network optimization

startDates = {}
chargeStarts = {}
latest = datetime.datetime(2010,01,01)

# first find the car which started recording the latest
with open(rangeData, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0][:3] != 'ST1':
            continue
        if row[0] not in startDates:
            startDates[row[0]] = datetime.datetime(int(row[1][:4]),
                                                   int(row[1][5:7]),
                                                   int(row[1][8:10]))
            if startDates[row[0]] > latest:
                latest = startDates[row[0]]

# then skip 3 weeks to ensure all car users have gotten used to the vehicles
latest += datetime.timedelta(21) # skip nervous weeks

# skip until you reach a Tuesday, so that all days considered will be normal weekdays
while latest.isoweekday() != 2: # pick a tuesday for day 1
    latest += datetime.timedelta(1)



energy = {} # stores energy required on each day
tripStarts = {} # stores first departure tip on each day
chargeStarts = {} # stores the final plug in time on each day 

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0][:3] != 'ST1': # only considering this feeder
            continue

        if row[0] not in dumbProfiles:
            dumbProfiles[row[0]] = [0]*(72*60)
            chargeStarts[row[0]] = {0:0,1:0,2:0}
            energy[row[0]] = {0:0,1:0,2:0}
            tripStarts[row[0]] = {0:24*60,1:24*60,2:24*60}

        # get the index of the day in the vehicles reference frame
        reqDay = (latest-startDates[row[0]]).days # this is actualy the day before

        dayNo = int(row[1]) - reqDay
        
        if dayNo > 2 or dayNo < 0:
            continue

        startTime = int(row[2])+dayNo*24*60
        endTime = int(row[3])+dayNo*24*60

        if int(row[2]) > chargeStarts[row[0]][dayNo]:
            chargeStarts[row[0]][dayNo] = int(row[2])

        # if all is well, no weekend journeys should reach this point
        weekendFlag = int(row[6])
        if weekendFlag == 1: 
            print 'fuck'
            continue

        for i in range(startTime,endTime):
            if i >= 72*60:
                continue
            dumbProfiles[row[0]][i] = power

        energy[row[0]][dayNo] += float(endTime-startTime)*power/60 # kWh

# now I want to get rid of all but 55 profiles

# first get a list of the vehicle IDs
allVehicles = []
for vehicle in dumbProfiles:
    allVehicles.append(vehicle)

while len(dumbProfiles) > 55:
    vehicleToBeDeleted = allVehicles[int(random.random()*len(allVehicles))]
    del dumbProfiles[vehicleToBeDeleted]
    allVehicles.remove(vehicleToBeDeleted)
# now only 55 remain, their index in the vector allVehicles will refer totheir csv file number

# next i need to find out when each vehicle will first be needed the next day
with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] not in allVehicles:
            continue

        reqDay = (latest-startDates[row[0]]).days # this is actualy the day before
        dayNo = int(row[1]) - reqDay

        if dayNo > 2 or dayNo < 0:
            continue

        tripStart = int(row[2])

        if tripStart < tripStarts[row[0]][dayNo]:
            tripStarts[dayNo] = tripStart

# now i need to import the relevant national baseload
baseloadDay1 = []
baseloadDay2 = []
baseloadDay3 = []

with open('../ng-data/Demand_Data2016.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == '13-Apr-16':
                baseloadDay1.append(float(row[4])/28000)
            elif row[0] == '14-Apr-16':
                baseloadDay2.append(float(row[4])/28000)
            elif row[0] == '15-Apr-16':
                baseloadDay3.append(float(row[4])/28000)

baseLoad30 = baseloadDay1 + baseloadDay2 + baseloadDay3
baseLoad30.append(baseLoad30[-1]) # repeat last element to avoid interpolation problems

# now turn the 30 minute data into 1 minute resolution data
baseLoad = []
t_int = 30 # number of intervals in 30 mins

for i in range(0,len(baseLoad30)-1):
    for j in range(0,t_int):
        baseLoad.append(((t_int-j)*baseLoad30[i]+j*baseLoad30[i+1])/t_int)

households = {}

for i in range(1,56):
    profile = []
    with open('../../Documents/lv_test_feeder/Load_profile_'+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            profile.append(float(row[1]))
    households[allVehicles[i-1]] = copy.copy(profile+profile+profile)

# I also need to get the LV household profiles
def individual_smart_charge(start,end,energy,version,interval=1,vehicleID=''):
    t = end-start

    if version == 'national':
        b = copy.copy(baseLoad[start:end])
    elif version == 'household':
        b = households[vehicleID][start:end]

    q = matrix(b)
    
    A = matrix(1.0/(2*t_int),(1,t))

    b = matrix([energy]) # amount of energy needed in.... kWh?

    A3 = spdiag([-1]*t)
    A4 = spdiag([1]*t)
    G = sparse([A3,A4])

    h = matrix([0.0]*t + [pMax]*t)
    
    P = spdiag([1]*t)
    sol = solvers.qp(P,q,G,h,A,b)
    X = sol['x']

    del b

    return X

for vehicle in allVehicles:
    nationalProfiles[vehicle] = [0]*(72*60)
    householdProfiles[vehicle] = [0]*(72*60)
    networkProfiles[vehicle] = [0]*((48+deadline)*60) # this enforces charging by 9AM
    for day in range(0,2):
        energyReq = energy[vehicle][day]
        
        start = chargeStarts[vehicle][day]+day*24*60

        end = tripStarts[vehicle][day+1]
        
        lim = int(60*(deadline+np.random.normal(0,0.5)))
        if end < lim: # be charged by morning deadline regardless
            end += (day+1)*24*60
        else:
            end = lim+(day+1)*24*60
        
        if energyReq == 0:
            continue

        X = individual_smart_charge(start,end,energyReq,'national')
        for j in range(0,len(X)):
                nationalProfiles[vehicle][start+j] += X[j]
                
        X = individual_smart_charge(start,end,energyReq,'household',vehicleID=vehicle)
        for j in range(0,len(X)):
                householdProfiles[vehicle][start+j] += X[j]


# the last problem requires one big optimisation... which I'm HOPING will be tractable

n = 55*2
t = (48+deadline)*60/interval 

energy_req = []
sum_households = [0.0]*(24*60/interval)
unused = []

starts = []
ends = []

#A_diff = []
#A_diffR = 0

for j in range(0,55*2):
    vehicle = allVehicles[int(j/2)]
    day = j%2
    
    if day == 0:
        profile = households[vehicle]
        tot = 0
        for i in range(0,24*60):
            tot += profile[i]
            if i%interval == 0:
                sum_households[i/interval] += tot/interval
                tot = 0
            
    if energy[vehicle][day] == 0:
        n -= 1
        unused.append(j)
        continue
   
    energy_req.append(energy[vehicle][day])

    start = chargeStarts[vehicle][day]+day*24*60
    end = tripStarts[vehicle][day+1]

    if end > 9*60:
        end = 9*60+(day+1)*24*60
    else:
        end += (day+1)*24*60

    start = int(start/interval)+1
    end = int(end/interval)-1       

    starts.append(start)
    ends.append(end)

'''
for i in range(0,n):
    for j in range(starts[i],ends[i]-1):
        row = [0.0]*n*t
        row[t*i+j] = 1.0
        row[t*i+j+1] = -1.0
        A_diff += row
        A_diffR += 1
'''        
# first let's deal with the objective function
I = spdiag([1]*t)
P = sparse([[I]*n]*n)

sum_households = sum_households+sum_households+sum_households[:deadline*60/interval]
q = []
for i in range(0,n):
    q += sum_households
q = matrix(q)

# and now the constranints: equality first
A_en = matrix(0.0,(n,t*n)) # en: energy required
for i in range(0,n):
    for j in range(0,t):
        A_en[n*t*i+j*n+i] = 1.0*interval/60
        
A_av = matrix(0.0,(n,t*n)) # av: avaliability
for i in range(0,n):
    for j in range(0,t):
        if j < starts[i] or j > ends[i]:
            A_av[n*t*i+j*n+i] = 1.0

A = matrix([A_en,A_av])
b = matrix(energy_req+[0.0]*n)

# and inequality
'''
A_diff = matrix(0.0,(n*(t-1),n*t)) # diff: change in power
for i in range(0,n):
    for j in range(0,t-1):
        A_diff[(i*t+j)*n*(t-1)+i*(t-1)+j] = -1.0
        A_diff[(i*t+j+1)*n*(t-1)+i*(t-1)+j] = 1.0
'''

#A_diff = matrix(A_diff,(A_diffR,n*t))


# ok so here's the deal the above will limit the rate at which charging can
# increase but not decrease, but this may be sufficient

A_pos = spdiag([-1.0]*n*t) # keeps powers positive
A_lim = spdiag([1.0]*n*t) # limits powers below a maximum

#G = matrix([A_diff,sparse([A_pos,A_lim])])
G = sparse([A_pos,A_lim])
#h = matrix([pDiffMax]*A_diffR + [0.0]*t*n + [pMax]*t*n)
h = matrix([0.0]*t*n + [pMax]*t*n)

sol=solvers.qp(P, q, G, h, A, b)
X = sol['x']


c = 0
for j in range(0,55*2):
    vehicle = allVehicles[int(j/2)]

    if j in unused:
        continue

    for i in range(0,(48+deadline)*60/interval):
        for j in range(0,interval):
            networkProfiles[vehicle][i*interval+j] += X[c]
        c += 1


for i in range(0,55):
    with open(dumbStem+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = dumbProfiles[allVehicles[i]][24*60:48*60]
        for cell in profile:
            writer.writerow([cell])
    
    with open(nationalStem+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = nationalProfiles[allVehicles[i]][24*60:48*60]
        for cell in profile:
            writer.writerow([cell])

    
    with open(householdStem+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = householdProfiles[allVehicles[i]][24*60:48*60]
        for cell in profile:
            writer.writerow([cell])

    
    with open(networkStem+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = networkProfiles[allVehicles[i]][24*60:48*60]
        for cell in profile:
            writer.writerow([cell])


