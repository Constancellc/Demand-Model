import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from cvxopt import matrix, spdiag, solvers, sparse

results = []
#distances = []
#energies = []

distanceVsEnergy = {}

cars = []

# 1st January 2013 was a Tuesday, how many days has it been since then?
monthOffset = {'01':0, '02':31, '03':59, '04':90, '05':120, '06':151, '07':181,
               '08':212,'09':243, '10':273, '11':304, '12':334}

remainder = {0:'Tuesday', 1:'Wednesday', 2:'Thursday', 3:'Friday', 4:'Saturday',
             5:'Sunday', 6:'Monday'}

months = ['01','02','03','04','05','06','07','08','09','10','11','12']
monthTitles = ['January','February','March','April','May','June','July',
               'August','September','October','November','December']
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
nextDay = {'Monday':'Tuesday','Tuesday':'Wednesday','Wednesday':'Thursday',
           'Thursday':'Friday','Friday':'Saturday','Saturday':'Sunday',
           'Sunday':'Monday'}

data = {'01':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '02':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '03':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '04':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '05':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '06':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '07':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '08':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '09':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '10':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '11':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)},
        '12':{'Monday':[0.0]*(24*60),'Tuesday':[0.0]*(24*60),
              'Wednesday':[0.0]*(24*60),'Thursday':[0.0]*(24*60),
              'Friday':[0.0]*(24*60),'Saturday':[0.0]*(24*60),
              'Sunday':[0.0]*(24*60)}}

users = {}

with open('../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]
        try:
            users[userID]
        except:
            users[userID] = [row[1],row[1]]

        startHour = int(row[1][11:13])
        startMin = int(row[1][14:16])

        if row[1] > users[userID][1]:
            users[userID][1] = row[1]
        elif row[1] < users[userID][0]:
            users[userID][0] = row[1]

        month = row[1][5:7]
        year = row[1][:4]

        if year == '2016':
            print 'I AM NOT EQUIPPED TO DEAL WITH LEAP YEARS!'
            
        date = int(row[1][8:10])

        yearOffset = int(year)-2013
        dateOffset = int(date)-1            

        daysOffset = yearOffset*365+monthOffset[month]+dateOffset

        day = remainder[daysOffset%7]

        endHour = int(row[2][11:13])
        if endHour < startHour:
            endHour += 24
        elif endHour == startHour:
            if endMin < startMin:
                endMin += 60
                
        endMin = int(row[2][14:16])

        for i in range(startHour*60+startMin, endHour*60+endMin):
            if i == 24*60:
                i -= 24*60
                day = nextDay[day]
            elif i > 24*60:
                i -= 24*60
            data[month][day][i] += 3.5



carMonths = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}

for key in users:

    if users[key][0][:4] != users[key][1][:4]: # not within one calender year
        for i in range(1,13):
            carMonths[i] += 1


    startMonth = int(users[key][0][5:7])
    endMonth = int(users[key][1][5:7])
    for i in range(startMonth, endMonth+1):
        carMonths[i] += 1


t = np.linspace(0,24,num=24*60)
plt.figure(1)

for i in range(0,12):
    plt.subplot(4,3,i+1)
    for j in range(0,7):
        for k in range(0,24*60):
            data[months[i]][days[j]][k] = data[months[i]][days[j]][k]/(4*carMonths[i+1])
        plt.plot(t,data[months[i]][days[j]],label=days[j])
    plt.xlim(0,24)
    plt.ylim(0,1)
    plt.title(monthTitles[i],y=0.8)
    xaxis = np.linspace(2,22,num=6)
    my_xticks = ['02:00','06:00','10:00','16:00','18:00','22:00']
    plt.xticks(xaxis, my_xticks)
    if i == 0:
        plt.legend(loc=[0,-4.1],ncol=7)
plt.show()
    
