# packages
import csv
import random
import copy
import datetime
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/netrev/TC2a/'

hh = {}
header = []
with open(stem+'1minProfiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[1] != '514':
            continue
        if row[0] not in hh:
            hh[row[0]] = [0]*1440
            header.append(row[0])
        hh[row[0]][int(row[2])] = float(row[3])

with open(stem+'03-Mar-2014.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t']+header)
    for t in range(1440):
        row = [t]
        for hh_ in header:
            row += [hh[hh_][t]]
        writer.writerow(row)
    
