import csv
import datetime
import matplotlib.pyplot as plt
import random
from cvxopt import matrix, spdiag, solvers, sparse

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges.csv'
rangeData =  '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'

profileStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/unchanged/'
profileStem2 = '../../Documents/My_Electric_avenue_Technical_Data/profiles/smart/'

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

while latest.isoweekday() > 5 and latest.isoweekday() < 2: # pick a middle of week day
    latest += datetime.timedelta(1)

profiles = {}

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0][:3] != 'ST1':
            continue

        if row[0] not in profiles:
            profiles[row[0]] = [0]*(48*60)
            chargeStarts[row[0]] = []

        reqDay = (latest-startDates[row[0]]).days # this is actualy the day before

        dayNo = int(row[1]) - reqDay
        
        if dayNo > 1 or dayNo < 0:
            continue


        startTime = int(row[2])+dayNo*24*60
        endTime = int(row[3])+dayNo*24*60

        chargeStarts[row[0]].append([startTime,endTime-startTime])

        weekendFlag = int(row[5])

        if weekendFlag == 1:
            print 'fuck'
            continue

        for i in range(startTime,endTime):
            if i >= 48*60:
                continue
            profiles[row[0]][i] = power

allVehicles = []

for vehicle in profiles:
    allVehicles.append(vehicle)

chosenVehicles = []

tripStarts = {}

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

        tripStart = dayNo*24*60+int(row[2])

        if row[0] not in tripStarts:
            tripStarts[row[0]] = []

        tripStarts[row[0]].append(tripStart)

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



def smart_charge(start,end,energy):
    t = end-start
    q = matrix(baseLoad[start:end])
    
    A = matrix(1.0/(2*t_int),(1,t))

    b = matrix([energy]) # amount of energy needed

    A3 = spdiag([-1]*t)
    A4 = spdiag([1]*t)
    G = sparse([A3,A4])


    h = matrix([0.0]*t + [7.0]*t)
    
    #q = matrix(baseLoad)

    P = spdiag([1]*t)
    sol = solvers.qp(P,q,G,h,A,b)
    X = sol['x']

    return X


# each vehicle is going to solve its own optimization problem
#t = t_int*48
smartProfiles = {}
for vehicle in chosenVehicles:
    smartProfiles[vehicle] = [0]*(72*60)
    nCharges = len(chargeStarts[vehicle])
    for i in range(0,nCharges):
        # first find the start of the next journey
        start = chargeStarts[vehicle][i][0]
        energy = float(chargeStarts[vehicle][i][1])*power/60

        end = 72*60

        for trip in tripStarts[vehicle]:
            if trip > start:
                if trip < end:
                    end = trip

        try:
            X = smart_charge(start,end,energy)
        except:
            print start,
            print end
            print energy
        for j in range(0,len(X)):
            smartProfiles[vehicle][start+j] += X[j]

plt.figure(1)
for i in range(1,17):
    ran = int(random.random()*55)
    vehicle = chosenVehicles[ran]
    plt.subplot(4,4,i)
    plt.plot(smartProfiles[vehicle][24*60:48*60])
    plt.plot(profiles[vehicle][24*60:])
    plt.title(vehicle)

plt.show()


for i in range(0,55):
    with open(profileStem+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = profiles[chosenVehicles[i]][24*60:]
        for cell in profile:
            writer.writerow([cell])


for i in range(0,55):
    with open(profileStem2+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        profile = smartProfiles[chosenVehicles[i]][24*60:48*60]
        for cell in profile:
            writer.writerow([cell])
    
