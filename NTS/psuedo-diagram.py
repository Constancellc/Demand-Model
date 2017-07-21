# packages
import csv
import matplotlib.pyplot as plt
import numpy as np
# my code
from NTSenergyPrediction import BaseLoad

baseObj = BaseLoad('3','1',36)
base = baseObj.getLoad()

ibase = [0.0]*len(base)
offset = max(base)*1.01
for i in range(0,len(base)):
    ibase[i] = offset-base[i]

t = np.linspace(0,36,num=36*60)

x_ticks = ['03:00','13:00','23:00','09:00']
x = np.linspace(3,33,num=4)

arrive = 16.5 # hours past 00:00
leave = 30.8
energyReq = 20 #kWh

lim1 = [arrive]*100
lim2 = [leave]*100

y = np.linspace(0,100,num=100)

ibase_fill = ibase[int(arrive*60):int(leave*60)]
x_fill = np.linspace(arrive,leave,num=len(ibase_fill))

tot = sum(ibase_fill)/60
scale = energyReq/tot

power = [0.0]*36*60
for i in range(0,len(x_fill)):
    power[int(60*arrive)+i] = ibase_fill[i]*scale

plt.figure(1)
plt.rcParams["font.family"] = 'serif'

plt.subplot(2,2,1)
plt.plot(t,base)
plt.xticks(x,x_ticks)
plt.title('1',y=0.8)
plt.ylim(20,60)
plt.xlim(0,36)
plt.ylabel('Power (GW)')

plt.subplot(2,2,2)
plt.plot(t,ibase)
plt.xticks(x,x_ticks)
plt.title('2',y=0.8)
plt.ylim(0,40)
plt.xlim(0,36)
plt.ylabel('Power (GW)')

plt.subplot(2,2,3)
plt.plot(t,ibase)
plt.xticks(x,x_ticks)
plt.plot(lim1,y,ls='--',c='r')
plt.plot(lim2,y,ls='--',c='r')
plt.fill_between(x_fill,ibase_fill,alpha=0.5)
plt.title('3',y=0.8)
plt.ylim(0,40)
plt.xlim(0,36)
plt.ylabel('Power (GW)')


plt.subplot(2,2,4)
plt.plot(t,power)
plt.xticks(x,x_ticks)
plt.title('4',y=0.8)
plt.ylim(0,3)
plt.xlim(0,36)
plt.ylabel('Power (kW)')

plt.show()
