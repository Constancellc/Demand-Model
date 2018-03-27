import numpy as np
import matplotlib.pyplot as plt
import csv
from NTSenergyPrediction2 import NationalEnergyPrediction
from fitDistributions import Inference
import copy


resultsStem = '../../Documents/simulation_results/NTS/national_stochastic/'
deadline = 16

for month in ['1','4','7','10']:
    run = NationalEnergyPrediction('2',month)
    o,a,b = run.getStochasticOptimalLoadFlatteningProfile(pDist=[0.05,0.11,0.68,0.11,0.05])

    with open(resultsStem+month+'_planned.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base',0.05,0.2,0.5,0.2,0.05])
        for t in range(len(o[0])):
            writer.writerow([10*t,b[t]/1000000,o[0][t]/1000000,o[1][t]/1000000,
                             o[2][t]/1000000,o[3][t]/1000000,o[4][t]/1000000])

    with open(resultsStem+month+'_experienced.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base',0.05,0.2,0.5,0.2,0.05])
        for t in range(len(o[0])):
            writer.writerow([10*t,b[t]/1000000,a[0][t]/1000000,a[1][t]/1000000,
                             a[2][t]/1000000,a[3][t]/1000000,a[4][t]/1000000])

'''
plt.figure(1)
for i in range(len(o)):
    plt.plot(o[i],label=str(i))
    plt.plot(a[i])
plt.legend()
plt.show()
'''

'''
run = NationalEnergyPrediction('2','1')
[a,t] = run.testDemandTurnUp(3.5,run.baseLoad,12*60)
[a1,t1] = run.testDemandTurnUp(3.5,run.baseLoad,16*60)
[a2,t2] = run.testDemandTurnUp(3.5,run.baseLoad,20*60)

x_ticks = ['02:00','08:00','14:00','20:00','02:00','08:00']
x = [1440+2*60,1440+8*60,1440+14*60,1440+20*60,1440+26*60,1440+32*60]
y_ticks = [20,40,60]
y = [2e7,4e7,6e7]

plt.figure(1)
plt.subplot(3,1,1)
plt.plot(a,label='Original')
plt.plot(t,label='After DTU')
plt.xlim(1440,3600)
plt.legend()
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.ylabel('Power (GW)')
plt.grid()
plt.title('12PM',y=0.8)
plt.subplot(3,1,2)
plt.plot(a1)
plt.plot(t1)
plt.xlim(1440,3600)
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.ylabel('Power (GW)')
plt.grid()
plt.title('4PM',y=0.8)
plt.subplot(3,1,3)
plt.plot(a2)
plt.plot(t2)
plt.xlim(1440,3600)
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.ylabel('Power (GW)')
plt.grid()
plt.title('8PM',y=0.8)
plt.show()
#d = run.getDumbCharging(3.5)

p = run.getApproximateLoadFlattening(16)
o = run.getOptimalLoadFlattening(3)

for i in range(len(p)):
    p[i] += run.baseLoad[i]
for i in range(len(o)):
    o[i] += run.baseLoad[i*10]

plt.figure(1)
plt.plot(p)
plt.plot(np.linspace(0,len(p)-1,num=len(o)),o)
plt.plot(run.baseLoad)
plt.show()

'''
