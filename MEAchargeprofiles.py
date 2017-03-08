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

charge = [0]*(24*60)

with open('../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]
        startHour = int(row[1][11:13])
        startMin = int(row[1][14:16])

        endHour = int(row[2][11:13])
        endMin = int(row[2][14:16])

        for i in range(startHour*60+startMin, endHour*60+endMin):
            charge[i] += 1

total = sum(charge)
for i in range(0,24*60):
    charge[i] = float(charge[i])/total

t = np.linspace(0,24,num=24*60)
plt.figure(1)
plt.plot(t,charge)
xaxis = np.linspace(2,22,num=6)
my_xticks = ['02:00','06:00','10:00','16:00','18:00','22:00']
plt.xticks(xaxis, my_xticks)
plt.ylabel('Probability')
plt.xlabel('time')
plt.title('Probability a vehicle is on charge (ish)')


plt.show()
    
