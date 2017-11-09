import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
import copy

data = '../../Documents/sharonb/7591/csv/profiles.csv'
dates = '../../Documents/sharonb/7591/csv/dates.csv'

hh = '9504'
heatmap = []


with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != hh:
            continue

        profile = row[2:]
        for num in profile:
            num = float(num)
        
        heatmap.append(profile)

with open(dates,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != hh:
            continue

        startdate = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                      int(row[1][8:10]))
        enddate = startdate + datetime.timedelta(int(row[2]))

timeline = [startdate]
for i in range(1,len(heatmap)):
    timeline.append(copy.copy(startdate)+datetime.timedelta(i))

months = {1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',
          9:'SEP',10:'OCT',11:'NOV',12:'DEC'}

y = []
x_ticks = []
for year in [2008,2009,2010]:
    for month in [1,4,7,10]:
        if datetime.datetime(year,month,1) < startdate:
            continue
        
        if datetime.datetime(year,month,1) > enddate:
            continue
        
        y.append(datetime.datetime(year,month,1))
        x_ticks.append(months[month]+'\n'+str(year))

x = []
c = 0
for i in range(0,len(timeline)):
    if y[c] == timeline[i]:
        x.append(i)
        c += 1

A = np.zeros((len(heatmap[0]),len(heatmap)))
for i in range(0,len(heatmap[0])):
    for j in range(0,len(heatmap)):
        A[i,j] = heatmap[j][i]

y_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
y = range(2,50,8)

plt.figure(1)
plt.imshow(A,aspect=8)
plt.colorbar()
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.show()
