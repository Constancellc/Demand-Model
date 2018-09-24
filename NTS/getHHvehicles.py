import csv
import random
import matplotlib.pyplot as plt

stage = '../../Documents/UKDA-7553-tab/tab/stagespecial2016_protect.tab'
households = '../../Documents/UKDA-7553-tab/tab/householdspecial2016_protect.tab'
outfile = '../../Documents/UKDA-7553-tab/constance/hh-veh.csv'
        
hh = {}
with open(households, 'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        hh[row[1]] = []
        
with open(stage,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        if row[38] in ['3','4','5']: # controversial - 5 is motorcycle
            if row[5] in hh:
                if row[7] not in hh[row[5]]:
                    hh[row[5]].append(row[7])

n = [0]*10       
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['HouseholdID','Vehicle1','Vehicle2','Vehicle3','Vehicle4',
                     'Vehicle5'])
    for h in hh:
        writer.writerow([h]+hh[h])
        try:
            n[int(len(hh[h]))] += 1
        except:
            continue

S = sum(n)/100
for i in range(10):
    n[i] = n[i]/S
plt.figure()
plt.title('Number of vehicles per household')
plt.grid()
plt.bar(range(10),n)
plt.xlim(-0.5,5.5)
plt.ylabel('%')
plt.show()
