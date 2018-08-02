import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import copy

stem = '../../Documents/pecan-street/mueller-solar/'

maxs = {}
with open('max.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        maxs[row[0]] = int(float(row[1]))+1
day0 = datetime.datetime(2018,1,1)

sun = {}

with open('austin-sun.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        c = 0
        dy = ''
        mn = ''
        yr = ''
        
        while row[0][c] != '-':
            dy += row[0][c]
            c += 1
        c += 1
        while row[0][c] != '-':
            mn += row[0][c]
            c += 1
        c += 1
        yr = row[0][c:]
        
        day = datetime.datetime(2000+int(yr),int(mn),int(dy))
        dayN = (day-day0).days
        sRise = int(60*float(row[1][:2])+float(row[1][3:5]))
        sSet = int(60*float(row[2][:2])+float(row[2][3:5]))

        sun[dayN] = [sRise,sSet]

profiles = {}
          
with open(stem+'feb18_3.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        dt = datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                               int(row[0][8:10]),int(row[0][11:13]),
                               int(row[0][14:16]))
        day = (dt-day0).days
        time = int((dt-day0).seconds/60)
        user = row[1]

        [sr,ss] = sun[day]

        if time not in range(sr+1,ss):
            continue

        if user not in maxs:
            continue
        
        solar = float(row[2])

        if solar == 0.0:
            continue

        if day not in profiles:
            profiles[day] = {}

        if user not in profiles[day]:
            profiles[day][user] = [0.0]*1440

        profiles[day][user][time] = solar/(maxs[user]*\
                                           np.sin(np.pi*(time-sr)/(ss-sr)))

def dot(x,y):
    res = 0.0
    for i in range(len(x)):
        res += x[i]*y[i]
    return res

def conv(x,y,maxShift=60):
    best = 0
    highest = dot(x,y)
    for s in range(1,maxShift):
        x1 = copy.copy(x)
        x1 = x1[1440-s:]+x1[:1440-s]
        y1 = copy.copy(y)
        new = dot(x1,y1)
        if new > highest:
            highest = new
            best = s

        x1 = copy.copy(x)
        y1 = copy.copy(y)
        y1 = y1[1440-s:]+y1[:1440-s]
        new = dot(x1,y1)
        if new > highest:
            highest = new
            best = -1*s
    return best

# normalize
'''
for day in profiles:
    for user in profiles[day]:
        s = sum(profiles[day][user])
        for t in range(1440):
            profiles[day][user][t] = profiles[day][user][t]/s
'''            
for day in profiles:
    users = []
    for user in profiles[day]:
        users.append(user)
    corr = []
    for i in range(len(users)):
        corr.append([0.0]*len(users))
    for i in range(len(users)):
        for j in range(i):
            d = conv(profiles[day][users[i]],profiles[day][users[j]])
            corr[i][j] = d
            corr[j][i] = d

    with open('shifts/'+str(day0+datetime.timedelta(day))[:10]+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['']+users)
        for i in range(len(users)):
            writer.writerow([users[i]]+corr[i])
