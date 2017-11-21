import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

hh = '30099'

base = '../../Documents/netrev/constance/EVcustomers10minData.csv'
starts = '../../Documents/netrev/constance/EVcustomerStartDates.csv'
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

        if dayNo not in profiles:
            profiles[dayNo] = {}
            
        typ = row[2]


        if dayNo > maxDay:
            maxDay = dayNo

        profile = []
        for i in range(0,144):
            profile.append(float(row[3+i]))

        profiles[dayNo][typ] = profile

heatmap = np.zeros((144,maxDay+1))
heatmap2 = np.zeros((144,maxDay+1))

for dayNo in profiles:
    for j in range(0,144):
        try:
            heatmap[j][dayNo] = profiles[dayNo]['House data'][j]
            heatmap2[j][dayNo] = profiles[dayNo]['Charge point'][j]
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
    i += 91

    x.append(i)
    try:
        x_ticks.append(months[startMonth+3]+'\n'+str(startYear))
    except:
        x_ticks.append(months[startMonth-9]+'\n'+str(startYear))
    i += 91
        
    x.append(i)
    try:
        x_ticks.append(months[startMonth+6]+'\n'+str(startYear))
    except:
        x_ticks.append(months[startMonth-6]+'\n'+str(startYear))
    i += 91

    x.append(i)
    try:
        x_ticks.append(months[startMonth+9]+'\n'+str(startYear))
    except:
        x_ticks.append(months[startMonth-3]+'\n'+str(startYear))
    i += 92
    startYear += 1           
            

y_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
y = range(12,156,24)

plt.figure(1)
plt.subplot(2,1,1)
plt.title('Location ID: '+hh+'\nSmart Meter')
plt.imshow(heatmap,aspect=0.5,vmin=0,vmax=3.5)
plt.colorbar()
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.xlim(0,maxDay)
plt.subplot(2,1,2)
plt.title('Charge Point')
plt.imshow(heatmap2,aspect=0.5,vmin=0,vmax=3.5)
plt.colorbar()
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.xlim(0,maxDay)
plt.show()
        
