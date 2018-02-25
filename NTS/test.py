import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction, TwoDayEnergyPrediction
'''
run = NationalEnergyPrediction('3','1',smoothTimes=True)
run.getOptimalLoadFlattening(3.5)

'''

run = NationalEnergyPrediction('2','1')
p = run.getOptimalLoadFlattening(3.5)

for i in range(len(p)):
    p[i] += baseload[i]
    
plt.figure(1)
plt.plot(p)
plt.plot(run.baseload)
plt.show()

