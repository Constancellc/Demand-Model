# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random


styles = ['NONE','DUMB','NATIONAL','HOUSEHOLD','NETWORK']
I = {}

for style in styles:
    I[style] = {1:[],2:[],3:[]}
    
    with open('../Downloads/openDSScurrents/currents-'+style+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            for i in range(1,4):
                try:
                    I[style][i].append(float(row[i]))
                except:
                    continue


t = np.linspace(0,24,num=1440)
xaxis2 = np.linspace(2,22,num=6)
my_xticks2 = ['02:00','06:00','10:00','14:00','18:00','22:00']

'''
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
'''

plt.figure(1)

for phase in range(1,4):
    plt.subplot(3,1,phase)
    for style in styles:
        plt.plot(t,I[style][phase],label=style)
    plt.ylabel('Current (A)')
    plt.xlim(0,24)
    plt.xticks(xaxis2, my_xticks2)
    plt.grid()
    if phase == 1:
        plt.legend()

    print 'PHASE ' + str(phase)


    for style in styles:
        print style
        print 'max: ',
        print max(I[style][phase])
        print 'min: ',
        print min(I[style][phase])
        print '-------'

plt.figure(2)
for style in styles:
    I2 = [0.0]*1440
    for phase in range(1,4):
        for i in range(0,1440):
            I2[i] += I[style][phase][i]*I[style][phase][i]
    plt.plot(t,I2,label=style)
plt.xlim(0,24)
plt.xticks(xaxis2,my_xticks2)
plt.legend()
    
plt.show()
