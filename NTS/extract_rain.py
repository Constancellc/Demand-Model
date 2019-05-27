import csv
import random
import datetime

f = open('midas_raindrnl_201801-201812.txt','r')
date0 = datetime.datetime(2018,1,1)

obs = []
res = {}
for x in f:
    arr = []
    i = 0
    cell = ''
    while i < len(x) and len(arr) < 13:
        while x[i] != ',':
            cell += x[i]
            i += 1
        arr.append(cell)
        cell = ''
        i += 2

    print(arr[6])

    if arr[3] != '1':
        continue
    date = datetime.datetime(int(arr[2][:4]),int(arr[2][5:7]),
                             int(arr[2][8:10]))
    stn = arr[7]
    dn = (date-date0).days
    try:
        obs = float(arr[9])
    except:
        continue

    if stn not in res:
        res[stn] = [0.0]*365

    res[stn][dn] += obs

save = []
for stn in res:
    n = 0
    for i in range(365):
        if res[stn][i] > 0:
            n += 1
    save.append([stn,n])

with open('2018rain.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['src_id','number rainy days'])
    for row in save:
        writer.writerow(row)
        
