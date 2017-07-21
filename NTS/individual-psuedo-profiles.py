# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from NTSenergyPrediction import EnergyPrediction, BaseLoad

day = '3'
month = '1'

run = EnergyPrediction(day,month,region='1')

base = BaseLoad(day,month,36,unit='k')
baseload = base.getLoad(population=int(150.0*65/28))

profiles = run.getPsuedoOptimalProfile(4,baseload,weighted=False,
                                       returnIndividual=True,
                                       allowOverCap=False)

vehicles = []

for vehicle in profiles[1]:
    vehicles.append(vehicle)

profiles2 = run.getDumbChargingProfile(3.5,36*60,individuals=vehicles,
                                       highUseHomeCharging=False,
                                       highUseWorkCharging=False,
                                       highUseShopCharging=False)
profiles3 = run.getOptimalChargingProfiles(3.5,baseload,individuals=vehicles,
                                           sampleScale=False,allowOverCap=False)

    
t = np.linspace(0,36,num=36*60)

x = np.arange(10,38,6)
x_ticks = ['10:00\nWed','16:00','22:00','04:00\nThu','10:00']

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
n = 1
for vehicle in vehicles[1:]:
    plt.subplot(3,1,n)
    plt.plot(t,profiles2[1][vehicle],label='Uncontrolled')

    opt = []
    for i in range(0,36):
        for j in range(0,60):
            opt.append(profiles3[vehicle][i])
#    plt.plot(profiles3[vehicle],label='Optimal')
    plt.plot(t,opt,label='Optimal')
    smart = [0.0]*36*60

    chargeStart = int(profiles[1][vehicle][1])

    for i in range(0,len(profiles[1][vehicle][0])):
        try:
            smart[chargeStart+i] += profiles[1][vehicle][0][i]
        except:
            continue
        
    plt.plot(t,smart,label='Approximate')
    plt.xlim(8,36)
    plt.xticks(x,x_ticks)
    plt.ylabel('Power (kW)')
    plt.grid()
    if n == 1:
        plt.legend(loc=[-0.1,1.05],ncol=2)
    n += 1

plt.show()

