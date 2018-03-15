# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction2 import EnergyPrediction

outfiles = {'1':'../../epg-psopt/constance/LV/EVchargingWedJanUC.csv',
            '2':'../../epg-psopt/constance/LV/EVchargingWedJanUT.csv',
            '3':'../../epg-psopt/constance/LV/EVchargingWedJanRT.csv',
            '4':'../../epg-psopt/constance/LV/EVchargingWedJanRV.csv'}

regionType = [0.0]*4
for rt in outfiles:
    regionType[int(rt)-1] = 1.0
    run = EnergyPrediction('2','1',regionType,10000,car='teslaS60D',
                           smoothTimes=True,recordVehicles=True)
    results = run.get_vehicle_requirements(1000)
    
    with open(outfiles[rt],'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row)
    
    regionType[int(rt)-1] = 0.0
