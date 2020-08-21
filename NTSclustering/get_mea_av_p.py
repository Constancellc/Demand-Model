import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

charge_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

max_days = {}
wday = [0.0]*48
wend = [0.0]*48
nc = 0
with open(charge_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        nc += 1
        v = row[0]
        day = int(row[1])
        if v not in max_days:
            max_days[v] = day
        else:
            if day > max_days[v]:
                max_days[v] = day
        t = int(int(row[2])/30)
        if row[6] == '1':
            wend[t] += 1
        else:
            wday[t] += 1

# get total number of vehicle weeks
print(nc)
wks = 0
for v in max_days:
    wks += max_days[v]
print(wks)

p = wday*5+wend*2
for t in range(5*48):
    p[t] = p[t]/(wks*5/7)
for t in range(5*48,7*48):
    p[t] = p[t]/(wks*2/7)


with open('mea_av.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for t in p:
        writer.writerow([t])
    
