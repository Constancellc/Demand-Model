# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction

outfiles = {'1':'../../Documents/thomas/EVchargingWedJanUC.csv',
            '2':'../../Documents/thomas/EVchargingWedJanUT.csv',
            '3':'../../Documents/thomas/EVchargingWedJanRT.csv',
            '4':'../../Documents/thomas/EVchargingWedJanRV.csv'}

for rt in outfiles:
    run = EnergyPrediction('3','1',regionType=rt,smoothTimes=True) # Wednesday, rural town
    run.getNextDayStartTimes()
    reqs = {}
    for vehicle in run.energy:
        reqs[vehicle] = [run.endTimes[vehicle],run.startTimes[vehicle]+1440,
                         run.energy[vehicle],round(run.distance[vehicle]/1609.34,1)]
        
    with open(outfiles[rt],'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['VehicleID','arrival (mins past 0:00)',
                         'departure (mins past 0:00)','consumption (kWh)',
                         'distance driven (miles)'])
        for vehicle in reqs:
            writer.writerow([vehicle]+reqs[vehicle])
