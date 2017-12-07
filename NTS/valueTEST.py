# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

from NTSvalueAssesment import ValueAssesment

test = ValueAssesment('3',1000,region='9',smoothTimes=True)

p = test.getTotalCapacity()

plt.figure(1)
plt.plot(p)
plt.show()
