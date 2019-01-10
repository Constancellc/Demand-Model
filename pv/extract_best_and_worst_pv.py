import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

day1 = datetime.datetime(2015,1,1)
#data = []
dataN = {}
for i in range(12):
    dataN[i] = {}

with open('GBPV_data.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if int(row[1][:4]) < 2014:
            continue
        month = int(row[1][5:7])-1
        date = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),int(row[1][8:10]))
        day = (date-day1).days
        if day not in dataN[month]:
            dataN[month][day] = [0]*48
            
        time = int(int(row[1][11:13])*2+int(row[1][14:16])/30)
        try:
            generation = float(row[2])
            installed = float(row[10])
        except:
            generation = 0.0
            installed = 1.0
            
        dataN[month][day][time] = generation/installed

best = []
worst = []
for m in range(12):
    b = None
    w = None
    h = 0
    l = 10000
    for d in dataN[m]:
        s = sum(dataN[m][d])
        if s < l:
            l = s
            w = d
        if s > h:
            h = s
            b = d
    best.append(dataN[m][b])
    worst.append(dataN[m][w])

with open('best_solar.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['month','t (30 mins)'])
    for m in range(12):
        writer.writerow([str(m+1)]+best[m])

with open('worst_solar.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['month','t (30 mins)'])
    for m in range(12):
        writer.writerow([str(m+1)]+worst[m])
