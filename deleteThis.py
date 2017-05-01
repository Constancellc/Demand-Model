# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

dumbI1 = []
dumbI2 = []
dumbI3 = []
with open('../Downloads/openDSScurrents/line6-dumb.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        dumbI1.append(float(row[8]))
        dumbI2.append(float(row[10]))
        dumbI3.append(float(row[12]))
        
smartI1 = []        
smartI2 = []        
smartI3= []
with open('../Downloads/openDSScurrents/line6-smart.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        smartI1.append(float(row[8]))
        smartI2.append(float(row[10]))
        smartI3.append(float(row[12]))

t = np.linspace(0,24,num=1440)
plt.figure(1)
plt.subplot(3,1,1)
plt.plot(t,dumbI1)
plt.plot(t,smartI1)
plt.subplot(3,1,2)
plt.plot(t,dumbI2)
plt.plot(t,smartI2)
plt.subplot(3,1,3)
plt.plot(t,dumbI3)
plt.plot(t,smartI3)


p1 = 0
p2 = 0
for i in range(0,1440):
    p1 += dumbI1[i]*dumbI1[i]
    p2 += smartI1[i]*smartI1[i]

print p1
print p2

plt.show()
