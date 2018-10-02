import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from chargingModel import MC_Sim

outstem = '../../Documents/simulation_results/NTS/clustering/power/'

nV = 50
nMC = 40
'''
sim = MC_Sim(nV)
sim.run(nMC,outstem+'charging.csv')

del sim
'''
sim = MC_Sim(nV,typ='available')
sim.run(nMC,outstem+'available.csv')

