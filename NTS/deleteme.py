# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, BaseLoad

day = '3'
month = '7'

run = EnergyPrediction(day,month,region='7')

runBase = BaseLoad(day,month,36,unit='k')
base = runBase.getLoad(population=0.1*run.nPeople)

profiles = run.getOptimalChargingProfiles(4,base,chargeAtWork=True)

profiles2 = run.getOptimalChargingProfiles(4,base,chargeAtWork=False)

summed = [0.0]*36
summed2 = [0.0]*36

for vehicle in profiles:
    for i in range(0,36):
        summed[i] += profiles[vehicle][i]
for vehicle in profiles2:
    for i in range(0,36):
        summed2[i] += profiles2[vehicle][i]

t = np.linspace(0,36,num=36*60)

plt.figure(1)
plt.plot(summed)
plt.plot(summed2)
plt.plot(t,base)
plt.show()
