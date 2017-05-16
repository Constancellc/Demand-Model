import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
from cvxopt import matrix, spdiag, solvers, sparse

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges2.csv'
rangeData =  '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'

profileStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/unchanged/'
profileStem2 = '../../Documents/My_Electric_avenue_Technical_Data/profiles/smart/'
profileStem3 = '../../Documents/My_Electric_avenue_Technical_Data/profiles/perturbed/'

power = 3.5

startDates = {}
chargeStarts = {}
latest = datetime.datetime(2010,01,01)

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
                
latest += datetime.timedelta(21) # skip nervous weeks

while latest.isoweekday() != 2: # pick a tuesday for day 1
    latest += datetime.timedelta(1)

profiles = {}
energy = {}

tripStarts = {}


with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0][:3] != 'ST1':
            continue

        if row[0] not in profiles:
            profiles[row[0]] = [0]*(72*60)
            chargeStarts[row[0]] = {0:0,1:0,2:0}
            energy[row[0]] = {0:0,1:0,2:0}
            tripStarts[row[0]] = {0:24*60,1:24*60,2:24*60}
            
        reqDay = (latest-startDates[row[0]]).days # this is actualy the day before

        dayNo = int(row[1]) - reqDay
        
        if dayNo > 2 or dayNo < 0:
            continue

        startTime = int(row[2])+dayNo*24*60
        endTime = int(row[3])+dayNo*24*60

        if int(row[2]) > chargeStarts[row[0]][dayNo]:
            chargeStarts[row[0]][dayNo] = int(row[2])

        weekendFlag = int(row[6])

        if weekendFlag == 1:
            print 'fuck'
            continue

        for i in range(startTime,endTime):
            if i >= 72*60:
                continue
            profiles[row[0]][i] = power

        energy[row[0]][dayNo] += float(endTime-startTime)*power/60 # kWh

allVehicles = []

for vehicle in profiles:
    allVehicles.append(vehicle)

chosenVehicles = []


for i in range(0,55):
    ran = int(random.random()*len(allVehicles))
    chosenVehicles.append(allVehicles[ran])
    allVehicles.remove(allVehicles[ran])

with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] not in chosenVehicles:
            continue

        reqDay = (latest-startDates[row[0]]).days # this is actualy the day before
        dayNo = int(row[1]) - reqDay

        if dayNo > 2 or dayNo < 0:
            continue

        tripStart = int(row[2])

        if tripStart < tripStarts[row[0]][dayNo]:
            tripStarts[dayNo] = tripStart

baseLoad30 = []
day2 = []
day3 = []

with open('../ng-data/Demand_Data2016.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == '13-Apr-16':
                baseLoad30.append(float(row[4])/28000)
            elif row[0] == '14-Apr-16':
                day2.append(float(row[4])/28000)
            elif row[0] == '15-Apr-16':
                day3.append(float(row[4])/28000)
                
baseLoad30 += day2
baseLoad30 += day3

baseLoad = []

baseLoad30.append(baseLoad30[-1])

t_int = 30 # number of intervals in 30 mins

for i in range(0,len(baseLoad30)-1):
    for j in range(0,t_int):
        baseLoad.append(((t_int-j)*baseLoad30[i]+j*baseLoad30[i+1])/t_int)



def smart_charge(start,end,energy,perturb=False):
    t = end-start
    b = copy.copy(baseLoad[start:end])

    if perturb == True:
        # first i want to downsample
        b2 = []
        for i in range(0,len(b)/30):
            b2.append(b[i]*30)
        for i in range(0,len(b2)):
            b2[i] = b2[i]*(1+np.random.normal(0,0.1))
        # now we want to upsample
        b3 = []
        for i in range(0,len(b)/30):
            for j in range(0,30):
                b3.append(b2[i])
        for i in range(0,len(b)%30):
            b3.append(b2[-1])
        b = b3
            
    
    q = matrix(b)
    
    A = matrix(1.0/(2*t_int),(1,t))

    b = matrix([energy]) # amount of energy needed in.... kWh?

    A3 = spdiag([-1]*t)
    A4 = spdiag([1]*t)
    G = sparse([A3,A4])


    h = matrix([0.0]*t + [7.0]*t)
    
    #q = matrix(baseLoad)

    P = spdiag([1]*t)
    sol = solvers.qp(P,q,G,h,A,b)
    X = sol['x']

    del b

    return X


# each vehicle is going to solve its own optimization problem
#t = t_int*48
smartProfiles = {}
smartProfiles2 = {}
for vehicle in chosenVehicles:
    smartProfiles[vehicle] = [0]*(72*60)
    smartProfiles2[vehicle] = [0]*(72*60)
    for day in range(0,2):
        energyReq = energy[vehicle][day]
        
        start = chargeStarts[vehicle][day]+day*24*60

        end = tripStarts[vehicle][day+1]
        if end < 540:
            end += (day+1)*24*60
        else:
            end = 540+(day+1)*24*60
        
        if energyReq == 0:
            continue

        X = smart_charge(start,end,energyReq)
        for j in range(0,len(X)):
                smartProfiles[vehicle][start+j] += X[j]
                
        X = smart_charge(start,end,energyReq,perturb=True)
        for j in range(0,len(X)):
                smartProfiles2[vehicle][start+j] += X[j]

t = np.linspace(9,33,24*60)
xaxis = np.linspace(9,33,num=5)
my_xticks = ['09:00','15:00','21:00','03:00','09:00']
plt.figure(1)
for i in range(1,17):
    vehicle = chosenVehicles[i]
    plt.subplot(4,4,i)
    plt.plot(t,smartProfiles[vehicle][33*60:57*60])
    plt.plot(t,profiles[vehicle][33*60:57*60])
    plt.plot(t,smartProfiles2[vehicle][33*60:57*60])
    plt.xticks(xaxis, my_xticks)
    #plt.plot(t,baseLoad[24*60:48*60])
    plt.xlim(9,33)
    plt.ylim(0,4)
    plt.title(vehicle,y=0.8)

summedSmart = [0.0]*24*60
summedDumb = [0.0]*24*60
summedSmart2 = [0.0]*(24*60)

for i in range(0,55):
    vehicle = chosenVehicles[i]
    for j in range(0,24*60):
        summedSmart[j] += smartProfiles[vehicle][33*60+j]
        summedDumb[j] += profiles[vehicle][33*60+j]
        summedSmart2[j] += smartProfiles2[vehicle][33*60+j]

xaxis2 = np.linspace(9,33,num=9)
my_xticks2 = ['09:00','12:00','15:00','18:00','21:00','00:00','03:00','06:00','09:00']
plt.figure(2)
plt.xticks(xaxis2, my_xticks2)
plt.plot(t,summedSmart,label='Valley filling')
plt.plot(t,summedDumb,label='Observed charging')
plt.plot(t,summedSmart2,label='slow charging')
plt.xlim(9,33)
plt.legend()
plt.xlabel('time')
plt.ylabel('total power (kW)')


for i in range(0,55):
    with open(profileStem+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = profiles[chosenVehicles[i]][33*60:57*60]
        profile = profile[15*60:] + profile[:15*60]
        for cell in profile:
            writer.writerow([cell])


for i in range(0,55):
    with open(profileStem2+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = smartProfiles[chosenVehicles[i]][33*60:57*60]
        profile = profile[15*60:] + profile[:15*60]
        for cell in profile:
            writer.writerow([cell])

for i in range(0,55):
    with open(profileStem3+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = smartProfiles2[chosenVehicles[i]][33*60:57*60]
        profile = profile[15*60:] + profile[:15*60]
        for cell in profile:
            writer.writerow([cell])

plt.show()
   
