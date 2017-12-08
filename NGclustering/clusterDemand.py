import matplotlib.pyplot as plt
import numpy as np
import csv
import sklearn.cluster as clst
import datetime

maxDemand = 0

profiles = {}
with open('../../Documents/gridwatch.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        '''
        year = row[1][:4]
        month = row[1][5:7]
        day = int(row[1][8:10]
        '''
        
        date = row[1][:11]
        
        if date not in profiles:
            profiles[date] = [0.0]*24*12
            
        time = int(int(row[1][11:13])*12+int(row[1][14:16])/5)

        demand = int(row[2])

        if demand > maxDemand:
            maxDemand = demand

        profiles[date][time] = demand

data = []
dates = []

for date in profiles:
    skip = False

    sf = sum(profiles[date])

    for i in range(24*12):
        if profiles[date][i] == 0:
            skip = True
        #profiles[date][i] = profiles[date][i]/maxDemand
        profiles[date][i] = profiles[date][i]/sf

    if skip == False:
        data.append(profiles[date])
        dates.append(date)

K = 8
centroid, label, inertia = clst.k_means(data,K)

clusteredDates = {}

for i in range(0,len(label)):
    c = label[i]

    if c not in clusteredDates:
        clusteredDates[c] = []

    d = datetime.datetime(int(dates[i][:4]),int(dates[i][5:7]),
                          int(dates[i][8:10]))

    clusteredDates[c].append([dates[i],d.isoweekday(),d.month])

days = ['mon','tue','wed','thu','fri','sat','sun']
ms = ['jan','feb','mar','apr','may','jun',' jul','aug','sep','oct',
      'nov','dec']

plt.figure(1)

totalN = len(label)

os = {0:-0.4,1:-0.3,2:-0.2,3:-0.1,4:0,5:0.1,6:0.2,7:0.3}

clsts = {}
for i in range(12):
    clsts[i] = {}
    for j in range(7):
        clsts[i][j] = [0]*K

for c in clusteredDates:
    wd = [0]*7
    m = [0]*12

    for d in clusteredDates[c]:
        wd[d[1]-1] += 1
        m[d[2]-1] += 1

        clsts[d[2]-1][d[1]-1][c] += 1
        
    n = len(clusteredDates[c])
    '''

    print('----------')
    print('cluster '+str(c))
    print('----------')
    print('')
    for i in range(0,len(wd)):
        print(days[i]+str(int(100*wd[i]/n))+'% ',end=' ')
    print('')
    print('months')
    for i in range(0,len(m)):
        print(ms[i]+str(int(100*m[i]/n))+'% ',end='')
    print('')
    '''

    for i in range(0,len(wd)):
        wd[i] = wd[i]/n
    for i in range(0,len(m)):
        m[i] = m[i]/n


    plt.subplot(2,4,c+1)
    plt.pie(wd,center=[0.5,0.5],radius=0.55,labels=days)
    plt.pie(m,center=[1.9,0.5],radius=0.55,labels=ms)
    plt.title('cluster '+str(c)+': '+str(int(100*len(clusteredDates[c])/totalN))+'% points',
              x=0.2)

plt.figure(2)
for i in range(len(clusteredDates)):
    if len(clusteredDates[i]) == 1:
        print(clusteredDates[i])
    plt.plot(centroid[i],label=str(i))
plt.legend()


for m in range(12):
    with open('results/'+ms[m]+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['cluster']+days)
        for c in range(K):
            x = [0]*7
            for d in range(7):
                x[d] = clsts[m][d][c]
            writer.writerow([c]+x)
plt.show()

'''
k_values = [6,8,10,12,14,16]

plt.figure(1)
for j in range(0,6):
    plt.subplot(2,3,1+j)
    centroid, label, inertia = clst.k_means(data,k_values[j])

    for i in range(0,k_values[j]):
        plt.plot(centroid[i])
    plt.title('k='+str(k_values[j]))
    
plt.show()
'''
