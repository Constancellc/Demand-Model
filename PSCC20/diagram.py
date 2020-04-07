import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.cluster import KMeans
import datetime

#def generate(solar,rain,temp):
dates = []
rain = []
temp = []
p = []
with open('../../Documents/solar_data_scenarios/net_profile_cleaned_40000.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        dates.append(row[0])
        dt = datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                               int(row[0][8:10]))
        wd = dt.isoweekday()
        if wd > 5:
            continue
        rain.append(float(row[1]))
        temp.append(float(row[2]))
        _p = []
        for i in range(3,len(row)):
            _p.append(float(row[i]))

        p.append(_p)

plt.figure()
plt.scatter(rain,temp,marker='x')
plt.xlabel('Rainfall (mm)')
plt.ylabel('Temperature (degrees C)')
# now normalise rain and temp
mr = sum(rain)/len(rain)
vr = 0
mt = sum(temp)/len(temp)
vt = 0
for i in range(len(rain)):
    vr += np.power(rain[i]-mr,2)/len(rain)
    vt += np.power(temp[i]-mt,2)/len(rain)

for i in range(len(rain)):
    rain[i] = (rain[i]-mr)/np.sqrt(vr)
    temp[i] = (temp[i]-mt)/np.sqrt(vt)

print(mr)
print(mt)
print(np.sqrt(vr))
print(np.sqrt(vt))
jdshfk

max_d = 0.5
test = [2,-1]
plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.subplot(1,2,1)
plt.scatter(rain,temp,marker='x')
plt.title('Weather')
plt.xlim(-1,4)
plt.ylabel('Temperature (standard derviations)')
plt.xlabel('Rainfall (standard derviations)')
plt.ylim(-2.5,2.5)
y1 = []
y2 = []
_x = np.arange(test[0]-max_d,test[0]+max_d+0.001,0.001)
for x in _x:
    y1.append(np.sqrt(max_d*max_d-np.power(x-test[0],2))+test[1])
    y2.append(-np.sqrt(max_d*max_d-np.power(x-test[0],2))+test[1])
plt.plot(_x,y1,c='r')
plt.plot(_x,y2,c='r')
plt.grid(ls=':')

plt.subplot(1,2,2)
p2 = []
for i in range(len(rain)):
    d = np.sqrt(np.power(test[0]-rain[i],2)+np.power(test[1]-temp[i],2))
    if d < max_d:
        plt.plot(p[i])
        p2.append(p[i])

plt.xlim(0,47)
plt.title('Scenarios')
plt.ylim(10000,55000)
plt.ylabel('Power (GW)')
plt.yticks([10000,20000,30000,40000,50000],['10','20','30','40','50'])
plt.xticks([7.5,23.5,39.5],['04:00','12:00','20:00'])
plt.xlabel('Time')
plt.grid(ls=':')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/PSCC-20/img/scenarios.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()

