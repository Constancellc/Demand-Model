# packages
import csv
import matplotlib.pyplot as plt
import numpy as np
import copy

arrive = 16.5 # hours past 00:00
leave = 30.8
energyReq = 24 #kWh

cPower = 3.5

cccv = [0]*36*60
tshift = [0]*36*60
pscale = [0]*36*60

for i in range(0,6*60):
    pscale[int(arrive*60)+i] = 0.5
for i in range(6*60,11*60):
    pscale[int(arrive*60)+i] = 4.0
for i in range(11*60,12*60):
    pscale[int(arrive*60)+i] = 1.0
    

cccvreq = copy.copy(energyReq)
ind = int(arrive*60)
while cccvreq > 0.2*energyReq:
    cccv[ind] = cPower
    ind += 1
    cccvreq -= cPower/60

a = 0.99
p = cPower*a

while cccvreq > 0:
    cccv[ind] = p
    cccvreq -= p/60
    ind += 1
    p = a*p

for i in range(960,1560):
    tshift[i+120] = cccv[i]


t = np.linspace(0,36,num=36*60)

x_ticks = ['12:00','16:00','20:00','00:00','04:00','08:00','12:00']
x = np.linspace(12,36,num=7)


lim1 = [arrive]*100
lim2 = [leave]*100

y = np.linspace(0,100,num=100)
plt.figure(1)
plt.rcParams["font.family"] = 'serif'


plt.plot(t,cccv,label='CC-CV')
plt.plot(t,tshift,label='Time shifted')
plt.plot(t,pscale,label='Power scaled')
plt.xlim(12,36)
plt.xticks(x,x_ticks)
plt.grid()
plt.legend()
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.ylim(0,5)

plt.plot(lim1,y,ls='--',c='r')
plt.plot(lim2,y,ls='--',c='r')

'''
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
'''
plt.show()
