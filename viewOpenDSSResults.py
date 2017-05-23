# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random


styles = ['none','dumb','national','household','network']
I = {}
V = {}

for style in styles:
    I[style] = {1:[],2:[],3:[]}
    V[style] = {1:[],2:[],3:[]}
    
    with open('../Downloads/openDSScurrents/line6-'+style+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            for i in range(1,4):
                I[style][i].append(float(row[6+2*i]))
                
    with open('../Downloads/openDSScurrents/line862-'+style+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            for i in range(1,4):
                V[style][i].append(float(row[2*i]))

t = np.linspace(0,24,num=1440)
xaxis2 = np.linspace(2,22,num=6)
my_xticks2 = ['02:00','06:00','10:00','14:00','18:00','22:00']


plt.figure(1)
for i in range(1,4):
    plt.subplot(3,2,2*i-1)
    for style in styles:
        plt.plot(t,I[style][i],label=style)
    plt.title('Phase '+str(i))
    plt.ylabel('Current (A)')
    plt.xlim(0,24)
    plt.xticks(xaxis2, my_xticks2)
    plt.grid()
    if i == 1:
        plt.legend()

for i in range(1,4):
    plt.subplot(3,2,2*i)
    for style in styles:
        plt.plot(t,V[style][i],label=style)
    plt.title('Phase '+str(i))
    plt.ylabel('Voltage (V)')
    plt.xlim(0,24)
    plt.xticks(xaxis2, my_xticks2)
    plt.grid()
    if i == 1:
        plt.legend()

plt.figure(2)
for style in styles:
    plt.plot(t,I[style][2],label=style)
plt.ylabel('Current (A)')
plt.xlim(0,24)
plt.xticks(xaxis2, my_xticks2)
plt.grid()
plt.legend()


for style in styles:
    print style
    print 'max: ',
    print max(I[style][3])
    print 'min: ',
    print min(I[style][3])
    print '-------'
                               
plt.show()
