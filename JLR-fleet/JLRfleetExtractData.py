import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

startDates = {}

newData = []

with open('../../Documents/JLRCompanyCars/JLRdata.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[14]

        #distance = row[2] # km
        startDate = datetime.datetime(int('20'+row[4][6:8]),int(row[4][3:5]),
                                      int(row[4][:2]))
        #startHour = int(row[4][9:11])
        #startMin = int(row[4][12:14])
        #endDate = row[6][:9]
        #endHour = int(row[6][9:11])
        #endMin = int(row[6][12:14])

        #avSpeed = int(float(row[7]))
        #duration = float(row[12])

        if userID not in startDates:
            startDates[userID] = datetime.datetime(2017,01,01)

        if startDate <= startDates[userID]:
            startDates[userID] = startDate



with open('../../Documents/JLRCompanyCars/JLRdata.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[14]

        distance = int(float(row[2])*1000) # km -> m
        date = datetime.datetime(int('20'+row[4][6:8]),int(row[4][3:5]),
                                 int(row[4][:2]))
        dayNo = (date-startDates[userID]).days
        month = int(row[4][3:5])
        
        start = int(row[4][12:14])+60*int(row[4][9:11]) # mins past 00:00
        end = int(row[6][12:14])+60*int(row[6][9:11])

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

        newData.append([userID,dayNo,month,start,end,distance,startWork,
                        endWork,startHome,endHome])

        #avSpeed = int(float(row[7]))
        #duration = float(row[12])

with open('../../Documents/JLRCompanyCars/trips_useful.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','day #','month','start','end','distance (m)',
                     'from work?','to work?','from home?','to home?'])
    for row in newData:
        writer.writerow(row)

    
