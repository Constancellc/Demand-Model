# packages
import csv
import random
import copy
import datetime
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/netrev/TC2a/'

day0 = datetime.datetime(2012,10,1)
'''
# this section will extract the whol data
hh = {}
with open(stem+'TrialMonitoringDataPassiv.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1] in ['solar power','whole home power import']:
            if row[0] not in hh:
                hh[row[0]] = {}
            day = datetime.datetime(int(row[3][6:10]),int(row[3][3:5]),
                                    int(row[3][:2]))
            dayNo = (day-day0).days
            if dayNo not in hh[row[0]]:
                hh[row[0]][dayNo] = [0.0]*1440
                
            time = int(row[3][11:13])*60+int(row[3][14:16])

            hh[row[0]][dayNo][time] += float(row[4])
           
with open(stem+'TrialMonitoringDataMicrowatt.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1] == 'Total Property':
            
            if row[0] not in hh:
                hh[row[0]] = {}
            day = datetime.datetime(int(row[3][6:10]),int(row[3][3:5]),
                                    int(row[3][:2]))
            dayNo = (day-day0).days
            if dayNo not in hh[row[0]]:
                hh[row[0]][dayNo] = [0.0]*1440
                
            time = int(row[3][11:13])*60+int(row[3][14:16])

            hh[row[0]][dayNo][time] = float(row[4])*60/1000

with open(stem+'1minProfiles.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Loc','Day','Time (mins)','Power (kW)'])
    for l in hh:
        for d in hh[l]:
            for t in range(1440):
                writer.writerow([l,d,t,hh[l][d][t]])

#'''


smallest = 1000
biggest = 0
hh = {}
with open(stem+'1minProfiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in hh:
            hh[row[0]] = {}
        if row[1] not in hh[row[0]]:
            hh[row[0]][row[1]] = [0]*1440
        hh[row[0]][row[1]][int(row[2])] = float(row[3])
        if int(row[1]) > biggest:
            biggest = int(row[1])
        if int(row[1]) < smallest:
            smallest = int(row[1])

print(day0+datetime.timedelta(smallest))
print(day0+datetime.timedelta(biggest))
def check_for_errors(p):
    nZero = 0
    for t in range(len(p)):
        if p[t] == 0:
            nZero += 1
    if nZero < 20:
        return False
    else:
        return True

days = {}

for hh_ in hh:
    for day in hh[hh_]:
        if day not in days:
            days[day] = []
        err = check_for_errors(hh[hh_][day])
        if err == False:
            days[day].append([hh_])

day_lens = []
for d in days:
    day_lens.append([len(days[d]),d])

day_lens = sorted(day_lens,reverse=True)
print(day_lens[0][0])
with open(stem+'goodDays.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['day','date','weekday'])
    for d in day_lens:
        if d[0] < 50:
            continue
        date = day0 = datetime.datetime(2012,10,1)+datetime.timedelta(int(d[1]))
        row = [d[1],date,date.isoweekday()] + days[d[1]]
        writer.writerow(row)
