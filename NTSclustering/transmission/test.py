import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

import pandapower
import pandapower.networks as pn
import pandapower.plotting as pplt

#net = pn.GBreducednetwork()
net = pn.GBnetwork()
lines = net.line
buses = net.bus

lds = net.load
print(lds)

ld_buses = []
total = 0
for l in range(446):
    total += lds.p_kw[l]
    ld_buses.append(lds.bus[l])

x = []
y = []

geo = net.bus_geodata
for l in range(446):
    x.append(geo.x[ld_buses[l]])
    y.append(geo.y[ld_buses[l]])

plt.figure()
plt.scatter(x,y)
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
