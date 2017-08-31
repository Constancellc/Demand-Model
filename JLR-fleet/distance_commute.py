import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

commutes = {}

with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        userID = row[0]

        if (row[10] == '1' or row[7] == '1') or (row[8] == '1' and row[9] == '1'):
            
            if userID not in commutes:
                commutes[userID] = [0.0,0]

            commutes[userID][0] += float(row[6])/1000
            commutes[userID][1] += 1

commute_length = [0]*100

for user in commutes:
    commute_length[int(commutes[user][0]/commutes[user][1])] += 1

plt.figure(1)
plt.bar(range(0,100),commute_length)
plt.xlim(0,60)
plt.xlabel('distance (km)')
plt.title('Average Length of Commute',y=0.8)
plt.ylabel('number of vehicles')
plt.show()
