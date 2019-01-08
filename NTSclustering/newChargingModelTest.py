import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

charge_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

trip_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/'
# First get the pdfs for charging
pdfs = {'0':{},'1':{}}
pdfs_ = {'0':{},'1':{}}
for d in ['0','1']:
    for i in range(3):
        pdfs[d][i] = {}
        for s in range(6):
            pdfs[d][i][s] = [0]*48
    for s in range(6):
        pdfs_[d][s] = [0]*48

stm = {'0':'jointPdfW','1':'jointPdfWE'}
for d in ['0','1']:
    for i in range(3):       
        with open(stem+stm[d]+str(i+1)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            s = 0
            for row in reader:
                for t in range(48):
                    pdfs[d][i][s][t] = float(row[t])
                s += 1
                
    with open(stem+stm[d]+'_.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                pdfs_[d][s][t] = float(row[t])
            s += 1

def chargeAfterJourney(d,k,s,t):
    if random.random() < pdfs[d][k][s][t]:
        return True
    else:
        return False
        
def randomCharge(d,s,t):
    if random.random() < pdfs_[d][s][t]/30:
        return True
    else:
        return False

def normalise(x):
    s = sum(x)
    for i in range(len(x)):
        x[i] = x[i]/s
    return x
    
# Then get the NTS vehicle labels, and the household to vehicle list
MEA = {}
with open(stem+'MEAlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])
with open(stem+'MEAlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])


# How will things change for the test?
journeyLogs = {}
dType = {}
with open(trip_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        if vehicle not in journeyLogs:
            journeyLogs[vehicle] = []
            dType[vehicle] = {}

        day = int(row[1])
        start = int(row[2])
        end = int(row[3])
        dType[vehicle][day] = row[-1]

        if start > end:
            end += 1440
        kWh = float(row[-2])/1000

        journeyLogs[vehicle].append([day,start,end,kWh,dType])

def step(t,d):
    t += 1
    if t >= 1440:
        t = 0
        d += 1
    return [t,d]
    
true = [0]*48
trueWE = [0]*48
true2 = [0]*48
trueWE2 = [0]*48
# now get the MEA data
with open(charge_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        #soc = float(row[4])
        start = int(row[2])
        end = int(row[3])
        if row[-1] == '0':
            true[int(start/30)] += 1
            for t in range(start,end):
                try:
                    true2[int(t/30)] += 1
                except:
                    true2[int(t/30)-48] += 1
        else:
            trueWE[int(start/30)] += 1
            for t in range(start,end):
                try:
                    trueWE2[int(t/30)] += 1
                except:
                    trueWE2[int(t/30)-48] += 1

dumb = [0]*48
dumbWE = [0]*48
dumb2 = [0]*48
dumbWE2 = [0]*48

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'

new_total = []
newWE_total = []
new_total2 = []
newWE_total2 = []
for i in range(1):
    new = [0]*48
    newWE = [0]*48
    new2 = [0]*48
    newWE2 = [0]*48

    rand = 0
    afte = 0
    for vehicle in journeyLogs:
        jLog = sorted(journeyLogs[vehicle])
        d = jLog[0][0]
        t = jLog[0][1]
        j = 0
        SOC = 0.99
        capacity = 30
        startCharge = False

        while d < jLog[-1][0]:
            if vehicle == '':
                print([d,t])
                print(jLog[j][0:2])
                print('')
            startCharge = False
            while (t < jLog[j][1] or d < jLog[j][0]) and startCharge == False:
                [t,d] = step(t,d)
                try:
                    startCharge = randomCharge(dType[vehicle][d],int(SOC*6),
                                               int(t/30))
                except:
                    startCharge = False
                if startCharge == True:
                    rand += 1

            if t == jLog[j][1] and d == jLog[j][0]:
                SOC -= jLog[j][2]/capacity
                if SOC < 0:
                    SOC = 0
                t = jLog[j][2]
                if t >= 1440:
                    t -= 1440
                    d += 1
                j += 1

                try:
                    k = MEA[vehicle+str(int(t/1440)+1)] # check - days in 0?!
                except:
                    k = int(random.random()*3) # hack
                try:
                    dt = dType[vehicle][day]
                except:
                    dt = '0'

                startCharge = chargeAfterJourney(dt,k,int(SOC*6),int(t/30))
                if startCharge == True:
                    afte += 1

            if startCharge == True:
                try:
                    dt = dType[vehicle][day]
                except:
                    dt = '0'
                if dt == '0':
                    new[int(t/30)] += 1
                    t2 = t
                    while SOC <= 0.99:
                        new2[int(t2/30)] += 1
                        SOC += 3.5/(60*capacity)
                        t2 += 1
                        if t2 == 1440:
                            t2 = 0
                else:
                    newWE[int(t/30)] += 1
                    t2 = t
                    while SOC <= 0.99:
                        newWE2[int(t2/30)] += 1
                        SOC += 3.5/(60*capacity)
                        t2 += 1
                        if t2 == 1440:
                            t2 = 0
                SOC = 0.99
                startCharge = False

            if j == len(jLog)-1:
                d = jLog[-1][0]

            if t >= jLog[j][1] and d >= jLog[j][0]:
                j += 1

    print(100*afte/(afte+rand))
    new_total.append(normalise(new))
    newWE_total.append(normalise(newWE))
    new_total2.append(normalise(new2))
    newWE_total2.append(normalise(newWE2))


m = [0]*48
mW = [0]*48
l = [1]*48
lW = [1]*48
u = [0]*48
uW = [0]*48
for t in range(48):
    for x in range(len(new_total)):
        m[t] += new_total[x][t]/len(new_total)
        mW[t] += newWE_total[x][t]/len(new_total)
        if new_total[x][t] < l[t]:
            l[t] = new_total[x][t]
        if new_total[x][t] > u[t]:
            u[t] = new_total[x][t]
        if newWE_total[x][t] < lW[t]:
            lW[t] = newWE_total[x][t]
        if newWE_total[x][t] > uW[t]:
            uW[t] = newWE_total[x][t]
m2 = [0]*48
mW2 = [0]*48

for t in range(48):
    for x in range(len(new_total2)):
        m2[t] += new_total2[x][t]/len(new_total2)
        mW2[t] += newWE_total2[x][t]/len(new_total2)




plt.subplot(2,1,1)
plt.plot(m,c='r',label='(b)')
#plt.fill_between(range(48),l,u,color='r',alpha=0.2)
plt.subplot(2,1,2)
plt.plot(mW,c='r',label='(b)')
#plt.fill_between(range(48),lW,uW,color='r',alpha=0.2)

# now dumb charging
for vehicle in journeyLogs:
    jLog = sorted(journeyLogs[vehicle])
    j = 0
    kWh = 0
    while j < len(jLog)-1:
        kWh += jLog[j][2]
        if jLog[j][0] != jLog[j+1][0]:
            if kWh > 30:
                kWh = 30
            t = jLog[j][1]
            t_req = int(kWh*60/3.5)
            if dType[vehicle][jLog[j][0]] == '0':
                dumb[int(jLog[j][1]/30)] += 1
                for t2 in range(t_req):
                    try:
                        dumb2[int((t+t2)/30)] += 1
                    except:
                        dumb2[int((t+t2-1440)/30)] += 1
            else:
                dumbWE[int(jLog[j][1]/30)] += 1
                for t2 in range(t_req):
                    try:
                        dumbWE2[int((t+t2)/30)] += 1
                    except:
                        dumbWE2[int((t+t2-1440)/30)] += 1
        j += 1

dumb = normalise(dumb)
true = normalise(true)
dumb2 = normalise(dumb2)
true2 = normalise(true2)
plt.subplot(2,1,1)
plt.plot(dumb,c='b',label='(a)')
plt.plot(true,ls='--',c='k',label='True')
plt.xlim(0,47)
plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Likelihood of starting charge')
plt.title('Weekday')
plt.legend()

dumbWE = normalise(dumbWE)
trueWE = normalise(trueWE)
dumbWE2 = normalise(dumbWE2)
trueWE2 = normalise(trueWE2)

plt.subplot(2,1,2)
plt.plot(dumbWE,c='b',label='(a)')
plt.plot(trueWE,ls='--',c='k',label='True')
plt.xlim(0,47)
plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Likelihood of starting charge')
plt.title('Weekend')
plt.tight_layout()

with open(outstem+'error.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['true','dumb','new','trueW','dumbW','newW'])
    for t in range(48):
        writer.writerow([true[t],dumb[t],m[t],trueWE[t],dumbWE[t],mW[t]])



with open(outstem+'error2.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['true','dumb','new','trueW','dumbW','newW'])
    for t in range(48):
        writer.writerow([true2[t],dumb2[t],m2[t],trueWE2[t],dumbWE2[t],mW2[t]])


plt.show()
