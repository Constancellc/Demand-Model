import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction, CornwallEnergyPrediction
from fitDistributions import Inference
import copy


run = CornwallEnergyPrediction('3','7',solar=True)
d = run.getDumbCharging(3.5,nHours=16+48)

[op,to,ba] = run.getStochasticOptimalLoadFlatteningProfile2()

t = np.linspace(0,len(d),num=len(op[0]))

for i in range(len(d)):
    d[i] += run.baseLoad[i]
    
plt.figure(1)
plt.plot(d)
for p in to:
    plt.plot(t,p)
plt.plot(run.baseLoad)
plt.show()


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
