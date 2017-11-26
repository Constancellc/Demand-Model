# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
#from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import NationalEnergyPrediction

profiles = {}

fileStem = '../../Documents/NationalProfiles/'

nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}

for m in range(1,2):#13):
    month = str(m)
    profiles[month] = {}

    for i in range(1,8):
        profiles[month][str(i)] = [0.0]*1440
        
    for d in range(1,8):
        day = str(d)
        run = NationalEnergyPrediction(day,month,vehicle='teslaS60D',smoothTimes=True)
        dumbProfile = run.getDumbChargingProfile(3.5,36) # kW

        for i in range(len(dumbProfile)):
            if i < 60*24:
                profiles[month][day][i] += dumbProfile[i] # kW
            else:
                profiles[month][nextDay[day]][i-1440] += dumbProfile[i]


ms = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun',
      '7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
ds = {'1':'Mon','2':'Tue','3':'Wed','4':'Thu','5':'Fri','6':'Sat','7':'Sun'}

for month in profiles:
    with open(fileStem+ms[month]+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (mins past midnight)','Mon','Tue','Wed','Thu',
                         'Fri','Sat','Sun'])
        for i in range(0,1440):
            row = [i+1]
            for day in profiles[month]:
                row.append(profiles[month][day][i])
            writer.writerow(row)
