import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

rnd = 10

# finding the locations
locations = {}

with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        
        ID = int(row[0])
        if ID not in locations:
            locations[ID] = {}

        start = int(row[3])
        end = int(row[4])

        if end < start:
            end += 24*60

        sw = int(row[6])
        ew = int(row[7])
        sh = int(row[8])
        eh = int(row[9])
            
        day = int(row[1])
        
        if day not in locations[ID]:
            locations[ID][day] = [-1]*(24*60) # -1 -> unknown
            '''
            if sw == 1:
                for i in range(0,start):
                    locations[ID][day][i] = 2 # 2 -> work
            elif sh == 1:
                for i in range(0,start):
                    locations[ID][day][i] = 0 # 0 -> home
            
            else:
                for i in range(0,start):
                    try:
                        locations[ID][day][i] = locations[ID][day-1][-1]
                    except:
                        continue
            '''
        if end < 24*60:
            for i in range(start,end):
                locations[ID][day][i] = 1 # 1 -> driving

            if ew == 1:
                locations[ID][day][end] = 2
            elif eh == 1:
                locations[ID][day][end] = 0
            else:
                locations[ID][day][end] = 3 # 3 -> unknown
        else:
            for i in range(start,24*60):
                locations[ID][day][i] = 1
            if day+1 not in locations[ID]:
                    locations[ID][day+1] = [0]*(24*60)
            for i in range(0,end-24*60):
                locations[ID][day+1][i] = 1

            if ew == 1:
                locations[ID][day+1][end-24*60] = 2
            elif eh == 1:
                locations[ID][day+1][end-24*60] = 0
            else:
                locations[ID][day+1][end-24*60] = 3 # 3 -> unknown

        

n = {} # counts the number of non-zero use days for each vehicle
highest = {} # counts the number of days recorded for each vehicle
# now forward filling
for ID in locations:
    n[ID] = len(locations[ID])
    highest[ID] = 0
    for day in locations[ID]:
        
        if day >= highest[ID]:
            highest[ID] = day
            
        profile = locations[ID][day]
        i = 0

        # first time skip to the starting point
        while profile[i] == -1:
            i += 1

        while i < 24*60-1:

            while profile[i] != -1 and i < 24*60-1:
                i += 1

            loc = profile[i-1]

            while profile[i] == -1 and i < 24*60-1:
                profile[i] = loc
                i += 1

        profile[i] = profile[i-1]

# now go back and fill in start point
for ID in locations:
    for day in locations[ID]:
        i = 0
        if locations[ID][day][i] != -1:
            continue
        
        while locations[ID][day][i] == -1:
            i += 1

        for j in range(0,i):
            try:
                locations[ID][day][j] = locations[ID][day-1][-1]
            except:
                locations[ID][day][j] = 0
            

home = [0]*(24*60)
transit = [0]*(24*60)
work = [0]*(24*60)
other = [0]*(24*60)

N = 0 # count number of idle vehicle-days
n_total = 0 # count total number of vehicle-days

for ID in locations:
    n_total += highest[ID]
    N += highest[ID]-n[ID]
    for day in locations[ID]:
        for i in range(0,24*60):
            if locations[ID][day][i] == 0:
                home[i] += 1
            elif locations[ID][day][i] == 1:
                transit[i] += 1
            elif locations[ID][day][i] == 2:
                work[i] += 1
            elif locations[ID][day][i] == 3:
                other[i] += 1
            else:
                print 'oops ',
                print locations[ID][day][i],
                print ' at ',
                print i

for i in range(0,24*60):
    home[i] += N


for i in range(0,24*60):
    home[i] = float(home[i])/n_total
    other[i] = float(other[i])/n_total
    work[i] = float(work[i])/n_total
    transit[i] = float(transit[i])/n_total

t = np.linspace(0,24,num=1440)
x = np.linspace(2,22,num=6)
my_xticks = ['02:00','06:00','10:00','14:00','18:00','22:00']

plt.figure(1)
plt.ylabel('Percentage fleet location')
plt.plot(t,home,label='home')
plt.plot(t,other,label='other')
plt.plot(t,transit,label='in transit')
plt.plot(t,work,label='work')
plt.xticks(x,my_xticks)
plt.xlim(0,24)
plt.ylim(0,1)
plt.legend()
plt.grid()
plt.xlabel
plt.show()

            

            
        
    
