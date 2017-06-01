import csv
import matplotlib.pyplot as plt
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

run1 = EnergyPrediction('1')
mon = run1.energy
print 'i have finished with monday'

run2 = EnergyPrediction('2')
tue = run2.energy
print 'i have finished with tuesday'

run3 = EnergyPrediction('3')
wed = run3.energy
print 'i have finished with wednesday'

run4 = EnergyPrediction('4')
thu = run4.energy
print 'i have finished with thursday'

run5 = EnergyPrediction('5')
fri = run5.energy
print 'i have finished with friday'

run6 = EnergyPrediction('6')
sat = run6.energy
print 'i have finished with saturday'

run7 = EnergyPrediction('7')
sun = run7.energy
print 'i have finished with sunday'

maxEnergy = {}

for day in [mon,tue,wed,thu,fri,sat,sun]:
    for vehicle in day:
        if vehicle not in maxEnergy:
            maxEnergy[vehicle] = 0

        if day[vehicle] > maxEnergy[vehicle]:
            maxEnergy[vehicle] = day[vehicle]

energy = [0]*200

for vehicle in maxEnergy:
    try:
        energy[int(maxEnergy[vehicle])] += 1
    except:
        print maxEnergy[vehicle]


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

print float(sum(energy[101:]))/s,
print '% need more than 100 kWh'

print '....'

print float(sum(energy[:25]))/s,
print '% less than nissan Leaf'
        
plt.show()

