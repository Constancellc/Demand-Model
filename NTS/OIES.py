# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from NTSenergyPrediction import EnergyPrediction, BaseLoad

day = '3'
month = '1'

runBase = BaseLoad(day,month,24,unit='k')
base = runBase.getLoad()

for cp in [3.5,7,21,50,200]:
    print(cp,end='')
    print('kW')
    n = []
    for i in range(len(base)):
        n.append(int((60000000-base[i])/cp))
    print(min(n))
    print(max(n))


