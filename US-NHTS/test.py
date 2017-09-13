# packages
import matplotlib.pyplot as plt
import csv
import numpy as np
# my code
from NHTSenergyPrediction import NationalEnergyPrediction, BaseLoad


plotN = {'1':1,'4':2,'7':3,'10':4}
plotTitle = {'1':'Jan','4':'Apr','7':'Jul','10':'Oct'}

x_ticks = ['08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00',
           '00:00','02:00','04:00','06:00','08:00']
x = np.arange(8,34,2)
t = np.linspace(0,36,num=36*60)
plt.figure(1)
for month in ['8']:#,'4','7','10']:
    #plt.subplot(2,2,plotN[month])
    plt.title('Wednesday in August')#plotTitle[month],y=0.9)
    base = BaseLoad('3',month,36)
    test = NationalEnergyPrediction('3',month)
    dumb = test.getDumbChargingProfile(3.5,36)

    for i in range(0,len(base.baseLoad)):
        dumb[i] = dumb[i]/1000000
        dumb[i] += base.baseLoad[i]
    plt.plot(t,dumb)
    plt.plot(t,base.baseLoad)
    plt.xticks(x,x_ticks)
    plt.xlim(7,33)
    plt.xlabel('Time')
    plt.ylabel('Power (GW)')
    plt.ylim(0,1200)
plt.show()

