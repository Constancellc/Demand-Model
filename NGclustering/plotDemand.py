import matplotlib.pyplot as plt
import numpy as np
import csv

maxDemand = 0

profiles = {}
with open('../../Documents/gridwatch.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
        '''
        year = row[1][:4]
        month = row[1][5:7]
        day = int(row[1][8:10]
        '''
        date = row[:10]
        if date not in profiles:
            profiles[date] = [0.0]*24*12
            
        time = int(row[1][11:13])*12+int(int(row[1][14:16])/5)

        demand = int(row[2])

        if demand > maxDemand:
            maxDemand = demand

        profiles[date][time] = demand

for date in profiles:
    for time in profiles[date]:
        profiles[date][time] = profiles[date][time]/maxDemand


