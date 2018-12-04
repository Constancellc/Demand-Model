import matplotlib.pyplot as plt
import numpy as np
import csv
import random


power = [0,0.1,0.3,0.5,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3]
eff = [0,0.2,0.38,0.5,0.7,0.79,0.82,0.85,0.87,0.88,0.89,0.9,0.9]

grid = [0]
for i in range(1,len(power)):
    grid.append(power[i]/eff[i])

plt.figure()
plt.plot(power,power)
plt.plot(power,grid)
plt.show()


