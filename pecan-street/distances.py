import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import copy
import scipy.optimize
import random

stem = '../../Documents/pecan-street/mueller-solar/'

day0 = datetime.datetime(2018,1,1)

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
        wind[day] = [int(row[1]),row[2]]

maxD = 0
distances = {}
for dayNo in range(50):  
    day = day0+datetime.timedelta(dayNo)

    # getting the time-shits
    with open('shifts/'+str(day)[:10]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        users = []
        corr = []
        for row in reader:
            users.append(row[0])
            corr.append(row[1:])

    for i in range(len(users)):
        if users[i] not in distances:
            distances[users[i]] = {}
        for j in range(i):
            if users[j] not in distances[users[i]]:
                distances[users[i]][users[j]] = []
            if float(corr[i][j]) > 50:
                continue
            if float(corr[i][j]) == 0:
                continue
            d = float(corr[i][j])*wind[day][0]
            if d > maxD:
                maxD = d
            distances[users[i]][users[j]].append([d,wind[day][1]])
    '''
    with open('distances/'+str(day)[:10]+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['']+users)
        for i in range(len(users)):
            writer.writerow([users[i]]+distances[i])
    '''

alpha = {'N':0.0,'NNE':22.5,'NE':45.0,'ENE':67.5,'E':90.0,'ESE':112.5,
         'SE':135.0,'SSE':157.5,'S':180.0,'SSW':202.5,'SW':225.0,'WSW':247.5,
         'W':270.0,'WNW':292.5,'NW':315.0,'NNW':337.5}

mse = {} 
users = []
for a in distances:
    users.append(a)
    mse[a] = {}
    for b in distances[a]:
        m = distances[a][b]
        def f(x):
            l = x[0]
            theta = x[1]
            obj = 0.0
            for r in m:
                obj += np.power(r[0]-l*np.cos(np.deg2rad(theta-alpha[r[1]])),2)
            return obj
        '''
        def g(x):
            l = x[0]
            theta = x[1]
            grad = [0.0]*2
            for r in m:
                grad[0] -= 2*(r[0]-l*np.cos(theta-alpha[r[1]]))*\
                        np.cos(theta-alpha[r[1]])
                grad[1] -= 2*(r[0]-l*np.cos(theta-alpha[r[1]]))*r[0]*\
                        np.sin(theta-alpha[r[1]])
            return grad
        '''
        lowest = 10000000000
        best = None

        for x1 in np.arange(0,2*maxD,10):
            for x2 in np.arange(0,360,5):
                f1 = f([x1,x2])
                if f1 < lowest:
                    lowest = f1
                    best = [x1,x2]triangu

        mse[a][b] = best


with open('distances.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['']+users)
    for i in range(len(users)):
        row = [users[i]]
        for j in range(i):
            try:
                row.append(mse[users[i]][users[j]][0])
            except:
                row.append('')
        writer.writerow(row)

with open('angles.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['']+users)
    for i in range(len(users)):
        row = [users[i]]
        for j in range(i):
            try:
                row.append(mse[users[i]][users[j]][1])
            except:
                row.append('')
        writer.writerow(row)
            
    
        
