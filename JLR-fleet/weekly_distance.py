import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

weeks = {}

with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        userID = row[0]
        dayNo = int(row[1])

        if userID not in weeks:
            weeks[userID] = [0.0]*100


        weeks[userID][int(dayNo/7)] += float(row[6])/10000

distances = [0]*100


for user in weeks:
    n = 0
    total = 0.0
    for cell in weeks[user]:
        if cell != 0.0:
            total += cell
            n += 1

    distances[int(total/n)] += 1

plt.figure(1)
plt.bar(range(0,1000,10),distances,6)
plt.xlabel('Average weekly distance (km)')
plt.ylabel('Number of users')
plt.xlim(0,900)
plt.show()

