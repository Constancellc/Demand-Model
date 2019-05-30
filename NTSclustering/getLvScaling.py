import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

nH = 200

vData = '../../Documents/My_Electric_Avenue_Technical_Data/constance/'+\
        'ST1charges/'
hData = '../../Documents/netrev/TC2a/03-Dec-2013.csv'
stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA/'

_hh = ['10032', '10228', '10163', '10009', '10249', '10064', '90035', '10220',
       '10265', '10184', '10008', '10083', '25163', '10146', '25174', '25265',
       '832', '45596', '10015', '10263', '10218', '10011', '10059', '10164',
       '10203', '10252', '10088', '10157', '10117', '10026', '10073', '10114',
       '10121', '10225', '10223', '10165', '10193', '10047', '10268', '10251',
       '10154', '10003', '10238', '10224', '10002', '10197', '10129', '10087',
       '10048', '10102', '10179', '10013', '10215', '10161', '10109', '10167',
       '10010', '10081', '10076', '10033', '10229', '10135', '10232', '10266',
       '10206', '10260', '10255', '10092', '10205', '10084', '10241', '10198',
       '10070', '10069', '10106', '10221', '10226', '10098', '10044', '10101',
       '10128', '10055', '10258', '10017', '10004', '10217', '10125', '10041',
       '10188', '10144', '10078', '10162', '10115', '10186', '10256', '10054',
       '10139', '10152', '10131']

_v = ['000','001','002','003','004','005','006','007','009','010','011','012',
      '013','014','018','019','020','021','022','023','027','028','029','030',
      '031','032','034','035','036','037','038','039','041','042','043','044',
      '045','046','047','048','049','050','052','053','054','055','056','057',
      '058','059','060','061','062','063','064','065','066','067','068','069',
      '070','071','072','073','074','075','076','077','078','079','080','081',
      '082','083','084','085','086','087','090','091','092','093','094','096',
      '097','098','099','100','101','102','103','104','105','106','107','108',
      '110','111','112','113','114']


days = []
for day in range(253):
    if day%7 not in [2,3]:
        days.append(day)

profiles = {}
for hh in _hh:
    profiles[hh] = []


with open(hData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(len(row)-1):
            profiles[_hh[i]].append(float(row[i+1]))


vProfiles = {}
for v in _v:
    for d in days:
        vProfiles[v+'-'+str(d)] = [0]*1440
    with open(vData+v+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            d = int(row[0])
            if d not in days:
                continue
            kWh = float(row[3])
            start = int(row[1])

            time_req = int(kWh*60/3.5)+1

            for t in range(start,start+time_req):
                if t < 1440:
                    vProfiles[v+'-'+str(d)][t] = 3.5
                else:
                    vProfiles[v+'-'+str(d)][t-1440] = 3.5
                  
total = [] # without EVs
total2 = [] # with EVs
for mc in range(1000):
    p = [0.0]*1440
    for n in range(nH):
        h = _hh[int(random.random()*len(_hh))]
        for t in range(1440):
            p[t] += profiles[h][t]
    total.append([sum(p)]+p)
    for n in range(nH):
        v = _v[int(random.random()*len(_v))]
        d = days[int(random.random()*len(days))]
        for t in range(1440):
            p[t] += vProfiles[v+'-'+str(d)][t]
    total2.append([sum(p)]+p)
    
total = sorted(total)
total2 = sorted(total2)
plt.figure()
plt.plot(total[500][1:])
plt.plot(total2[500][1:])
plt.show()

# get current ADMD
def admd(p):
    p2 = [0]*48
    for t in range(1440):
        p2[int(t/30)] += p[t]/30
    return max(p2)/200

f1 = admd(total[50][1:])
f2 = admd(total2[50][1:])

# now get the la specific admd
old = {}
new = {}
with open(stem+'peaks.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        old[row[0]] = float(row[1])
        new[row[0]] = float(row[2])

with open(stem+'lvScaling.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA Code','HH Scale','V Scale'])
    for la in old:
        hs = old[la]/f1
        vs = (new[la]-old[la])/(f2-f1)
        writer.writerow([la,hs,vs])
