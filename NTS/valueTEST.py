# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

from NTSvalueAssesment import ValueAssesment

test = ValueAssesment('3',1,car=None,regionType='3',smoothTimes=True)
test.chargeOpportunistically(3.5,30)
#p = test.getTotalCapacity()
p = test.total
diff = []
total = 0
'''
for i in range(1440*7):
    diff.append(test.rtPower[i]/60-test.demand[i]/60)
    total += (test.rtPower[i]/60-test.demand[i]/60)

print(p[-1])
'''
plt.figure(1)
plt.subplot(2,1,1)
plt.title('Total Capacity')
plt.plot(p)
plt.fill_between(range(1440*7),test.max,test.min,alpha=0.2)
plt.grid()
plt.subplot(2,1,2)
plt.title('Charging Power')
plt.plot(test.demand)
'''
plt.subplot(4,1,2)
plt.plot(test.demand)
plt.subplot(4,1,3)
plt.plot(test.rtPower)
plt.subplot(4,1,4)
plt.plot(diff)
'''
plt.grid()

plt.show()
