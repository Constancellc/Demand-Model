# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle, Vehicle

vehicles = {'nissanLeafS':Vehicle(1647.7,29.97,0.0713,0.02206,0.84,24.0),
            'nissanLeafSL':Vehicle(1647.7,29.61,0.0738,0.02195,0.86,30.0),
            'nissanLeafSV':Vehicle(1704.5,29.92,0.076,0.02195,0.847,30.0),
            'bmwI3':Vehicle(1420.4,22.9,0.346,0.01626,0.849,18.8),
            'teslaS60D':Vehicle(2272.7,37.37,0.1842,0.01508,0.969,60.0),
            'teslaS60R':Vehicle(2272.7,40.35,0.1324,0.01557,0.884,60.0),
            'teslaS70D':Vehicle(2272.7,36.23,0.1906,0.01746,0.865,70.0),
            'teslaS75D':Vehicle(2272.7,37.37,0.1842,0.01508,0.964,75.0),
            'teslaS75R':Vehicle(2272.7,40.35,0.1324,0.01557,0.943,75.0),
            'teslaS85D':Vehicle(2272.7,36.23,0.1906,0.01746,0.86,85.0),
            'teslaS90D':Vehicle(2272.7,39.24,0.1493,0.01514,0.952,90.0),
            'teslaSP100D':Vehicle(2386.4,41.35,0.267,0.0137,0.956,100.0),
            'teslaP85D':Vehicle(2386.4,41.91,0.1389,0.0185,0.812,85.0),
            'teslaSP90D':Vehicle(2386.4,41.51,0.2226,0.01403,0.939,90.0),
            'teslaX60D':Vehicle(2500.0,37.68,0.0486,0.0214,0.953,60.0),
            'teslaX75D':Vehicle(2500.0,37.68,0.0486,0.0214,0.957,75.0),
            'teslaX90D':Vehicle(2500.0,37.68,0.0486,0.0214,0.931,90.0),
            'teslaXP10D':Vehicle(2727.3,45.71,-0.0555,0.0216,0.928,100.0),
            'BYDe6':Vehicle(2500,69.473,0.0697,0.02814,0.911,61.0),
            'chevroletSpark':Vehicle(1420.45,21.96,0.1688,0.01806,0.78,19.0),
            'fiat500e':Vehicle(1477.3,24.91,0.2365,0.01816,0.79,22.0),
            'toyotaScionIQ':Vehicle(1250,15.993,0.56499,0.013095,0.844,12.0),
            'toyotaRAV4':Vehicle(1931.8,32.246,0.27335,0.022058,0.721,41.8),
            'VWeGolf':Vehicle(1647.7,39.36,0.5083,0.0125,0.942,24.2),
            'kiaSoul':Vehicle(1647.7,22.058,0.25763,0.022168,0.881,27.0),
            'coda':Vehicle(1818.2,39.18,0.2549,0.0199,0.635,31.0),
            'mercedesBclass':Vehicle(1931.8,31.7,0.177,0.019,0.681,36.0),
            'mercedesSmart':Vehicle(1079.5,32.869,-0.1639,0.028583,0.786,17.6),
            'hondaFit':Vehicle(1647.7,19.06,0.407,0.01499,0.813,20.0),
            'mitsubishiMiEV':Vehicle(1306.8,19.484,0.43515,0.016133,0.752,16.0)}

pvehicles = ['bmwI3','mitsubishiMiEV','nissanLeafS','teslaS60D','teslaSP100D']
plt.figure(1)
n = 1
for dc in ['rural','urban','motorway']:
    cycle = Drivecycle(10000,dc)        
    x_ticks = []
    energy = []
    for v in pvehicles:
        x_ticks.append(v)
        energy.append(vehicles[v].getEnergyExpenditure(cycle,0))
    plt.subplot(3,1,n)
    plt.bar(range(len(energy)),energy)
    plt.xticks(range(len(energy)),x_ticks,rotation='vertical')
    plt.title(dc)
    n += 1
plt.show()
        
