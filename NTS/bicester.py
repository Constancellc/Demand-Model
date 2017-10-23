# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import AreaEnergyPrediction

outfileStem = '../../Documents/bicester'

nph = 3 # number per household

mo = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun','7':'Jul',
      '8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
da = {'1':'Mon','2':'Tue','3':'Wed','4':'Thu','5':'Fri','6':'Sat','7':'Sun'}

run = AreaEnergyPrediction(day,month,regionType='2',region='')
run.getDumbChargingProfile

# switch to half hourly data


with open(outfileStem+mo[m]+'-'da[d]+'.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time (mins past 00:00)','Power Demand (kW)'])
