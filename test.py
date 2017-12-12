import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from vehicleModel import Drivecycle, Vehicle

dc = Drivecycle(2000,'urban')
car = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)

car.getEnergyExpenditure(dc,0.0)
