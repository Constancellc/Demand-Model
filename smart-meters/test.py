import csv
import datetime
import matplotlib.pyplot as plt

months = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,
          'SEP':9,'OCT':10,'NOV':11,'DEC':12}

day_profiles = {}

start = datetime.datetime(2007,2,15)
nDays = 0

with open('../../Documents/sharonb/7591/csv/edrp_elec.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        anon_id = row[0]
        hh_id = row[2]

        if hh_id != '10':
            continue
        
        kwh = float(row[3])
        date = int(row[1][:2])
        month = months[row[1][2:5]]
        year = 2000+int(row[1][5:7])

        date = datetime.datetime(year,month,date)
        day = (date-start).days

        if day not in day_profiles:
            day_profiles[day] = [0.0]*48

        if day > nDays:
            nDays = day

        time = int(row[1][8:10])*2+int(row[1][11:13])

        day_profiles[day][time] = kwh

print(nDays)
heatplot = []

for i in range(0,nDays+1):
    heatplot.append([])

for date in day_profiles:
    heatplot[date] = day_profiles[date]

plt.figure(1)
plt.imshow(heatplot)
plt.show()
    
