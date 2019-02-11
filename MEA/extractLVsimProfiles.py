import csv
import matplotlib.pyplot as plt
import datetime

charges = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'

tripss = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'

outStem = '../../Documents/My_Electric_avenue_Technical_Data/constance/ST1charges/'
# okay let's keep things simpler and just get a time series for both charging
# and velocity for each vehicle.

dayS = datetime.datetime(2014,10,23)
dayE = datetime.datetime(2015,7,3)

print(dayS-dayE)

trips = {}         
with open(tripss,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0][:3] != 'ST1':
            continue
        vehicle = row[0][3:]

        if vehicle in ['015','017','051','095']:
            continue
        
        if vehicle not in trips:
            trips[vehicle] = {}

        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                int(row[1][8:10]))
        if day < dayS:
            continue
        if day > dayE:
            continue
        dayN = (day-dayS).days

        if dayN not in trips[vehicle]:
            trips[vehicle][dayN] = []
            
        start = 60*int(row[1][11:13])+int(row[1][14:16])

        trips[vehicle][dayN].append(start)
        
charge = {}
          
with open(charges,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0][:3] != 'ST1':
            continue
        vehicle = row[0][3:]

        if vehicle in ['015','017','051','095']:
            continue
        
        if vehicle not in charge:
            charge[vehicle] = []

        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                int(row[1][8:10]))
        wd = day.isoweekday()
        if day < dayS:
            continue
        if day > dayE:
            continue
        dayN = int((day-dayS).days)
            
        start = 60*int(row[1][11:13])+int(row[1][14:16])
        kWh = 2*(float(row[4])-float(row[3]))

        nextUse = 1440
        # first look for journeys after that charge that day
        if dayN in trips[vehicle]:
            for trip in trips[vehicle][dayN]:
                if trip > start and trip < nextUse:
                    nextUse = trip
        # then look for first journey the next day
        if nextUse == 1440 and dayN+1 in trips[vehicle]:
            for trip in trips[vehicle][dayN+1]:
                if trip < start and trip < nextUse:
                    nextUse = trip
        # finally - hack to ensure that there is 1 min constraint
        if nextUse == 1440:
            nextUse = start-60

        charge[vehicle].append([dayN,start,nextUse,kWh,wd])
        

for vehicle in charge:
    with open(outStem+vehicle+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['day','start','needed by','kWh','Weekday'])
        for i in range(len(charge[vehicle])):
            writer.writerow(charge[vehicle][i])


