import csv
import matplotlib.pyplot as plt
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

run = EnergyPrediction('3','5')
energy = run.plotEnergyConsumption(returnResults=True, wait=True)
plt.xlim(0,60)
run2 = EnergyPrediction('3','5',car='bmw')
energy2 = run2.plotEnergyConsumption(returnResults=True, wait=True)

plt.figure(2)
plt.subplot(2,1,1)
plt.bar(range(0,24),energy[:24],color='b')
plt.bar(range(24,len(energy)),energy[24:],color='r')
plt.xlim(-0.5,60)
plt.title('Nissan Leaf')

plt.subplot(2,1,2)
plt.bar(range(0,22),energy2[:22],color='b')
plt.bar(range(22,len(energy2)),energy[22:],color='r')
plt.xlim(-0.5,60)
plt.title('BMW i3')

plt.show()
'''
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

'''
