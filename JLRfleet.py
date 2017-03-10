import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from cvxopt import matrix, spdiag, solvers, sparse

results = []

with open('../Documents/JLRCompanyCars/JLRdata.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[14]
        distance = row[2] # km
        startDate = row[4][:9]
        startHour = int(row[4][9:11])
        startMin = int(row[4][12:14])
        endDate = row[6][:9]
        endHour = int(row[6][9:11])
        endMin = int(row[6][12:14])

        avSpeed = int(float(row[7]))
        duration = float(row[12])

        startWork = row[20]
        endWork = row[21]
        startHome = row[22]
        endHome = row[23]

        


        if row[24][0] == '0':
            parkHours = int(row[24][1])
        else:
            try:
                parkHours = int(row[24][:2])
            except:
                print row[24][:2]

        if row[24][3] == '0':
            parkMins = int(row[24][4])
        else:
            try:
                parkMins = int(row[24][3:5])
            except:
                print row[24][3:5]

        if userID == '1':
            for i in range(0,int(duration)):
                results.append(1)
            if endWork == 'TRUE':
                for i in range(0,60*parkHours+parkMins):
                    results.append(2)
            elif endHome == 'TRUE':
                for i in range(0,60*parkHours+parkMins):
                    results.append(0)
            else:
                for i in range(0,60*parkHours+parkMins):
                    results.append(3)
                
                
plt.figure(1)
plt.plot(results)
plt.show()

    
