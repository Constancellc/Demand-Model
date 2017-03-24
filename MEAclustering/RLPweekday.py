import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'

users = []
weekdayRLPs = {}
weekendRLPs = {}
ranges = {}

data = {'charge':chargeData, 'use':tripData}

for key in data:
    with open(data[key]) as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            userID = row[0]

            if userID not in users:
                users.append(userID)
                weekdayRLPs[userID] = {'charge':[0.0]*(24*60),'use':[0.0]*(24*60)}
                weekendRLPs[userID] = {'charge':[0.0]*(24*60),'use':[0.0]*(24*60)}
                ranges[userID] = {'charge':{'earliest':datetime.datetime.now(),
                                            'latest':datetime.datetime(2010,01,01)},
                                  'use':{'earliest':datetime.datetime.now(),
                                         'latest':datetime.datetime(2010,01,01)}}

            stampIn = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                        int(row[1][8:10]),int(row[1][11:13]),
                                        int(row[1][14:16]))
            dayIn = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                      int(row[1][8:10]))
            minsIn = (stampIn-dayIn).seconds/60

            stampOut = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                         int(row[2][8:10]),int(row[2][11:13]),
                                         int(row[2][14:16]))
            dayOut = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                       int(row[2][8:10]))
            minsOut = (stampOut-dayOut).seconds/60

            if stampIn < ranges[userID][key]['earliest']:
                ranges[userID][key]['earliest'] = stampIn
            if stampOut > ranges[userID][key]['latest']:
                ranges[userID][key]['latest'] = stampOut

            if minsOut > minsIn:
                for i in range(minsIn,minsOut):
                    if stampIn.weekday() < 5:
                        weekdayRLPs[userID][key][i] += 1
                    else:
                        weekendRLPs[userID][key][i] += 1
            else:
                for i in range(minsIn,24*60):
                    if stampIn.weekday() < 5:
                        weekdayRLPs[userID][key][i] += 1
                    else:
                        weekendRLPs[userID][key][i] += 1
                for i in range(0,minsOut):
                    if stampOut.weekday() < 5:
                        weekdayRLPs[userID][key][i] += 1
                    else:
                        weekendRLPs[userID][key][i] += 1


    for ID in users:
        days = (ranges[ID][key]['latest']-ranges[ID][key]['earliest']).days
        weekdays = int(days*5/7)
        weekendDays = days - weekdays
        for i in range(0,24*60):
            weekdayRLPs[ID][key][i] = weekdayRLPs[ID][key][i]/weekdays
            weekendRLPs[ID][key][i] = weekendRLPs[ID][key][i]/weekendDays


#with open('weekdayChargeRLPs.csv','w') as csvfile:
#    writer = csv.writer(csvfile)
#    for ID in users:
#        row = [ID] + weekdayRLPs[ID]['charge']
#        writer.writerow(row)

#with open('weekendChargeRLPs.csv','w') as csvfile:
#    writer = csv.writer(csvfile)
#    for ID in users:
#        row = [ID] + weekendRLPs[ID]['charge']
#        writer.writerow(row)

t = np.linspace(0,24,num=24*60)

plt.figure(1)
plt.subplot(211)
for user in ['YH11']:
    plt.plot(t,weekdayRLPs[user]['charge'])
    plt.plot(t,weekdayRLPs[user]['use'])
    plt.ylim(0,1)
    plt.xlim(0,24)
plt.subplot(212)
for user in ['YH11']:
    plt.plot(t,weekendRLPs[user]['charge'])
    plt.plot(t,weekendRLPs[user]['use'])
    plt.ylim(0,1)
    plt.xlim(0,24)
plt.show()
