import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

ss = {}
with open('substations.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        ss[row[0]] = [float(row[2]),float(row[3])]

def get_nearest(l):
    mind = 1e10
    best = None
    for s in ss:
        d = np.power(ss[s][0]-l[0],2)+np.power(ss[s][1]-l[1],2)
        if d < mind:
            mind = d
            best = s
    return best

_2030 = {}
c = {}

with open('2030.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        lat = ''
        i = 1
        while row[0][i] != ',':
            lat += row[0][i]
            i += 1
        lon = ''
        i += 2
        while row[0][i] != ']':
            lon += row[0][i]
            i += 1
        l = [float(lat),float(lon)]
        b = get_nearest(l)
        print(b)
    
