import numpy as np
import matplotlib.pyplot as plt
import csv
from NTSenergyPrediction2 import NationalEnergyPrediction
from fitDistributions import Inference
import copy


resultsStem = '../../Documents/simulation_results/NTS/national_stochastic/'
deadline = 16

header = ['t']
for i in range(1,4):
    header.append('base'+str(i))
for i in range(1,10):
    header.append('sceanrio'+str(i))
    
for month in ['1','4','7','10']:
    run = NationalEnergyPrediction('2',month)
    o,a,b = run.getStochasticOptimalLoadFlatteningProfile4()

    with open(resultsStem+month+'_planned.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for t in range(len(o[0])):
            writer.writerow([10*t,b[0][t]/1000000,b[1][t]/1000000,
                             b[2][t]/1000000,o[0][t]/1000000,o[1][t]/1000000,
                             o[2][t]/1000000,o[3][t]/1000000,o[4][t]/1000000,
                             o[5][t]/1000000,o[6][t]/1000000,o[7][t]/1000000,
                             o[8][t]/1000000])

    with open(resultsStem+month+'_experienced.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for t in range(len(o[0])):
            writer.writerow([10*t,b[0][t]/1000000,b[1][t]/1000000,
                             b[2][t]/1000000,a[0][t]/1000000,a[1][t]/1000000,
                             a[2][t]/1000000,a[3][t]/1000000,a[4][t]/1000000,
                             a[5][t]/1000000,a[6][t]/1000000,a[7][t]/1000000,
                             a[8][t]/1000000])
