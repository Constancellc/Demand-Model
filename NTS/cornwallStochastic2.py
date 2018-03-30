import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction, CornwallEnergyPrediction
from fitDistributions import Inference
import copy
import csv

resultsStem = '../../Documents/simulation_results/NTS/cornwall2/'

for month in ['1','4','7','10']:
    run = CornwallEnergyPrediction('2',month,solar=True)
    #dumb = run.getDumbCharging(3.5,nHours=48+16)
    o,a,b = run.getStochasticOptimalLoadFlatteningProfile3()

    with open(resultsStem+month+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base1','base2','base3',0.1,0.8,0.1])
        for t in range(len(o[0])):
            writer.writerow([10*t,b[0][t]/1000,b[1][t]/1000,b[2][t]/1000,
                             a[0][t]/1000,a[1][t]/1000,a[2][t]/1000])
