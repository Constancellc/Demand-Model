import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

cap = 8529

day1 = datetime.datetime(2018,1,1)
#data = []
dataN = {}
for i in range(12):
    dataN[i] = {}

for i in range(1,5):
    with open('../../Documents/gen_by_fuel_type'+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) < 3:
                continue
            time = int(row[2])-1
            wind = float(row[7])/cap
            month = int(row[1][4:6])-1
            date = datetime.datetime(int(row[1][:4]),int(row[1][4:6]),
                                     int(row[1][6:8]))
            day = (date-day1).days
            if day not in dataN[month]:
                dataN[month][day] = [0]*48
            try:
                dataN[month][day][time] = wind
            except:
                continue

best = []
worst = []
for m in range(12):
    b = None
    w = None
    h = 0
    l = 10000
    print(len(dataN[m]))
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

with open('best_wind.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['month','t (30 mins)'])
    for m in range(12):
        writer.writerow([str(m+1)]+best[m])

with open('worst_wind.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['month','t (30 mins)'])
    for m in range(12):
        writer.writerow([str(m+1)]+worst[m])
