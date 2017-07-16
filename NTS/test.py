import matplotlib.pyplot as plt
import numpy as np

from NTSenergyPrediction import NationalEnergyPrediction, NationalEnergyPrediction2


new = NationalEnergyPrediction2('3','1')
new.getDumbChargingProfile(3.5,36)
mc = new.getMissingCapacity()

plt.figure(1)
plt.plot(mc)
plt.show()
