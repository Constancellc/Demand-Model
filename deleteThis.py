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
        
slowI1 = []        
slowI2 = []        
slowI3= []
with open('../Downloads/openDSScurrents/line6-slow.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        slowI1.append(float(row[8]))
        slowI2.append(float(row[10]))
        slowI3.append(float(row[12]))

noneI1 = []        
noneI2 = []        
noneI3= []
with open('../Downloads/openDSScurrents/line6-none.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        noneI1.append(float(row[8]))
        noneI2.append(float(row[10]))
        noneI3.append(float(row[12]))

t = np.linspace(0,24,num=1440)
xaxis2 = np.linspace(2,22,num=6)
my_xticks2 = ['02:00','06:00','10:00','14:00','18:00','22:00']


plt.figure(1)
plt.subplot(3,2,1)
plt.plot(t,dumbI1,label='dumb')
plt.plot(t,smartI1,label='valley filling')
plt.plot(t,slowI1,label='slow')
plt.plot(t,noneI1,label='no vehicles')
plt.legend()
plt.title('Phase 1')
plt.ylabel('Current (A)')
plt.xlim(0,24)
plt.xticks(xaxis2, my_xticks2)
plt.grid()

plt.subplot(3,2,3)
plt.plot(t,dumbI2)
plt.plot(t,slowI2)
plt.plot(t,smartI2)
plt.plot(t,noneI2)
plt.title('Phase 2')
plt.xlim(0,24)
plt.ylabel('Current (A)')
plt.xticks(xaxis2, my_xticks2)
plt.grid()

plt.subplot(3,2,5)
plt.plot(t,dumbI3)
plt.plot(t,slowI3)
plt.plot(t,smartI3)
plt.plot(t,noneI3)
plt.title('Phase 3')
plt.ylabel('Current (A)')
plt.xlim(0,24)
plt.xlabel('time')
plt.xticks(xaxis2, my_xticks2)
plt.grid()

dumbV1 = []
dumbV2 = []
dumbV3 = []
with open('../Downloads/openDSScurrents/line862-dumb.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        dumbV1.append(float(row[2]))
        dumbV2.append(float(row[4]))
        dumbV3.append(float(row[6]))
        
smartV1 = []        
smartV2 = []        
smartV3= []
with open('../Downloads/openDSScurrents/line862-smart.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        smartV1.append(float(row[2]))
        smartV2.append(float(row[4]))
        smartV3.append(float(row[6]))

        
slowV1 = []        
slowV2 = []        
slowV3= []
with open('../Downloads/openDSScurrents/line862-slow.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        slowV1.append(float(row[2]))
        slowV2.append(float(row[4]))
        slowV3.append(float(row[6]))

noneV1 = []        
noneV2 = []        
noneV3= []
with open('../Downloads/openDSScurrents/line862-none.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        noneV1.append(float(row[2]))
        noneV2.append(float(row[4]))
        noneV3.append(float(row[6]))


plt.subplot(3,2,2)
plt.plot(t,dumbV1,label='dumb')
plt.plot(t,smartV1,label='valley filling')
plt.plot(t,slowV1)
plt.plot(t,noneV1)
#plt.legend()
plt.title('Phase 1')
plt.ylabel('Voltage (V)')
plt.xlim(0,24)
plt.xticks(xaxis2, my_xticks2)
plt.grid()

plt.subplot(3,2,4)
plt.plot(t,dumbV2)
plt.plot(t,smartV2)
plt.plot(t,slowV2)
plt.plot(t,noneV2)
plt.title('Phase 2')
plt.ylabel('Voltage (V)')
plt.xlim(0,24)
plt.xticks(xaxis2, my_xticks2)
plt.grid()

plt.subplot(3,2,6)
plt.plot(t,dumbV3)
plt.plot(t,smartV3)
plt.plot(t,slowV3)
plt.plot(t,noneV3)
plt.title('Phase 3')
plt.ylabel('Voltage (V)')
plt.xlim(0,24)
plt.xticks(xaxis2, my_xticks2)
plt.xlabel('time')
plt.grid()


p1 = 0
p2 = 0
for i in range(0,1440):
    p1 += dumbI1[i]*dumbI1[i]
    p2 += smartI1[i]*smartI1[i]

print p1
print p2

plt.show()
