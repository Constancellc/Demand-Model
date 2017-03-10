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

j = 1

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

        if month != '01':
            continue
        
        year = row[1][:4]

        if year == '2016':
            print 'I AM NOT EQUIPPED TO DEAL WITH LEAP YEARS!'
            
        date = int(row[1][8:10])

        yearOffset = int(year)-2013
        dateOffset = int(date)-1            

        daysOffset = yearOffset*365+monthOffset[month]+dateOffset

        day = remainder[daysOffset%7]

        if day != 'Monday':
            continue

        endHour = int(row[2][11:13])
        if endHour < startHour:
            endHour += 24
        elif endHour == startHour:
            if endMin < startMin:
                endMin += 60
                
        endMin = int(row[2][14:16])

        profile = [0.0]*24*60

        for i in range(startHour*60+startMin, endHour*60+endMin):
            if i == 24*60:
                i -= 24*60
                day = nextDay[day]
            elif i > 24*60:
                i -= 24*60
            profile[i] = 3.5

        with open('MEAprofiles/'+str(j)+'.csv','w') as csvfile:
            writer = csv.writer(csvfile)
            for k in range(0,24*60):
                writer.writerow([profile[k]])
            j += 1