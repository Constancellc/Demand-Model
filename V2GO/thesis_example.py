# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
from vehicleModelV2GO import Drivecycle, Vehicle
import datetime
from matplotlib import cm

stem = '../../Documents/V2GO/EV_data_processed/WithElevation/'
vehicle = '356449064315004'

car = Vehicle(3000,102.5,3.63,0.422,0.85,90)

# okay, what do we want to do with the vehicle model?

start_day = [16,11,21,19]
days_recorded = [15,19,9,12]
# we want to segment the diary into a dictionary of journeys I suspect

for ii in range(1):
    '''
    plt.figure(figsize=(5,3))
    plt.rcParams["font.family"] = 'serif'
    plt.rcParams["font.size"] = '8'
    plt.title(vehicle)
    plt.grid(ls=':')
    plt.ylim(0,100)
    plt.xlim(0,24)
    plt.ylabel('SOC (%)')'''
    
    time0 = datetime.datetime(2016,11,int(start_day[ii]))
    results = []
    v = []
    sl =[]
    x = []
    y = []
    e = []
    with open(stem+vehicle+'_on_2016-11-18_elv.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            h = int(row[0][:2])
            m = int(row[0][3:5])
            s = int(row[0][6:8])
            t = 3600*h+60*m+s
            v.append(float(row[-4]))
            sl.append(float(row[-1]))
            x.append(float(row[4]))
            y.append(float(row[3]))
            e.append(float(row[-2]))
            
        dc = Drivecycle(v,sl)
        energy = car.getEnergyExpenditurePerSecond(dc)

        capacity = 60       

        SOC = [100]
        for t in range(len(energy)):
            SOC.append(SOC[-1]-100*energy[t]/capacity)

e_m = min(e)
e_r = max(e)-min(e)
for t in range(len(e)):
    e[t] = (e[t]-e_m)/e_r


plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '12'
plt.subplot(2,1,1)
plt.plot(np.linspace(0,24,num=len(v)),v)
plt.ylabel('Velocity (kmph)')
plt.xticks([2,6,10,14,18,22],['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.grid()
plt.xlim(0,24)

plt.subplot(2,1,2)
plt.plot(np.linspace(0,24,num=len(SOC)),SOC)
plt.ylabel('SOC (%)')
plt.xlim(0,24)
plt.xticks([2,6,10,14,18,22],['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.tight_layout()
plt.grid()
plt.savefig('../../Dropbox/thesis/chapter3/img/v2go_prof.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.1)
#plt.show()


step = 10
plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '12'
for t in range(int(len(x)/step)):
    if t > 0:
        if x[(t-1)*step] == x[t*step]:
            continue
    plt.scatter(x[t*step],y[t*step],c=cm.viridis(e[t*step]),s=10)

# now do colorbar
top = 51.5
btm = 51.35

for i in range(100):
    y1 = btm+(top-btm)*(i/100)
    y2 = btm+(top-btm)*((i+1)/100)
    plt.plot([0,0],[y1,y2],lw=6,c=cm.viridis(i/100))
tcks = ['0 m','40 m','80 m','120 m']

plt.annotate('Elevation',(-0.005,51.515))
top = 51.488
for i in range(4):
    y_ = btm+(top-btm)*(i/3)-0.004
    plt.annotate('- '+tcks[i],(0.005,y_))
plt.yticks([51.35,51.5],['',''])
plt.xticks([-0.3,0],['',''])
plt.tight_layout()
plt.axis('off')
plt.savefig('../../Dropbox/thesis/chapter3/img/v2go_trace.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.1)
plt.show()
'''        plt.plot(np.linspace(0,24,num=len(SOC)),SOC,
                 label=str(time0+datetime.timedelta(day))[:10])
            

        results.append([time0+datetime.timedelta(days=day,seconds=earliest),
                        time0+datetime.timedelta(days=day,seconds=latest),
                        energy])
    plt.xticks([2,6,10,14,18,22],['02:00','06:00','10:00','14:00','18:00',
                                  '22:00'])
    plt.legend(ncol=3)
    plt.tight_layout()
    plt.savefig(stem+'/predicted/'+str(vehicle)+'.pdf',format='pdf')


log = {}
sts = []
i = 0
while i < len(_log)-2:
    j = []
    start = _log[i][0]
    while _log[i][0]+1 == _log[i+1][0] and i <len(_log)-2:
        j.append(_log[i][1])
        i += 1
    log[start] = j
    sts.append(start)
    i += 1
del _log

total = []
SOC = [100]

capacity = 60
chargerate = 50

d = 0
t = 0
while d < len(sts):
    
    dc = Drivecycle(log[sts[d]])
    energy = car.getEnergyExpenditurePerSecond(dc)
    while t < sts[d]:
        SOC.append(SOC[-1])
        t += 1
    t2 = 0
    while t2 < len(energy)-1:
        SOC.append(SOC[-1]-energy[t2]*100/capacity)
        t2 += 1
    t = t2
    d += 1
    if d == len(sts):
        while SOC[-1] < 100:
            SOC.append(SOC[-1]+chargerate*100/(3600*capacity))
    else:
        while t < sts[d] and SOC[-1] < 100:
            SOC.append(SOC[-1]+chargerate*100/(3600*capacity))
            t += 1

plt.figure()
for day in range(16):
    plt.subplot(4,4,day+1)
    plt.plot(SOC)
    plt.xlim(86400*day,86400*(day+1))
    plt.xticks(np.linspace(86400*day+14400,86400*(day+1)-+14400,3),
               ['04:00','12:00','20:00'])
    plt.grid()
    plt.ylim(0,100)
plt.tight_layout()
plt.show()
# note velocity is in kmph'''
