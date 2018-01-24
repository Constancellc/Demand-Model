import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

#hh = '30099'
hh = []
base = '../../Documents/netrev/constance/EVcustomers10minData.csv'
starts = '../../Documents/netrev/constance/EVcustomerStartDates.csv'
goodIDs = '../../Documents/netrev/constance/good_ids.csv'

with open(goodIDs,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[1] != 'x':
            hh.append(row[0])

profiles = {}
with open(base,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locID = row[0]
        #if locID != hh:
        if locID not in hh:
            continue

        if locID not in profiles:
            profiles[locID] = {}

        dayNo = int(row[1])

        if dayNo not in profiles[locID]:
            profiles[locID][dayNo] = {}
            
        typ = row[2]

        profile = []
        for i in range(0,144):
            profile.append(float(row[3+i]))
            
        profiles[locID][dayNo][typ] = profile


ev_charging = []
hh_demand = []

for loc in hh:

    for day in profiles[loc]:
        if sum(profiles[loc][day]['Charge point']) == 0:
            continue

        ev_charging.append([loc,day]+profiles[loc][day]['Charge point'])

        without_ev = [loc,day]
        for j in range(144):
            without_ev.append(profiles[loc][day]['House data'][j]-\
                              profiles[loc][day]['Charge point'][j])

        hh_demand.append(without_ev)

times = []
for t in range(144):
    times.append(str(t*10))

with open('../../Documents/netrev/constance/charging_hh_profiles/hh.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['loc','day']+times)
    for row in hh_demand:
        writer.writerow(row)
        
with open('../../Documents/netrev/constance/charging_hh_profiles/ev.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['loc','day']+times)
    for row in ev_charging:
        writer.writerow(row)
