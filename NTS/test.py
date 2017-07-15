import matplotlib.pyplot as plt
import numpy as np

from NTSenergyPrediction import NationalEnergyPrediction, NationalEnergyPrediction2

old = NationalEnergyPrediction('3','1')
oldPro = old.getNationalOptimalChargingProfiles(4)
new = NationalEnergyPrediction2('3','1')
newPro = new.getOptimalChargingProfiles(4)

oldSummed = [0.0]*36
for vehicle in oldPro:
    for i in range(0,36):
        oldSummed[i] += oldPro[vehicle][i]
newSummed = [0.0]*36
for vehicle in newPro['']:
    for i in range(0,36):
        newSummed[i] += newPro[''][vehicle][i]/1000000

plt.figure(1)
plt.plot(oldSummed)
plt.plot(newSummed)
plt.show()
