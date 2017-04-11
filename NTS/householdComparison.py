import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime

trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'
households = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv'

vehicles = {}
distances = {}


i = 2 # index of vehicle no
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[i] == '' or row[i] == ' ':
            continue
        if row[i] not in vehicles:
            distances[row[i]] = 0.0
            
        distances[row[i]] += float(row[10])

householdIDs = {}
# finding the income bands of each vehicle
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        vehicle = row[2]
        if row[2] in householdIDs:
            continue
        householdIDs[row[2]] = row[1]

cap = 1000
f = 1
#dist = [0]*(int(cap/f))
zeros = [0]*(int(cap/f))
x3 = np.arange(0,cap,f)
histograms = {}

catergories = {}
# this is the index of the variable in the household file we are comparing
# 3 = income band
index = 4
with open(households,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[0] in catergories:
            continue
        catergories[row[0]] = row[index]
        if row[index] not in histograms:
            histograms[row[index]] = [0]*(int(cap/f))



for vehicle in distances:
    try:
        band = catergories[householdIDs[vehicle]]
    except:
        continue
    n = round(distances[vehicle]/f)
    if n >= cap/f:
        continue
    histograms[band][int(n)] += 1


pdfs = {}
for band in histograms:
    if histograms[band] == [0]*(int(cap/f)):
        print band
        continue
    if band == '4' or band == '7':
        continue
    normalised = []
    for i in range(0,len(histograms[band])):
        normalised.append(float(histograms[band][i])/sum(histograms[band]))
    pdfs[band] = normalised

plt.figure(1)

for band in pdfs:
    plt.plot(x3,pdfs[band],label=band,alpha=0.5)
plt.xlim(-1, 50)
plt.ylim(0,0.175)
plt.title('Distance Driven per Vehicle in 1 Week for each Houeshold Type')
plt.xlabel('miles')
plt.ylabel('probability density')
plt.legend()


plt.show()
