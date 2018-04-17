import csv
import matplotlib.pyplot as plt
import numpy as np

#day = '7' # day of week
#month = '7' # month

def getLocations(day,month,normalise=True,smooth=False):
    locations = {}

    nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}

    with open('../../Documents/UKDA-5340-tab/constance-trips.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[7] != month:
                continue

            vehicle = row[2]

            if vehicle not in locations:
                locations[vehicle] = [0]*(48*60)

            if row[6] != day:
                continue
           
            
            purposeFrom = row[12]
            purposeTo = row[13]

            try:
                tripStart = int(row[9])
                tripEnd = int(row[10])
            except:
                continue

            for i in range(tripStart,tripEnd):
                locations[vehicle][i] = 1
                

            if purposeTo == '1': # work
                location = 2
            elif purposeTo == '23': # home
                location = 3
            elif purposeTo == '4' or purposeTo == '5': # shops
                location = 4
            else:
                location = 4+int(purposeTo) # other

            locations[vehicle][tripEnd] = location



    # now get the next day info
    
    with open('../../Documents/UKDA-5340-tab/constance-trips.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[7] != month:
                continue

            vehicle = row[2]

            if row[6] != nextDay[day]:
                continue
            
            purposeTo = row[13]

            try:
                tripStart = int(row[9])
                tripEnd = int(row[10])
            except:
                continue

            if purposeTo == '1': # work
                location = 2
            elif purposeTo == '23': # home
                location = 3
            elif purposeTo == '4' or purposeTo == '5': # shops
                location = 4
            else:
                location = 4+int(purposeTo) # other

            try:
                tripStart = int(row[8])+24*60
                tripEnd = int(row[9])+24*60
            except:
                continue

            if tripEnd < 48*60:
                for i in range(tripStart,tripEnd):
                    locations[vehicle][i] = 1

                locations[vehicle][tripEnd] = location
                
            else:
                for i in range(tripStart,48*60):
                    locations[vehicle][i] = 1
                    
    # now forward fill locations

    for vehicle in locations:
        i = 0
        
        # first assume the vehicle starts from home
        while locations[vehicle][i] == 0:
            locations[vehicle][i] = 3
            i += 1
            if i == 48*60:
                break

        while i < 48*60:
            l = locations[vehicle][i]

            if l == 1:
                while locations[vehicle][i] == 1:
                    i += 1
                    if i == 48*60:
                        break
            else:
                i += 1
                if i == 48*60:
                        break

                while locations[vehicle][i] == 0:
                    locations[vehicle][i] = l
                    i += 1
                    if i == 48*60:
                        break

            
    home = [0]*(48*60)
    transit = [0]*(48*60)
    work = [0]*(48*60)
    shops = [0]*(48*60)
    other = [0]*(48*60)

    totals = {3:home,1:transit,2:work,4:shops,5:other}
    others = {}

    for vehicle in locations:
        for i in range(0,48*60):
            j = locations[vehicle][i]
            if j > 4:
                if j not in others:
                    others[j] = [0]*(48*60)
                others[j][i] += 1
                j = 5
            totals[j][i] += 1

    # but I also want to combine some of the vectors in other
    # 10, 12 personal business medical + other
    # 11, 13 eating out
    # 21 - 25 escort

    for i in range(0,48*60):
        others[10][i] += others[12][i]
        others[11][i] += others[13][i]
        others[21][i] += others[22][i] + others[23][i] + others[24][i] +\
                         others[25][i] + others[26][i]

    del others[12]
    del others[13]
    del others[22]
    del others[23]
    del others[24]
    del others[25]
    del others[26]

    # normalising for fleet size
    if normalise == True:
        fleetSize = len(locations)

        for vector in others:
            for i in range(0,48*60):
                if totals[4][i] == 0:
                    others[vector][i] = 0
                else:
                    others[vector][i] = float(others[vector][i])/totals[5][i]



        for vector in totals:
            for i in range(0,48*60):
                totals[vector][i] = float(totals[vector][i])*100/fleetSize



    if smooth == True:
        newTotals = {}
        #i = 1
        for vector in totals:
            newVector = [0]*(48*2)
            for j in range(0,48*2):
                newVector[j] = sum(totals[vector][j*30:j*30+30])/30
            newTotals[vector] = newVector
            #i += 1

        totals = newTotals

        newOthers = {}
        for key in others:
            newVector = [0]*(48*2)
            for j in range(0,48*2):
                newVector[j] = sum(others[key][j*30:j*30+30])/30
            newOthers[key] = newVector

        others = newOthers
            
    # I don't want stupid flat lines on my graph

    toDel = []

    for vector in others:
        if max(others[vector]) < 0.1:
            toDel.append(vector)

    for vector in toDel:
        del others[vector]

    # un-normalising others, not entirely sure hwat the point of this was

    for i in range(0,48*2):
        for key in others:
            others[key][i] = others[key][i]*totals[5][i]
        
        
    return totals, others

run = getLocations('3','5',smooth=True)
totals = run[0]
others = run[1]

t = np.linspace(0,48,num=len(totals[1]))
labels = {3:'Home',1:'in transit',2:'Work',4:'Shops',5:'other'}
styles = {1:'-',2:'--',3:'-',4:'-.',5:':'}
plt.figure(figsize=(4,2.2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 8
#plt.subplot(1,2,1)
for line in [3,2,4]:#totals:
    if line == 1:
        continue
    elif line == 5:
        continue
    #if line == 3:
        #plt.plot(t,totals[line],label=labels[line],lw=2)
    else:
        plt.plot(t,totals[line],label=labels[line],ls=styles[line])
plt.ylabel('Percentage of Vehicles')
#plt.title('Vehicle Location')

# and x axis
x = np.linspace(26,46,num=6)
my_xticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
plt.xticks(x, my_xticks)
plt.xlim(24,48)
plt.ylim(0,100)
plt.xlabel('Time')
plt.legend(loc='upper center')
plt.grid()

plt.tight_layout()
plt.savefig('../../Dropbox/papers/smart-charging/locations.eps', format='eps', dpi=1000)

'''
plt.subplot(1,2,2)
t2 = np.linspace(0,48,num=len(others[6]))
labels2 = {6:'Work trip',7:'Education',8:'Shopping',10:'Personal business',11:'Eat out',14:'Visit friends',15:'social',16:'entertainment',17:'sport',18:'holiday',19:'day trip',20:'other',21:'escort',}
for line in others:
    plt.plot(t2,others[line],label=labels2[line])
plt.xticks(x, my_xticks)
plt.xlabel('time')
plt.xlim(24,48)
plt.legend(loc='upper center',ncol=3)
plt.grid()
plt.title('Top Contributers to "other"')
       
# now looking at variation with day of the week
days = {'7':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday',
        '4':'Friday','5':'Saturday','6':'Sunday'}

plt.figure(2)
for day in days:
    if day == '7':
        i = 1
    else:
        i = int(day)+1
    plt.subplot(2,4,i)
    run = getLocations(day,'5',smooth=True)
    totals = run[0]
    for line in totals:
        plt.plot(t,totals[line],label=labels[line])
        plt.xticks(x, my_xticks)
        plt.xlim(24,48)
    plt.title(days[day])
    plt.grid()
    if day == '7':
        plt.legend(loc=[3.8,-.8])
'''
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

'''
plt.show()
