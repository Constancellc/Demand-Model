import numpy as np
import matplotlib.pyplot as plt
from NTSenergyPrediction2 import NationalEnergyPrediction

run = NationalEnergyPrediction('3','1',smoothTimes=True)
run.getOptimalLoadFlatteningProfile([1.0]*36*60)

