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

for cp in [3.5,7,21,50,145]:
    print(cp,end='')
    print('kW')
    n = []
    for i in range(len(base)):
        n.append(round((70000000-base[i])/(cp*320000),2))
    print(min(n))
    print(max(n))


