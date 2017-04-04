import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
import random

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'

users = []
vehicles = ['GC04']#,'GC06','GC08','GC10']

plugIns = {}
months = {}

data = {'charge':chargeData, 'use':tripData}

overallHistogram = [0]*13

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        initialSOC = int(row[3])
        overallHistogram[initialSOC] += 1

        if row[0] not in users:
            users.append(row[0])
            months[row[0]] = []
            plugIns[row[0]] = {}

        month = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),1)

        if month not in months[row[0]]:
            months[row[0]].append(month)
            plugIns[row[0]][month] = [0]*13

        plugIns[row[0]][month][initialSOC] += 1       

N = sum(overallHistogram)

for i in range(0,13):
    overallHistogram[i] = float(overallHistogram[i])/N



    
plt.figure(1)
plt.bar(range(0,13),overallHistogram)
plt.title('State of Charge (out of 12) on Plug In')

# examining change in plug in habits with time

vehicles = users
#lower = []
plt.figure(2)
for vehicle in vehicles:
    ran = random.random()
    if ran > 0.02:
        continue

    means = []
    maxs = []
    mins = []    

    months[vehicle].sort()

    for i in range(0,len(months[vehicle])): # for each month
        highest = 0
        lowest = 12
        # calculate average
        m = 0
        n = float(sum(plugIns[vehicle][months[vehicle][i]])) # number of plug ins that month
        
        for j in range(0,13): # for each possible SOC
            m += j*float(plugIns[vehicle][months[vehicle][i]][j])
            if plugIns[vehicle][months[vehicle][i]][j] != 0:
                if j > highest:
                    highest = float(j)
                if j < lowest:
                    lowest = float(j)
        m = m/n

        # and variance

        v = 0

        for j in range(0,13):
            d = float(j)-m
            v += d*d*plugIns[vehicle][months[vehicle][i]][j]

        v = v/n

        means.append(m)
        maxs.append(highest-m)
        mins.append(m-lowest)
    plt.errorbar(months[vehicle],means,yerr=[mins, maxs],label=vehicle)
    #plt.plot(months[vehicle],means,label=vehicle)
    #plt.fill_between(months[vehicle],upper,lower,alpha=0.5)
plt.xlabel('time')
plt.ylabel('average SOC on plug in')
plt.title('Variation of plug-in SOC wth time')
plt.legend()


        





plt.show()


    
