import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

base = '../../Documents/netrev/TC1a/TrialMonitoringDataHH.csv'
out = '../../Documents/netrev/constance/'

startDay = datetime.datetime(2005,1,1)

smallestNo = {}
biggestNo = {}
profiles = {}

with open(base,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locID = row[0]
        if locID not in profiles:
            profiles[locID] = {}
            smallestNo[locID] = 100000
            biggestNo[locID] = 0

        day = datetime.datetime(int(row[3][6:10]),int(row[3][3:5]),int(row[3][:2]))
        dayNo = (day-startDay).days

        if dayNo < smallestNo[locID]:
            smallestNo[locID] = dayNo
        if dayNo > biggestNo[locID]:
            biggestNo[locID] = dayNo

        if dayNo not in profiles[locID]:
            profiles[locID][dayNo] = [0.0]*48

        time = int(row[3][11:13])*2+int(int(row[3][14:16])/30)
        power = float(row[4])*2 # kWh pver half hour -> kWh

        profiles[locID][dayNo][time] = power

times = []
for i in range(0,48):
    times.append(str(int(i/2))+':'+str(int(30*i%2)))
# first save profiles
with open(out+'halfHourlySmartMeter.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LocID','Day No.']+times)
    for locID in profiles:
        for dayNo in profiles[locID]:
            day = dayNo-smallestNo[locID]
            writer.writerow([locID,day]+profiles[locID][dayNo])


with open(out+'startDates.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LocID','Start Date','Day Range'])
    for locID in smallestNo:
        startDate = datetime.datetime(2005,1,1) + datetime.timedelta(smallestNo[locID])
        dayRange = biggestNo[locID]-smallestNo[locID]
        writer.writerow([locID,startDate,dayRange])
