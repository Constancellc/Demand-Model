import csv
import matplotlib.pyplot as plt
import numpy as np

distances = {'US':[0]*400,'UK':[0]*400}
tripsPerDay = {'US':[0]*40,'UK':[0]*40}

trips = {}
# first US data
with open('../../Documents/NHTS/DAYV2PUB.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        if row[-3] not in ['01','02','03','04','05','06']:
            continue
        dis = int(float(row[-16]))
        
        try:
            distances['US'][dis] += 1
        except:
            continue
        
        household = row[0]

        if household not in trips:
            trips[household] = 0

        trips[household] += 1

for hh in trips:
    try:
        tripsPerDay['US'][trips[hh]] += 1
    except:
        continue
    
trips = {}
with open('../../Documents/UKDA-5340-tab/tab/tripeul2015.tab','rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:

        if row[16] != '5':
            continue
        hhID = row[4]
        day = row[7]

        key = hhID + day
        if key not in trips:
            trips[key] = 0

        trips[key] += 1

        dis = int(float(row[38]))

        try:
            distances['UK'][dis] += 1
        except:
            continue
        
for hh in trips:
    try:
        tripsPerDay['UK'][trips[hh]] += 1
    except:
        continue

distances['US'] = distances['US'][:300]
distances['UK'] = distances['UK'][:300]

# now normalising
for metric in [tripsPerDay, distances]:
    for nation in metric:
        S = sum(metric[nation])
        for i in range(0,len(metric[nation])):
            metric[nation][i] = metric[nation][i]/S

plt.figure(1)
plt.subplot(2,1,1)
plt.bar(np.arange(0,300),distances['US'],width=0.45,label='US')
plt.bar(np.arange(0,300)+0.5,distances['UK'],width=0.45,label='UK')
plt.xlim(-1,40)
plt.xlabel('miles')
plt.legend()
plt.title('distances',y=0.85)

plt.subplot(2,1,2)
plt.bar(np.arange(0,40),tripsPerDay['US'],width=0.45,label='US')
plt.bar(np.arange(0,40)+0.5,tripsPerDay['UK'],width=0.45,label='UK')
plt.title('trips per day',y=0.85)
plt.xlim(0,30)

plt.show()
