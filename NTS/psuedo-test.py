# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction, BaseLoad

day = '3'
month = '6'
'''
run = EnergyPrediction(day,month=month,region='8')

runBase = BaseLoad(day,month,36,unit='k')
base = runBase.getLoad(population=run.nPeople)

psuedo = run.getPsuedoOptimalProfile(4,base,weighted=False)
psuedoW = run.getPsuedoOptimalProfile(4,base)

'''
run = NationalEnergyPrediction(day,month)

psuedo = run.getPsuedoOptimalProfile(4,weighted=False)
psuedoW = run.getPsuedoOptimalProfile(4)

base = run.baseLoad



for i in range(0,len(base)):
    psuedo[i] += base[i]
    psuedo[i] = psuedo[i]/1000000
    psuedoW[i] += base[i]
    psuedoW[i] = psuedoW[i]/1000000
    base[i] = base[i]/1000000

t = np.linspace(0,36,num=36*60)
x = np.arange(10,38,4)
x_ticks = ['10:00','14:00','18:00','22:00','02:00','06:00','10:00']

plt.figure(1)
plt.plot(t,base,label='base')
plt.plot(t,psuedo,label='unweighted')
plt.plot(t,psuedoW,label='weighted')
plt.ylim(0,55)
plt.xlim(8,36)
plt.xticks(x,x_ticks)
plt.legend()
plt.show()
