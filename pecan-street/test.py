import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

day0 = datetime.datetime(2018,7,4)
profiles = {}
hhs = []
with open('../../Documents/pecan-street/1min-texas/4-jul-18.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hh = row[1]
        if hh not in hhs:
            hhs.append(hh)
            profiles[hh] = [0]*1440
            
        p = float(row[3])-float(row[2])
        t = int((datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                   int(row[0][8:10]),int(row[0][11:13]),
                                   int(row[0][14:16]))-day0).seconds/60)
        profiles[hh][t] = p

print(len(hhs))

with open('../../Documents/pecan-street/1min-texas/profiles.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for hh in hhs:
        writer.writerow(profiles[hh])
