import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction, CornwallEnergyPrediction
from fitDistributions import Inference
import copy

resultsStem = '../../Documents/simulation_results/NTS/cornwall/'

for month in ['1','4','7','10']:
    run = CornwallEnergyPrediction('2',month,solar=True)
    dumb = run.getDumbCharging(3.5,nHours=48+16)
    o,a,b = run.getStochasticOptimalLoadFlatteningProfile2()

    dumb2 = [0.0]*len(a[0])
    for i in range(len(dumb)):
        dumb2[int(i/10)] += dumb[i]/10

    with open(resultsStem+month+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base','dumb',0.05,0.2,0.5,0.2,0.05])
        for t in range(len(o[0])):
            writer.writerow([10*t,dumb2[t]/1000,b[t]/1000,a[0][t]/1000,
                             a[1][t]/1000,a[2][t]/1000,a[3][t]/1000,a[4][t]/1000])

