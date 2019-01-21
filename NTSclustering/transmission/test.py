import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

import pandapower
import pandapower.networks as pn
import pandapower.plotting as pplt

net = pn.GBreducednetwork()
#net = pn.GBnetwork()
lines = net.line
buses = net.bus

lds = net.load
print(lds)

lds_ = {}

for l in range(29):
    bus = lds.bus[l]
    p = lds.p_kw[l]
    if bus not in lds_:
        lds_[bus] = p
    else:
        lds_[bus] += p
        
ld_buses = []
ld_buses2 = []
ld_buses3 = []
ld_buses4 = []
total = 0
for l in lds_:
    total += lds_[l]
    if lds_[l]< 100000:
        ld_buses.append(l)
    elif lds_[l] < 500000:
        ld_buses2.append(l)
    elif lds_[l]< 1000000:
        ld_buses3.append(l)
    else:
        ld_buses4.append(l)

x = []
y = []
x2 = []
y2 = []
x3 = []
y3 = []
x4 = []
y4 = []

geo = net.bus_geodata
for l in ld_buses:
    x.append(geo.x[l])
    y.append(geo.y[l])
for l in ld_buses2:
    x2.append(geo.x[l])
    y2.append(geo.y[l])
for l in ld_buses3:
    x3.append(geo.x[l])
    y3.append(geo.y[l])
for l in ld_buses4:
    x4.append(geo.x[l])
    y4.append(geo.y[l])

plt.figure()
plt.subplot(1,2,1)
plt.title('Panda Power Network')
#plt.scatter(x,y)
#plt.scatter(x2,y2)
#plt.scatter(x3,y3)
#plt.scatter(x4,y4)
plt.scatter(y+y2+y3+y4,x+x2+x3+x4)

print(len(x+x2+x3+x4))
x = []
y = []

with open('gsp.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        x.append(float(row[3]))
        y.append(float(row[4]))
print(len(x))
plt.subplot(1,2,2)
plt.title('Grid Supply Point Locations')
plt.scatter(y,x)
plt.show()

lds.p_kw[10] = 4.3

pandapower.runpp(net)


#print(lines.max_i_ka[14])
#print(lds)
#print(net.gen.max_p_kw)
#print(net.load)
#print(net.bus)
#pplt.simple_plot(net)


res = net.res_line

#print(res.loading_percent)

loading = [0]*400
m = 0
for i in range(1557):
    loading[int(res.loading_percent[i])] += 1
    if res.loading_percent[i] > m:
        m = res.loading_percent[i]

plt.figure()
plt.bar(range(400),loading)
plt.xlim(0,50)
plt.show()
