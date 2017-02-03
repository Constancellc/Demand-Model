import numpy as np
import matplotlib.pyplot as plt
import random
import csv

data = []

with open('ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == '03-Feb-16':
            data.append(row[4])

nd = data[8:]+data[0:8]
print nd

plt.figure(1)
plt.plot(nd)
plt.show()
