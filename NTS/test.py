import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction
'''
run = NationalEnergyPrediction('3','1',smoothTimes=True)
run.getOptimalLoadFlattening(3.5)

'''

run = NationalEnergyPrediction('2','1')
#d = run.getDumbCharging(3.5)
p = run.getApproximateLoadFlattening(3.5,60)


for i in range(len(p)):
    p[i] += run.baseLoad[i]


plt.figure(1)
plt.plot(p)
plt.plot(run.baseload)
plt.show()

