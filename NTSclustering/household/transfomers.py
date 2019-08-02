import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = '../../../Documents/transformers.csv'
data2 = '../../../Documents/postcodes.csv'
stem = '../../../Documents/census/'

pd = {}
with open(stem+'lsoa_population_density.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(5):
        next(reader)
    for row in reader:
        lsoa = row[0]
        _pd = int(row[4].replace(',',''))
        pd[lsoa] = _pd


# 400 = super rural
# 4000 = super urban
p2l = {}
with open(stem+'postcode2census.csv','rU',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        pc = row[1].replace(' ','')
        lsoa = row[7]
        p2l[pc] = lsoa
        
pc = {}
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        pc[row[0][:-3]] = row[1].replace(' ','')
        pc[row[4][:-3]] = row[5].replace(' ','')
        pc[row[8][:-3]] = row[9].replace(' ','')
        pc[row[12][:-3]] = row[13].replace(' ','')

sizes = [100,200,300,315,400,500,750,800]
ri = {100:0,200:1,300:2,315:3,400:4,500:5,750:6,800:7}
nCust = {0:{},1:{},2:{}}

c64 = {0:[0]*8,1:[0]*8,2:[0]*8}
c200 = {0:[0]*8,1:[0]*8,2:[0]*8}
c471 = {0:[0]*8,1:[0]*8,2:[0]*8}
for s in sizes:
    for i in range(3):
        nCust[i][s] = [0]*80
tt = 0
with open(data,'rU',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(4):
        next(reader)
    for row in reader:
        try:
            name = row[31]
            n = int(row[32])
            rating = float(row[33])
            nrn = row[61].replace('_',' ')[:-3]
        except:
            continue
        tt += 1
        if n > 20:
            if nrn not in pc:
                continue
            if pc[nrn] not in p2l:
                continue
            p = pd[p2l[pc[nrn]]]
            if p < 400:
                t = 0
            elif p > 4000:
                t = 2
            else:
                t = 1
            if rating in sizes:
                nCust[t][rating][int(n/10)] += 1
            else:
                continue
            if n > 150 and n < 250:
                c200[0][ri[rating]] += 1
            if n > 50 and n < 80:
                c64[0][ri[rating]] += 1
            if n > 400 and n < 600:
                c471[0][ri[rating]] += 1
            '''
            print(rating/n)
            try:
                print(pc[nrn])
                print(' ')
            except:
                print(' ')
            '''
print(tt)
for k in [c64,c200,c471]:
    c = k[0]
    s = sum(c)/100
    for i in range(len(c)):
        c[i] = c[i]/s
s = range(len(sizes))
plt.figure(figsize=(8,5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 11
plt.subplot(3,1,1)
plt.bar(sizes,c200[0],width=10)
plt.xticks(sizes,sizes,rotation=90)
plt.grid(ls=':')
plt.ylabel('Networks (%)')
plt.title('50-80',y=0.65)
plt.xlim(90,810)
plt.ylim(0,70)
plt.subplot(3,1,2)
plt.bar(sizes,c64[0],width=10)
plt.grid(ls=':')
plt.ylabel('Networks (%)')
plt.title('150-250',y=0.65)
plt.xlim(90,810)
plt.ylim(0,70)
plt.xticks(sizes,sizes,rotation=90)
plt.subplot(3,1,3)
plt.bar(sizes,c471[0],width=10)
plt.xticks(sizes,sizes,rotation=90)
plt.grid(ls=':')
plt.ylabel('Networks (%)')
plt.title('400-600',y=0.65)
plt.xlim(90,810)
plt.ylim(0,70)

plt.xlabel('Transformer Rating (kVA)')
plt.tight_layout()
plt.savefig('../../../Dropbox/thesis/appendix1/img/transformers.eps',
            format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()
plt.figure()
for i in range(8):
    plt.subplot(4,2,i+1)
    plt.xticks()
    plt.title(str(sizes[i])+' kVA',y=0.6)
    for j in range(3):
        plt.plot(np.arange(0,800,10),nCust[j][sizes[i]])
    plt.grid(ls=':')
    plt.xlim(0,500)
    if i >= 6:
        plt.xlabel('No. Customers')
plt.tight_layout()
plt.show()
                           
