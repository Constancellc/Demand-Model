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


wind = {}
with open('austin-wind.csv','rU') as csvfile:
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
        wind[dayN] = [int(row[1]),row[2]]

profiles = {}
          
with open(stem+'jan18_2.csv','rU') as csvfile:
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

def cc(x,y,maxShift=60):
    res = [0.0]*(2*maxShift+1)
    res[maxShift] = dot(x,y)
    for s in range(1,maxShift+1):
        x1 = copy.copy(x)
        x1 = x1[1440-s:]+x1[:1440-s]
        y1 = copy.copy(y)
        res[maxShift+s] = dot(x1,y1)
        
        x1 = copy.copy(x)
        y1 = y1[1440-s:]+y1[:1440-s]
        res[maxShift-s] = dot(x1,y1)

    Sn = sum(res)
    for i in range(len(res)):
        res[i] = res[i]/Sn

    return res

users = []
for user in profiles[11]:
    if len(users) < 2:
        users.append(user)


plt.figure()
n = 1
for day in profiles:
    try:
        x = profiles[day][users[0]]
        y = profiles[day][users[1]]
    except:
        continue
    plt.subplot(3,3,n)
    n += 1

    res = cc(x,y)
    plt.plot(res)
    plt.ylim(min(res),0.011)
    plt.plot([60,60],[0,1],'r',ls='--')
    plt.title(wind[day][1],y=0.8)

plt.show()
