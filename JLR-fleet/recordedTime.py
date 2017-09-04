import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

lengths = {}
with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        userID = row[0]

        if userID not in lengths:
            lengths[userID] = int(row[1])
        

        if int(row[1]) > lengths[userID]:
            lengths[userID] = int(row[1])


nWeeks = [0]*70

for userID in lengths:
    try:
        nWeeks[int(lengths[userID]/7)] += 1
    except:
        print(int(lengths[userID]/7))


plt.figure(1)

plt.rcParams["font.family"] = 'serif'
plt.bar(np.arange(0,70)+0.5,nWeeks,width=0.8)
plt.xlabel('time (weeks)')
plt.ylabel('number of vehicles')
plt.title('Length of time recored',y=0.9)
plt.xlim(0,70)
plt.ylim(0,50)

plt.show()
