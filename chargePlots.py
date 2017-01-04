import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import datetime

"""
THIS FILE EXPLOITS THE PERSUITS OF CHARGETESTING, WHICH CREATES A LOG OF
JOURNEY FINISH TIMES AND ENERGY EXPEDITURES.

CURRENTLY THE ONLY CHARGING MODEL EXPLORED IS THAT WHERE EVERYONE PLUGS IN THE
EV AS SOON AS THE JOURNEY IS FINISHED.

THE CHARGING POWER IS ASSUMED FIXED, ALTHOUGH SEVERAL POWERS ARE EXPLORED.
"""

"""
to do list:
- change axis of graph to display the time
"""
# first set up vector to plot
times = []

#for hour in range(0,24):
#    for minute in range(0,60):
#        for second in range(0,60):
#        times.append(datetime.time(hour,minute))

"""
# how to run testCharging?
speed = {43:'rapid',7:'fast',3:'slow'}
for chargePower in [43, 7, 3]:

    powers = [0.0]*24*60*60


    with open('journeysModel.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            secondsCharging = int(float(row['energy expended'])*60*60/chargePower)
            for i in range(int(row['index']),int(row['index'])+secondsCharging):
                if i >= 24*60*60:
                    i -= 24*60*60
                    
                powers[i] += chargePower

    plt.plot(np.linspace(0,24,num=24*60*60),powers, label=speed[chargePower])
plt.legend(loc='upper left')
plt.xlabel('time /hour')
plt.ylabel('total energy /kWh')
plt.show()
        
# ok let's try something slightly different
"""

chargeProbability = 0.3

#for chargeProbability in [0.1, 0.5]:
speed = {43:'rapid',7:'fast',3:'slow'}
for chargePower in [43, 7, 3]:
    
    energy = 0
    powers2 = [0.0]*24*60*60

    with open('journeysModel.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            energy += float(row['energy expended'])
            if random.random() <= chargeProbability:
                chargeTime = int(energy*60*60/chargePower)
                for i in range(int(row['index']),int(row['index'])+chargeTime):
                    if i >= 24*60*60:
                        i -= 24*60*60
                        
                    powers2[i] += chargePower
                    energy = 0

    plt.plot(np.linspace(0,24,num=24*60*60),powers2, label=speed[chargePower])
plt.legend(loc='upper left')
plt.xlabel('time /hour')
plt.ylabel('total energy /kWh')
plt.show()
"""
energy = 0
batteryCap = 32 # kWh

powers3 = [0.0]*24*60*60

with open('journeysModel.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        energy += float(row['energy expended'])
        if energy <= 0.5*batteryCap:
            continue
        else:
            if random.random() < 0.8 or energy >= 0.9*batteryCap:
                chargeTime = int(energy*60*60/4)
                for i in range(int(row['index']),int(row['index'])+chargeTime):
                    if i >= 24*60*60:
                        i -= 24*60*60
                        
                    powers3[i] += 4
                    energy = 0
            else:
                continue

plt.plot(powers3)
plt.show()
"""               
