# packages
import matplotlib.pyplot as plt
import csv
import numpy as np
# my code
from NHTSenergyPrediction import NationalEnergyPrediction, EnergyPrediction, BaseLoad

'''
test = EnergyPrediction('3','4',car='tesla')
base = BaseLoad('3','3',36)
profiles = test.getOptimalChargingProfiles(22,base.baseLoad)
plt.figure(1)
summed = [0]*36
n = 0
for v in profiles:
    n += 1
    for i in range(0,36):
        summed[i] += profiles[v][i]
plt.plot(summed)
plt.plot(np.linspace(0,36,num=36*60), base.baseLoad)
print(n)
plt.show()
'''
plotN = {'1':1,'4':2,'7':3,'10':4}
plotTitle = {'1':'Jan','4':'Apr','7':'Jul','10':'Oct'}

x_ticks = ['08:00','12:00','16:00','20:00','00:00','04:00','08:00']
x = np.arange(8,36,4)
t = np.linspace(0,36,num=36*60)
plt.figure(1)
for month in ['1','4','7','10']:
    plt.subplot(2,2,plotN[month])
    plt.title(plotTitle[month],y=0.85)
    base = BaseLoad('3',month,36,unit='k').getLoad()
    test = NationalEnergyPrediction('3',month,vehicle='teslaS60D',smoothTimes=True)
    print(test.getNumberOfVehicles(),end=' ')
    print('vehicles')
    dumb = test.getDumbChargingProfile(3.5,36,extraCharge=False)
    totalEn = 0
    for i in range(0,36*60):
        totalEn += dumb[i]/60
    print('total energy used: ',end='')
    print(totalEn,end=' ')
    print('kWh')
    opt =  test.getOptimalChargingProfiles(22,36)

    for i in range(0,len(base)):
        dumb[i] += base[i]
        dumb[i] = dumb[i]/1000000
        if i%60 == 0:
            opt[int(i/60)] += base[i]
            opt[int(i/60)] = opt[int(i/60)]/1000000
        base[i] = base[i]/1000000
    plt.plot(t,dumb)
    plt.plot(t,base,'g',ls=':')
    plt.plot(opt)
    plt.xticks(x,x_ticks)
    plt.xlim(7,33)
    plt.ylim(300,900)
    plt.xlabel('Time')
    plt.ylabel('Power (GW)')
    plt.grid()
plt.show()

