import matplotlib.pyplot as plt
from SMenergyPrediction import HouseholdElectricityDemand
import csv

test = HouseholdElectricityDemand(regionType='3')

profiles = test.getProfile(3,12,nProfiles=1000)

data = np.zeros((1440,1000))
for i in range(0,1000):
    for j in range(1440):
        data[j][i] = profiles[i][j]

with open('../../Documents/household_demand_pool.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)
