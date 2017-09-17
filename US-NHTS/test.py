# packages
import matplotlib.pyplot as plt
import csv
import numpy as np
# my code
from NHTSenergyPrediction import NationalEnergyPrediction, EnergyPrediction, BaseLoad

day = '3'

plotN = {'1':1,'4':2,'7':3,'10':4}
plotTitle = {'1':'January','4':'April','7':'July','10':'October'}


x = np.linspace(8,32,num=5)
x_ticks = ['08:00 \n Wed','14:00','20:00','02:00','08:00 \n Thu']
t = np.linspace(0,36,num=36*60)
plt.figure(1)

plt.rcParams["font.family"] = 'serif'
for month in ['1','4','7','10']:
    plt.subplot(2,2,plotN[month])
    plt.title(plotTitle[month],y=0.85)
    base = BaseLoad(day,month,36,unit='k').getLoad()
    test = NationalEnergyPrediction(day,month,vehicle='teslaS60D',smoothTimes=True)

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
    plt.plot(t,dumb,label='Uncontrolled Charging')
    plt.plot(t,base,'g',ls=':',label='Base Load')
    plt.plot(opt,ls='--',label='Controlled Charging')
    plt.xticks(x,x_ticks)
    plt.xlim(7,33)
    plt.ylim(300,900)
    plt.xlabel('Time')
    plt.ylabel('Power (GW)')
    plt.grid()
    
    if month == '1':
        plt.legend(loc=[-0.2,1.1],ncol=3)
plt.show()

