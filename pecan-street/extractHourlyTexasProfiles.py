import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage.filters as fil
profiles = {}
hhs = []

stem = '../../Documents/pecan-street/hourly-texas/'
files = ['27-Jun-2018','11-Jul-2018','18-Jul-2018','22-Aug-2018',
         '1-Aug-2018','8-Aug-2018','15-Aug-2018','25-Jul-2018']

profiles = {}
for f in files:
    with open(stem+f+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            hr = int(row[0][11:13])
            hh = f+row[1]

            if hh not in profiles:
                profiles[hh] = [0.0]*48

            p = float(row[3])-float(row[2])

            profiles[hh][hr*2] = p
            profiles[hh][hr*2+1] = p

with open(stem+'profiles.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for hh in profiles:
        if sum(profiles[hh]) < 1:
            continue
        p = fil.gaussian_filter1d(profiles[hh],0.5)
        writer.writerow(p)
