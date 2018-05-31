import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import copy

stem = '../../Documents/pecan-street/mueller-solar/'

day0 = datetime.datetime(2018,1,1)

maxs = {}

for file in ['jan18_1','jan18_2','jan18_3','feb18_1','feb18_2','feb18_3']:         
    with open(stem+file+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
        
            user = row[1]
            solar = float(row[2])

            if solar <= 0.1:
                continue

            if user not in maxs:
                maxs[user] = 0.0

            if solar > maxs[user]:
                maxs[user] = solar

with open('max.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['user','max'])
    for user in maxs:
        writer.writerow([user]+[maxs[user]])
