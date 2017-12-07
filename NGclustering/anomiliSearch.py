import matplotlib.pyplot as plt
import numpy as np
import csv
import sklearn.cluster as clst
import datetime

maxDemand = 0

profile = [0.0]*288
with open('../../Documents/gridwatch.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        '''
        year = row[1][:4]
        month = row[1][5:7]
        day = int(row[1][8:10]
        '''
        date = row[1][:11]
        if date == ' 2015-01-12':
                
            time = int(int(row[1][12:14])*12+int(row[1][15:17])/5)

            demand = int(row[2])

            profile[time] = demand
plt.figure(1)
plt.plot(profile)
plt.show()
