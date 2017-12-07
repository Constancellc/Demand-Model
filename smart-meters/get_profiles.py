import matplotlib.pyplot as plt
from SMenergyPrediction import HouseholdElectricityDemand
import csv
import numpy as np

test = HouseholdElectricityDemand()

profiles = test.getProfile(3,12,nProfiles=500)

data = np.zeros((len(profiles),len(profiles[0])))
for i in range(0,len(profiles)):
    for j in range(len(profiles[0])):
        data[i][j] = profiles[i][j]

with open('../../Documents/household_demand_pool_matt.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)
