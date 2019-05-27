import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
profiles = []
hhs = []

day0 = datetime.datetime(2018,1,1)
for d in range(1440):
    profiles.append([0.0]*430)
with open('../../Documents/pecan-street/1min-ev-370.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
            
        p = float(row[2])#row[3])-float(row[2])
        t = int((datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                   int(row[0][8:10]),int(row[0][11:13]),
                                   int(row[0][14:16]))-day0).seconds/60)


        d = int((datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                   int(row[0][8:10]),int(row[0][11:13]),
                                   int(row[0][14:16]))-day0).days)
        profiles[1439-t][d] = p

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12
plt.imshow(profiles,aspect=0.15,cmap='Blues')
plt.xticks([30,120,211,303,395],['Feb\n2018','May\n2018','Aug\n2018',
                               'Nov\n2018','Feb\n2019'])
plt.yticks([0,4*60,8*60,12*60,16*60,20*60,24*60-1],
           ['23:59','20:00','16:00','12:00','08:00','04:00','00:00'])
plt.grid(ls=':')
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/eg_pecanstreet.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
