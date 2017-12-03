# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
#from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import NationalEnergyPrediction, EnergyPrediction


run = NationalEnergyPrediction('3','3',smoothTimes=True,recordUsage=True)
#run = EnergyPrediction('3','3',smoothTimes=True,recordUsage=True)

rtDemand = run.rtDemand

profile = [0.0]*1440

dumb = run.getDumbChargingProfile(3.5,40) # kW

for i in range(len(dumb)):
    if i < 1440:
        profile[i] += dumb[i]
    else:
        profile[i-1440] += dumb[i]

print(sum(rtDemand))
print(sum(profile))

plt.figure(1)
plt.plot(profile)
plt.plot(rtDemand)
plt.show()
