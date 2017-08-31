import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

startDates = {}

newData = []

with open('../../Documents/JLRCompanyCars/JLRdata.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)
    for row in reader:
        print(row)

        userID = row[14]

        if userID not in startDates:
            startDates[userID] = datetime.datetime(2018,1,1)

        date = datetime.datetime(int('20'+row[4][6:8]),int(row[4][3:5]),
                                 int(row[4][:2]))

        if date <= startDates[userID]:
            startDates[userID] = date


with open('../../Documents/JLRCompanyCars/JLRdata.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        userID = row[14]

        date = datetime.datetime(int('20'+row[4][6:8]),int(row[4][3:5]),
                                 int(row[4][:2]))

        start = int(int(row[4][9:11])*60+int(row[4][12:14]))
        end = int(int(row[6][9:11])*60+int(row[6][12:14]))

        distance = int(float(row[2])*1000) # km -> m

        weekday = date.isoweekday()
        
        dayNo = (date-startDates[userID]).days
        month = int(row[4][3:5])
        

        if row[20] == 'TRUE':
            startWork = 1
        else:
            startWork = 0
            
        if row[21] == 'TRUE':
            endWork = 1
        else:
            endWork = 0
            
        if row[22] == 'TRUE':
            startHome = 1
        else:
            startHome = 0
            
        if row[23] == 'TRUE':
            endHome = 1
        else:
            endHome = 0

        newData.append([userID,dayNo,weekday,month,start,end,distance,startWork,
                        endWork,startHome,endHome])


with open('../../Documents/JLRCompanyCars/trips_useful.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','day #','weekday','month','start','end',
                     'distance (m)','from work?','to work?','from home?',
                     'to home?'])
    for row in newData:
        writer.writerow(row)

    
