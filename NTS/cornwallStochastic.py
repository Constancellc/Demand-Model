import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction, CornwallEnergyPrediction
from fitDistributions import Inference
import copy
import csv

# this one considers 3 baseloads and 5 thresholds without solar generation 
resultsStem = '../../Documents/simulation_results/NTS/cornwall/'

for month in ['1','4','7','10']:
    run = CornwallEnergyPrediction('2',month,solar=False)
    o,a,b = run.getStochasticOptimalLoadFlatteningProfile()

    with open(resultsStem+month+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for t in range(len(o[0])):
            writer.writerow([10*t,b[0][t]/1000,b[1][t]/1000,b[2][t]/1000,
                             a[0][t]/1000,a[1][t]/1000,a[2][t]/1000,
                             a[3][t]/1000,a[4][t]/1000,a[5][t]/1000,
                             a[6][t]/1000,a[7][t]/1000,a[8][t]/1000,
                             a[9][t]/1000,a[10][t]/1000,a[11][t]/1000,
                             a[12][t]/1000,a[13][t]/1000,a[14][t]/1000])
