# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

# my code
from NHTSenergyPrediction import CaliforniaEnergyPrediction

day = 'weekday'

t = np.linspace(0,36,num=36*60)
x = np.linspace(8,32,num=5)
x_ticks = ['08:00 \n Wed','14:00','20:00','02:00','08:00 \n Thu']

plt.figure(1)
plt.rcParams["font.family"] = 'serif'

months = ['1','4','7','10']
plotTitle = {'1':'January','4':'April','7':'July','10':'October'}

for mo in range(0,4):
    month = months[mo]

    cali = CaliforniaEnergyPrediction(day,month,smoothTimes=True)
    dumb = cali.getDumbChargingProfile(3.5,36,extraCharge=False)
    base = cali.areaBase.getLoad()
    opt = cali.getOptimalChargingProfiles(7,deadline=9)

    '''
    current problems: really not sure i've got the base load time difference right

    i'm also not sure about the size of the cali base load

    I also need to change the get load thing to take a percentage of population as
    input, not an absolute number
    '''

    for i in range(0,len(base)):
        dumb[i] += base[i]
        dumb[i] = dumb[i]/1000000
        if i%60 == 0:
            opt[int(i/60)] += base[i]
            opt[int(i/60)] = opt[int(i/60)]/1000000
        base[i] = base[i]/1000000

    # artificially smooth dumb charging
    newDumb = [0.0]*36*2

    for i in range(0,len(newDumb)):
        for j in range(0,30):
            newDumb[i] += dumb[30*i+j]
        newDumb[i] = newDumb[i]/30

    dumb = newDumb


    plt.subplot(2,2,mo+1)
    
    plt.title(plotTitle[month],y=0.85)
    plt.plot(np.linspace(0,36,num=36*2),dumb,label='Uncontrolled Charging')
    plt.plot(t,base,'g',ls=':',label='Base Load')
    plt.plot(opt,label='Controlled Charging')
    plt.xlim(7,33)
    plt.ylim(20,80)
    plt.xlabel('Pacific Time')
    plt.ylabel('Power (GW)')
    plt.xticks(x,x_ticks)
    plt.grid()
    
    if month == '1':
        plt.legend(loc=[-0.2,1.1],ncol=3)
plt.show()
