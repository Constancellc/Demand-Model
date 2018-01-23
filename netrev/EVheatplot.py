import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

#hh = '30099'
hh = []
base = '../../Documents/netrev/constance/EVcustomers10minData.csv'
starts = '../../Documents/netrev/constance/EVcustomerStartDates.csv'

figs = '../../Documents/netrev/constance/EVplots/'

with open(starts,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hh.append(row[0])
        
maxDay = 0

profiles = {}
with open(base,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locID = row[0]
        #if locID != hh:
        if locID not in hh:
            continue

        if locID not in profiles:
            profiles[locID] = {}

        dayNo = int(row[1])

        if dayNo not in profiles[locID]:
            profiles[locID][dayNo] = {}
            
        typ = row[2]

        if dayNo > maxDay:
            maxDay = dayNo

        profile = []
        for i in range(0,144):
            profile.append(float(row[3+i]))
            
        profiles[locID][dayNo][typ] = profile


for loc in hh:
    heatmap = np.zeros((144,maxDay+1))
    heatmap2 = np.zeros((144,maxDay+1))

    for dayNo in profiles[loc]:
        for j in range(0,144):
            try:
                heatmap[j][dayNo] = profiles[loc][dayNo]['House data'][j]
            except:
                heatmap[j][dayNo] = 0.0

            try:
                heatmap2[j][dayNo] = profiles[loc][dayNo]['Charge point'][j]
            except:
                heatmap2[j][dayNo] = 0.0

    months = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',
              9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

    x = []
    x_ticks = []

    # get start date
    with open(starts,'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[0] == loc:
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

    plt.figure()
    plt.subplot(2,1,1)
    plt.title('Location ID: '+loc+'\nSmart Meter')
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
    plt.savefig(figs+str(loc)+'.pdf',format='pdf')
    plt.close()
#plt.show()
        
