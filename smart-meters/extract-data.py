import csv
import datetime
import matplotlib.pyplot as plt

months = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,
          'SEP':9,'OCT':10,'NOV':11,'DEC':12}

outfile = '../../Documents/sharonb/7591/csv/profiles.csv'
day_profiles = {}

start = datetime.datetime(2007,1,1)
minDay = {}
#maxDay = {}

with open('../../Documents/sharonb/7591/csv/edrp_elec.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hh_id = row[0]

        if hh_id not in day_profiles:
            day_profiles[hh_id] = {}
            minDay[hh_id] = 10000
            #maxDay[hh_id] = 0
        
        kwh = float(row[3])
        date = int(row[1][:2])
        month = months[row[1][2:5]]
        year = 2000+int(row[1][5:7])

        date = datetime.datetime(year,month,date)
            
        day = (date-start).days

        if day < minDay[hh_id]:
            minDay[hh_id] = day
            '''
        if day > maxDay[hh_id]:
            maxDay[hh_id] = day
            '''
        if day not in day_profiles[hh_id]:
            day_profiles[hh_id][day] = [0.0]*48

        time = int(row[2])

        day_profiles[hh_id][day][time] = kwh

times = []
for i in range(0,48):
    if i%2 == 0:
        times.append(str(int(i/2))+':00')
    else:
        times.append(str(int(i/2))+':30')
        
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','day']+times)
    for hh in day_profiles:
        for day in day_profiles[hh]:
            writer.writerow([hh]+[day-minDay[hh]]+day_profiles[hh][day])
'''
heatplot = []
for i in range(0,nDays+1):
    heatplot.append([])

for date in day_profiles:
    heatplot[date-minDay] = day_profiles[date]

plt.figure(1)
plt.imshow(day_profiles)
plt.show()
'''
