import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction import NationalEnergyPrediction


run = NationalEnergyPrediction('3','1')

pph = 15
total1 = run.getOptimalChargingProfiles(7,returnTotal=True)
total = run.getClusteredOptimalProfiles(7,4,pointsPerHour=pph)
bl = run.baseLoad

x_ticks = ['10:00','14:00','18:00','22:00','02:00','06:00']
x = np.linspace(10,30,num=6)

plt.figure(1)
plt.rcParams["font.family"] = 'serif'

for i in range(0,len(total)):
    total[i] += bl[int(i*60/pph)]
    total[i] = total[i]/1000000

for i in range(0,len(total1)):
    total1[i] += bl[int(i*60)]
    total1[i] = total1[i]/1000000

for i in range(0,len(bl)):
    bl[i] = bl[i]/1000000

plt.plot(np.linspace(0,36,num=len(total)),total,label='Clustered k=4')
plt.plot(np.linspace(0,36,num=len(total1)),total1,label='Optimal')
plt.plot(np.linspace(0,36,num=len(bl)),bl)

plt.xlim(8,32)
plt.grid()
plt.title('January')
plt.xlabel('time')
plt.ylabel('Power (kW)')
plt.legend()

plt.xticks(x,x_ticks)

plt.show()
