# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
#from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import NationalEnergyPrediction

heatplot = np.zeros((1440,12*4*7))

#fileStem = '../../Documents/NationalProfiles/'

fileStem = '../../Documents/NationalProfilesRT/'

ms = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun',
      '7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
for m in range(1,13):
    month = str(m)
    #with open(fileStem+ms[month]+'.csv','rU') as csvfile:
    with open(fileStem+ms[month]+'RT.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        t = 0
        for row in reader:
            for k in range(0,4):
                for j in range(0,7):
                    heatplot[1399-t][7*4*(m-1)+7*k+j] = float(row[1+j])/1000000 # kW->GW
            t += 1

y = range(2*60,26*60,4*60)
y_ticks = ['22:00','18:00','14:00','10:00','06:00','02:00']

x = range(14,14+12*4*7,7*4)
x_ticks = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov',
           'Dec']
plt.figure(1)
plt.imshow(heatplot,aspect=0.1)
plt.colorbar()
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.show()
