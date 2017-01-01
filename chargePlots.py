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


# how to run testCharging?

for chargePower in [0.5, 40]:

    powers = [0.0]*24*60*60


    with open('journeysModel.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            secondsCharging = int(float(row['energy expended'])*60*60/chargePower)
            for i in range(int(row['index']),int(row['index'])+secondsCharging):
                if i >= 24*60*60:
                    i -= 24*60*60
                    
                powers[i] += chargePower

    plt.plot(np.linspace(0,24,num=24*60*60),powers)
plt.show()
        
        
