import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv


stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
stem2 = '../../../Documents/census/'
data = '../../../Documents/elec_demand/MSOA_domestic_electricity_2016.csv'

data2 = '../../../Documents/elec_demand/LSOA_domestic_electricity_2016.csv'


ruType = {}
with open(stem2+'LA_rural_urban.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        ruType[row[0]] = int(row[1])


nE7 = {}
nStd = {}
msoa2la = {}
with open(data,'r+',encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        LA = row[1]
        msoa2la[row[3]] = LA
        if LA == '':
            continue
        if LA not in nE7:
            nE7[LA] = 0
            nStd[LA] = 0
            
        nE7[LA] += int(row[8])# total number of E7 meters
        nStd[LA] += int(row[7])# total number of standard standard

lsoa2la = {}
with open(data2,'r+',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        LA = row[1][1:-1]
        lsoa = row[5].replace(' ','')
        lsoa2la[lsoa] = LA

with open(stem2+'e7.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for l in nStd:
        writer.writerow([l,nE7[l]/(nStd[l]+nE7[l])])

cars = {}
with open(stem2+'cars-MSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(10):
        next(reader)
    for row in reader:
        if len(row) < 5:
            continue
        if len(row[0]) < 10:
            continue
        i = 0
        m = ''
        while row[0][i] != ' ':
            m += row[0][i]
            i += 1
        LA = msoa2la[m]
        vph = float(row[3])+2*float(row[4])+3*float(row[5])+4*float(row[6])
        vph = vph/float(row[1])
        cars[LA] = vph
nBd = {}
nP = {}
with open(stem2+'hhSize-MSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(10):
        next(reader)
    for row in reader:
        if len(row) < 1:
            continue
        if len(row[0]) < 10:
            continue
        i = 0
        m = ''
        while row[0][i] != ' ':
            m += row[0][i]
            i += 1
        LA = msoa2la[m]
        if LA not in nBd:
            nBd[LA] = [0,0]
            nP[LA] = [0,0]

        nBd[LA][0] += float(row[3])
        nP[LA][0] += float(row[1])
        nBd[LA][1] += 1
        nP[LA][1] += 1

wDist = {}
with open(stem2+'distToWork-LSOA2.csv','rU',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            la = lsoa2la[row[0]]
        except:
            continue
        if la not in wDist:
            wDist[la] = [0,0]
        wDist[la][0] += float(row[2])
        wDist[la][1] += float(row[1])
        
with open(stem2+'cars.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for la in cars:
        writer.writerow([la,cars[la]])

with open(stem2+'hhsize.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for la in nP:
        writer.writerow([la,nP[la][0]/nP[la][1]])

with open(stem2+'dist.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for la in wDist:
        writer.writerow([la,wDist[la][0]/wDist[la][1]])

def fs(x):
    return 0.6+x*0.3
def fe(x):
    return 1.6+x*0.3

rnh = {'1':64,'2':200,'3':471}
with open(stem2+'ADMD.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA Code','Max kW'])
    for la in ruType:
        a = nE7[la]/(nE7[la]+nStd[la])
        try:
            b = nBd[la][0]/nBd[la][1]
        except:
            b = 3
            
        admd = ((1-a)*fs(b)+a*fe(b))
        admd = rnh[str(ruType[la])]*admd
        writer.writerow([la,admd])
