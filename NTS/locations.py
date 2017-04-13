import csv
import matplotlib.pyplot as plt
import numpy as np

#day = '7' # day of week
#month = '7' # month

def getLocations(day,month,normalise=True):
    locations = {}

    with open('../../Documents/UKDA-5340-tab/csv/tripsUseful.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            if row[5] != day:
                continue
            if row[6] != month:
                continue

            vehicle = row[2]
            purposeFrom = row[11]
            purposeTo = row[12]

            if vehicle not in locations:
                locations[vehicle] = [0]*(24*60)

            try:
                tripStart = int(row[8])
                tripEnd = int(row[9])
            except:
                continue

            if tripEnd < 24*60:
                for i in range(tripStart,tripEnd):
                    locations[vehicle][i] = 1
            else:
                tripEnd -= 24*60
                for i in range(tripStart,24*60):
                    locations[vehicle][i] = 1
                for i in range(0,tripEnd):
                    locations[vehicle][i] = 1
                

            if purposeTo == '1': # work
                location = 2
            elif purposeTo == '23': # home
                location = 3
            else: # other
                location = 4

            locations[vehicle][tripEnd] = location

    # now forward fill locations

    for vehicle in locations:
        i = 0
        
        # first assume the vehicle starts from home
        while locations[vehicle][i] == 0:
            locations[vehicle][i] = 3
            i += 1
            if i == 24*60:
                break

        while i < 24*60:
            l = locations[vehicle][i]

            if l == 1:
                while locations[vehicle][i] == 1:
                    i += 1
                    if i == 24*60:
                        break
            else:
                i += 1
                if i == 24*60:
                        break

                while locations[vehicle][i] == 0:
                    locations[vehicle][i] = l
                    i += 1
                    if i == 24*60:
                        break

            
    home = [0]*(24*60)
    transit = [0]*(24*60)
    work = [0]*(24*60)
    other = [0]*(24*60)

    totals = {3:home,1:transit,2:work,4:other}

    for vehicle in locations:
        for i in range(0,24*60):
            totals[locations[vehicle][i]][i] += 1

    # normalising for fleet size
    if normalise == True:
        fleetSize = len(locations)

        for vector in totals:
            for i in range(0,24*60):
                totals[vector][i] = float(totals[vector][i])/fleetSize

    return totals

totals = getLocations('3','5')

t = np.linspace(0,24,num=24*60)
labels = {3:'home',1:'in transit',2:'work',4:'other'}
plt.figure(1)
for line in totals:
    plt.plot(t,totals[line],label=labels[line])
plt.ylabel('percentage of vehicles')

# and x axis
x = np.linspace(3,21,num=4)
my_xticks = ['03:00','09:00','15:00','21:00']
plt.xticks(x, my_xticks)
plt.xlabel('time')
plt.xlim(0,24)
plt.legend(loc='upper center')
'''        
# now looking at variation with day of the week
days = {'1':'Monday','2':'Tuesday','3':'Wednesday','4':'Thursday',
        '5':'Friday','6':'Saturday','7':'Sunday'}

plt.figure(2)
for day in days:
    plt.subplot(2,4,int(day))
    totals= getLocations(day,'2')
    for line in totals:
        plt.plot(t,totals[line],label=labels[line])
        plt.xticks(x, my_xticks)
    plt.title(days[day])
    if day == '1':
        plt.legend(loc=[3.8,-.8])
'''
# now looking at monthly variation
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
          '6':'June','7':'July','8':'August','9':'September',
          '10':'October','11':'November','12':'December'}

plt.figure(2)
for month in months:
    plt.subplot(3,4,int(month))
    totals = getLocations('3',month)
    for line in totals:
        plt.plot(t,totals[line],label=labels[line])
        plt.xticks(x, my_xticks)
    plt.title(months[month],y=0.8)
    plt.grid()
    if month == '1':
        plt.legend(loc=[1.1,-2.8],ncol=4)    
plt.show()
