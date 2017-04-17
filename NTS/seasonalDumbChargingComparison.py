# packages
import matplotlib.pyplot as plt
import numpy as np
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction

nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)

days = {'1':'Monday','2':'Tuesday','3':'Wednesday','4':'Thursday','5':'Friday',
        '6':'Saturday','7':'Sunday'}
t = np.linspace(0,48,48*60)

plt.figure(1)
for i in days:
    test = EnergyPrediction(i,'5',nissanLeaf,regionType='2')
    profile = test.getDumbChargingProfile(3.5,48*60,scalePerVehicle=True)
    plt.plot(t,profile,label=days[i])

x = np.linspace(4,36,num=9)
plt.grid()
my_xticks = ['04:00 \n Day 1','08:00','12:00','16:00','20:00','0:00',
             '04:00 \n Day 2','08:00','12:00']
plt.xticks(x, my_xticks)
plt.xlim(0,40)
plt.xlabel('time')
plt.ylabel('power per household (kW)')
plt.title('Dumb Charging in May')
plt.legend()

months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
          '6':'June','7':'July','8':'August','9':'September','10':'October',
          '11':'November','12':'December'}
plt.figure(2)
for i in months:
    test = EnergyPrediction('3',i,nissanLeaf,regionType='2')
    profile = test.getDumbChargingProfile(3.5,48*60,scalePerVehicle=True)
    plt.plot(t,profile,label=months[i])

plt.grid()
my_xticks = ['04:00 \n Wed','08:00','12:00','16:00','20:00','0:00',
             '04:00 \n Thu','08:00','12:00']
plt.xticks(x, my_xticks)
plt.xlabel('time')
plt.ylabel('power per households (kW)')
plt.xlim(0,40)
plt.title('Dumb Charging on Wednesday')
plt.legend()

plt.show()
