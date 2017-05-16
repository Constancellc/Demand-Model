import csv
import matplotlib.pyplot as plt
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

run = EnergyPrediction('3')
energy = run.plotEnergyConsumption(returnResults=True, wait=True)

s = float(sum(energy))/100

print float(energy[0])/s,
print '% need no energy'

breaks = [1,6,11,21,31,51,101]

for i in range(0,len(breaks)-1):
    tot = 0
    for j in range(breaks[i],breaks[i+1]):
        tot += energy[j]
    print float(tot)/s,
    print '% between ' + str(breaks[i]-1) + ' and ' + str(breaks[i+1]-1)

print float(energy[-1])/s,
print '% need more than 100 kWh'

print '....'

print float(sum(energy[:25]))/s,
print '% less than nissan Leaf'
        
plt.show()

