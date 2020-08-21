import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

charge_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

trip_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

chosenVehicle = 'ST1001'
# first I want to extract the training data
dType = {}
log = {}
known = []
with open(charge_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] != chosenVehicle:
            continue
        d = int(row[1])
        s = int(row[2])
        e = int(row[3]) # can be greater than 1440
        c = float(row[4])
        known.append([d,s])
        if d not in dType:
            dType[d] = int(float(row[6]))
            log[d] = []
        log[d].append([s,'c',c]) # start time (1440), charge flag, SOC (0-1)
        

with open(trip_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] != chosenVehicle:
            continue
        d = int(row[1])
        s = int(row[2])
        e = int(row[3])
        c = float(row[5])/24000 # Wh to % soc
        if d not in dType:
            dType[d] = int(float(row[6]))
            log[d] = []
        log[d].append([s,'j',e,c]) # start time (1440), charge flag, SOC (0-1)
        
# now I need to compile a log for each day, filling in SOC as necessary
soc = 0.99
d = 121
save_log = []
print(dType[d])
while dType[d] == 0:
    d += 1
while dType[d] == 1:
    d += 1
    print(dType[d])
for i in range(14):
    save_log += [[d]]
    save_log += sorted(log[d])
    d += 1

with open(chosenVehicle+'_'+str(d-14)+'to'+str(d)+'.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in save_log:
        writer.writerow(row)

