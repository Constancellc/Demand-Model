import numpy as np
import matplotlib.pyplot as plt
import csv
from NTSenergyPrediction2 import NationalEnergyPrediction
from fitDistributions import Inference
import copy


resultsStem = '../../Documents/simulation_results/NTS/national_stochastic/'
deadline = 16

for month in ['1','4','7','10']:
    run = NationalEnergyPrediction('2',month)
    o,a,b = run.getStochasticOptimalLoadFlatteningProfile2()

    with open(resultsStem+month+'_planned.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base',0.05,0.2,0.5,0.2,0.05])
        for t in range(len(o[0])):
            writer.writerow([10*t,b[t]/1000000,o[0][t]/1000000,o[1][t]/1000000,
                             o[2][t]/1000000,o[3][t]/1000000,o[4][t]/1000000])

    with open(resultsStem+month+'_experienced.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base',0.05,0.2,0.5,0.2,0.05])
        for t in range(len(o[0])):
            writer.writerow([10*t,b[t]/1000000,a[0][t]/1000000,a[1][t]/1000000,
                             a[2][t]/1000000,a[3][t]/1000000,a[4][t]/1000000])
