# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import AreaEnergyPrediction

elecData = '../../Documents/Elec_demand_oneyear.csv'
outfileStem = '../../Documents/bicesterSmart'


data = []
with open(elecData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        data.append(float(row[1]))

firstOfMonth = [0,744,1416,2160,2880,3624,4344,5088,5832,6552,7296,8016,8760]
stdProfiles = []

for i in range(12):
    p = [0.0]*24
    for j in range(firstOfMonth[i],firstOfMonth[i+1]):
        p[j%24] += data[j]

    newp = [0.0]*36*60

    for j in range(len(newp)):
        try:
            newp[j] = p[int(j/60)]
        except:
            newp[j] = p[int(j/60)-24]
    stdProfiles.append(newp)


pen = 0.3

mo = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun','7':'Jul',
      '8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
da = {'1':'Mon','2':'Tue','3':'Wed','4':'Thu','5':'Fri','6':'Sat','7':'Sun'}

for nph in [3]:
    for mi in range(1,13):
        m = str(mi)
        for di in range(1,8):
            d = str(di)
            run = AreaEnergyPrediction('8',0,int(pen*nph*1700),0,0,d,m,
                                       vehicle='teslaS60D')
            dumb = run.getPsuedoOptimalProfile(3.5,baseLoad=stdProfiles[mi-1])

            newDumb = [0.0]*24*2

            # switch to half hourly data and wrap around
            for i in range(0,len(dumb)):
                if int(i/30) < len(newDumb):
                    newDumb[int(i/30)] += dumb[i]/30
                else:
                    newDumb[int(i/30)-24*2] += dumb[i]/30

            with open(outfileStem+str(nph)+'/'+mo[m]+'-'+da[d]+'.csv','w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Time (mins past 00:00)','Power Demand (kW)'])
                for i in range(0,len(newDumb)):
                    writer.writerow([str(int((i+0.5)*30)),newDumb[i]])
        
