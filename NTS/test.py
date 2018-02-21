import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction, TwoDayEnergyPrediction

run = NationalEnergyPrediction('3','1',smoothTimes=True)
run.getOptimalLoadFlattening(3.5)

'''

run = TwoDayEnergyPrediction('2','1',[0.4,0.4,0.1,0.1],65640000)
p = run.getDumbCharging(3.5)

plt.figure(1)
plt.plot(p)
plt.show()
'''
