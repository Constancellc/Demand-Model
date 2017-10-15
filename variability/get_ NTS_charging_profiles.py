# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('../NTS')

# my code
from NTSenergyPrediction import EnergyPrediction

profiles = []

for i in range(0,1000):
    profiles.append([0.0]*1440)

i = 0

run = EnergyPrediction('3','7')

vehicleProfiles = run.returnDumbChargingProfiles(1000,3.5)

print(len(vehicleProfiles[0]))

with open('../../Documents/vehicle_demand_pool.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for profile in vehicleProfiles:
        writer.writerow(profile)
