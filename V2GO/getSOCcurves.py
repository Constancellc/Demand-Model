# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
from vehicleModelV2GO import Drivecycle, Vehicle
import datetime

stem = '../../Documents/V2GO/EV_data_processed/WithElevation/'
vehicle = '356449064315004'

car = Vehicle(3000,102.5,3.63,0.422,0.85,90)

# okay, what do we want to do with the vehicle model?
vehicles = ['356449064315004','356449064371353','356449064394454',
            '356449064404196']
start_day = [16,11,21,19]
days_recorded = [15,19,9,12]
# we want to segment the diary into a dictionary of journeys I suspect

for ii in range(4):
    vehicle = vehicles[ii]
    plt.figure(figsize=(5,3))
    plt.rcParams["font.family"] = 'serif'
    plt.rcParams["font.size"] = '8'
    plt.title(vehicle)
    plt.grid(ls=':')
    plt.ylim(0,100)
    plt.xlim(0,24)
    plt.ylabel('SOC (%)')
    
    time0 = datetime.datetime(2016,11,int(start_day[ii]))
    results = []
    for day in range(days_recorded[ii]):
        v = []
        sl =[]
        earliest = 86400
        latest = 0
        try:
            with open(stem+vehicle+'_on_2016-11-'+str(16+day)+'_elv.csv',
                      'rU') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    h = int(row[0][:2])
                    m = int(row[0][3:5])
                    s = int(row[0][6:8])
                    t = 3600*h+60*m+s
                    if t < earliest:
                        earliest = t
                    if t > latest:
                        latest = t
                    v.append(float(row[-4]))
                    sl.append(0)#float(row[-1]))
                    
        except:
            continue
        dc = Drivecycle(v,sl)
        energy = car.getEnergyExpenditurePerSecond(dc)
        '''
        plt.figure()
        plt.subplot(3,1,1)
        plt.plot(v)
        plt.subplot(3,1,2)
        plt.plot(sl)
        plt.subplot(3,1,3)
        plt.plot(energy)
        plt.show()'''

        # so this will be a vector of kWh consumed per second

        capacity = 60

        
        
        

        SOC = [100]
        for t in range(len(energy)):
            SOC.append(SOC[-1]-100*energy[t]/capacity)
        plt.plot(np.linspace(0,24,num=len(SOC)),SOC,
                 label=str(time0+datetime.timedelta(day))[:10])
            
        '''
        results.append([time0+datetime.timedelta(days=day,seconds=earliest),
                        time0+datetime.timedelta(days=day,seconds=latest),
                        energy])'''
    plt.xticks([2,6,10,14,18,22],['02:00','06:00','10:00','14:00','18:00',
                                  '22:00'])
    plt.legend(ncol=3)
    plt.tight_layout()
    plt.savefig(stem+'/predicted/'+str(vehicle)+'_no_elev.pdf',format='pdf')

'''
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
