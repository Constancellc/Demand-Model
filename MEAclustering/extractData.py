import csv
import matplotlib.pyplot as plt
import datetime

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'

tripsOUT = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'
chargesOUT = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges.csv'
timeRanges = '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'
charges = {}
trips = {}

chargeRanges = {}
tripRanges = {}

# FIRST I AM GOING TO GET THE DATA

with open(chargeData) as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]

        if userID not in charges:
            charges[userID] = []
            trips[userID] = []

            chargeRanges[userID] = {'earliest':datetime.datetime.now(),
                                    'latest':datetime.datetime(2010,01,01)}

            tripRanges[userID] = {'earliest':datetime.datetime.now(),
                                    'latest':datetime.datetime(2010,01,01)}

        stampIn = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                    int(row[1][8:10]),int(row[1][11:13]),
                                    int(row[1][14:16]))

        stampOut = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                     int(row[2][8:10]),int(row[2][11:13]),
                                     int(row[2][14:16]))
                
        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                  int(row[1][8:10]))

        if day >= datetime.datetime(2013,3,31) and day < datetime.datetime(2013,10,27):
            stampIn += datetime.timedelta(hours=1)
            stampOut += datetime.timedelta(hours=1)

        if day >= datetime.datetime(2014,3,30) and day < datetime.datetime(2014,10,26):
            stampIn += datetime.timedelta(hours=1)
            stampOut += datetime.timedelta(hours=1)
            
        if day >= datetime.datetime(2015,3,29) and day < datetime.datetime(2015,10,25):
            stampIn += datetime.timedelta(hours=1)
            stampOut += datetime.timedelta(hours=1)

    

        minsIn = (stampIn-day).seconds/60

        minsOut = (stampOut-day).seconds/60

        if minsOut < minsIn:
            minsOut += 24*60

        if stampIn < chargeRanges[userID]['earliest']:
            chargeRanges[userID]['earliest'] = stampIn
        if stampOut > chargeRanges[userID]['latest']:
            chargeRanges[userID]['latest'] = stampOut

        energy = int(2000*(float(row[4])-float(row[3]))) # Wh

        initialSOC = float(int(100*float(row[3])/12))/100
        finalSOC = float(int(100*float(row[4])/12))/100

        if day.isoweekday() > 5:
            weekend = 1
        else:
            weekend = 0

        charges[userID].append([day,minsIn,minsOut,initialSOC,finalSOC,weekend])

for user in charges:
    # get start date
    start = chargeRanges[user]['earliest']
    for i in range(0,len(charges[user])):
        charges[user][i][0] = (charges[user][i][0]-start).days+1

with open(timeRanges,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User ID','first charge','last charge'])
    for ID in chargeRanges:
        row = [ID]
        row += [chargeRanges[ID]['earliest']]
        row += [chargeRanges[ID]['latest']]
        writer.writerow(row)
    
with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        user = row[0]

        tripStart = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                    int(row[1][8:10]),int(row[1][11:13]),
                                    int(row[1][14:16]))

        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                  int(row[1][8:10]))

        # skip trip if it's outside the charge data collection period
        if day < chargeRanges[user]['earliest']:
            continue
        if day > chargeRanges[user]['latest']:
            continue


        tripEnd = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                     int(row[2][8:10]),int(row[2][11:13]),
                                     int(row[2][14:16]))

        if day >= datetime.datetime(2013,3,31) and day < datetime.datetime(2013,10,27):
            tripStart += datetime.timedelta(hours=1)
            tripEnd += datetime.timedelta(hours=1)

        if day >= datetime.datetime(2014,3,30) and day < datetime.datetime(2014,10,26):
            tripStart += datetime.timedelta(hours=1)
            tripEnd += datetime.timedelta(hours=1)
            
        if day >= datetime.datetime(2015,3,29) and day < datetime.datetime(2015,10,25):
            tripStart += datetime.timedelta(hours=1)
            tripEnd += datetime.timedelta(hours=1)


        minsStart = (tripStart-day).seconds/60        
        minsEnd = (tripEnd-day).seconds/60

        if minsEnd < minsStart:
            minsEnd += 24*60

        tripDist = int(float(row[3])) # m
        tripEnergy = int(float(row[4])) # Wh

        if tripDist == 0:
            continue

        if tripEnergy == 0:
            continue

        if day.isoweekday() > 5:
            weekend = 1
        else:
            weekend = 0

        trips[user].append([day,minsStart,minsEnd,tripDist,tripEnergy,weekend])
        
for user in trips:
    start = chargeRanges[user]['earliest']
    for i in range(0,len(trips[user])):
        trips[user][i][0] = (trips[user][i][0]-start).days+1

# NOW I THINK I WILL DO SOME DATA CLEANING

with open(tripsOUT,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','day No','start time','end time','distance','energy',
                     'weekend?'])
    for user in trips:
        for line in trips[user]:
            row = [user] + line
            writer.writerow(row)

with open(chargesOUT,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','day No','start time','end time','intial SOC','final SOC',
                     'weekend?'])
    for user in trips:
        for line in charges[user]:
            row = [user] + line
            writer.writerow(row)
        
