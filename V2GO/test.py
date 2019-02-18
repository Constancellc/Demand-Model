# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import datetime

from vehicleModel import Vehicle, Drivecycle

# Something is wrong. Either with the data or the model

# Given that we don't have very much data it might be nice to do each hour as
# a seperate drivecycle instead of each day

day0 = datetime.datetime(2016,11,16)
# ok first I think I should sort the data into driving days
profiles = {}

bad = []
with open('../../Documents/V2GO/356449064315004_2016-11-16_to_2016-11-30.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        dt = row[5]
        day = datetime.datetime(int(dt[6:10]),int(dt[3:5]),int(dt[:2]))
        t = int(dt[11:13])*3600+int(dt[14:16])*60+int(dt[17:19])

        h = int(t/3600)
        t2 = t%3600
        d = (day-day0).days
        v = float(row[-1])

        if v > 100:
            bad.append(row[0])
        
        if d not in profiles:
            profiles[d] = {}

        if h not in profiles[d]:
            profiles[d][h] = []

        profiles[d][h].append([t,v])

print(bad)
energy = []
distance = {}
for d in profiles:
    distance[d] = [0]*24
    for h in profiles[d]:
        new = []
        t = 0
        for i in range(len(profiles[d][h])-1):
            t += profiles[d][h][i+1][0]-profiles[d][h][i][0]
            new.append([profiles[d][h][i+1][0]-profiles[d][h][i][0],
                        profiles[d][h][i+1][1]])

        dc = Drivecycle(new)
        leaf = Vehicle(1704.5,26.06,0.3,0.01965,0.859,60)
        #energy.append(leaf.getEnergyExpenditure(dc))
        distance[d][h] = dc.distance/1000

plt.figure()
#plt.plot(energy)
plt.bar(range(24),distance[0])
plt.show()

    


        
    

        

        
