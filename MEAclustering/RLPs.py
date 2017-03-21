import csv
import matplotlib.pyplot as plt
import datetime

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'

users = []
RLPs = {}
chargeRanges = {}

with open(chargeData) as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]

        if userID not in users:
            users.append(userID)
            RLPs[userID] = [0.0]*(24*60)
            chargeRanges[userID] = {'earliest':datetime.datetime.now(),
                                    'latest':datetime.datetime(2010,01,01)}

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

        if stampIn < chargeRanges[userID]['earliest']:
            chargeRanges[userID]['earliest'] = stampIn
        if stampOut > chargeRanges[userID]['latest']:
            chargeRanges[userID]['latest'] = stampOut

        if minsOut > minsIn:
            for i in range(minsIn,minsOut):
                RLPs[userID][i] += 1
        else:
            for i in range(minsIn,24*60):
                RLPs[userID][i] += 1
            for i in range(0,minsOut):
                RLPs[userID][i] += 1


for ID in users:
    days = (chargeRanges[ID]['latest']-chargeRanges[ID]['earliest']).days
    for i in range(0,24*60):
        RLPs[ID][i] = RLPs[ID][i]/days

with open('chargeRLPs.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for ID in users:
        row = [ID] + RLPs[ID]
        writer.writerow(row)

plt.figure(1)
for user in users:
    plt.plot(RLPs[user])
plt.show()
