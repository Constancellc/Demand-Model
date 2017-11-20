import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

hh = '2773'

base = '../../Documents/netrev/constance/halfHourlySmartMeter.csv'
starts = '../../Documents/netrev/constance/startDates.csv'
maxDay = 0


profiles = {}
with open(base,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locID = row[0]
        if locID != hh:
            continue

        dayNo = int(row[1])

        if dayNo > maxDay:
            maxDay = dayNo

        profile = []
        for i in range(0,48):
            profile.append(float(row[2+i]))

        profiles[dayNo] = profile

heatmap = np.zeros((48,maxDay+1))

for dayNo in profiles:
    for j in range(0,48):
        try:
            heatmap[j][dayNo] = profiles[dayNo][j]
        except:
            print(i)

months = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',
          9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

x = []
x_ticks = []

# get start date
with open(starts,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] == hh:
            startYear = int(row[1][:4])
            startMonth = int(row[1][5:7])
            x_ticks.append(months[startMonth]+'\n'+str(startYear))

i = 0
while i < maxDay:
    x.append(i)
    if i != 0:
        x_ticks.append(months[startMonth]+'\n'+str(startYear))
    i += 182

    x.append(i)
    try:
        x_ticks.append(months[startMonth+6]+'\n'+str(startYear))
    except:
        x_ticks.append(months[startMonth-6]+'\n'+str(startYear))
    i += 183
    startYear += 1           
            

y_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
y = range(4,52,8)

plt.figure(1)
plt.title('Location ID: '+hh)
plt.imshow(heatmap,aspect=6,vmin=0,vmax=2)
plt.colorbar()
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.xlim(0,maxDay)
plt.show()
        
