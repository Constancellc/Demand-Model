import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from mpl_toolkits.basemap import Basemap
from sklearn.linear_model import LinearRegression



import pandapower
import pandapower.networks as pn
import pandapower.plotting as pplt

net = pn.GBreducednetwork()
fig=plt.figure(figsize=(8,10))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=59,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
m.drawcoastlines()

ld_inc = {}
with open('substation_predictions.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ld_inc[int(row[0])-1] = 1+(float(row[1])/100)
    
#net = pn.GBnetwork()
lines = net.line

tran = net.trafo
gen = net.gen

gen_bus = {}

for i in range(len(gen)):
    gen_bus[i] = gen.bus[i]


bus_loc = {}

with open('substations.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        xpt,ypt = m(float(row[3]),float(row[2]))
        bus_loc[int(row[0])-1] = [ypt,xpt]
        
lineAB = {}
found = []
for i in range(len(lines)):
    a = bus_loc[int(lines.from_bus[i])]
    b = bus_loc[int(lines.to_bus[i])]
    if [a,b] in found:
        a_ = [a[0]+0.05,a[1]+10000]
        b_ = [b[0]+0.05,b[1]+10000]
            
        lineAB[i] = [a_,b_]
    else:        
        lineAB[i] = [a,b]
        found.append([a,b])
    #lineAB[i] = [int(lines.from_bus[i]),int(lines.to_bus[i])]

for i in range(len(tran)):
    a = bus_loc[int(tran.hv_bus[i])]
    b = bus_loc[int(tran.lv_bus[i])]
    lineAB[i+len(lines)] = [a,b]
    #lineAB[i+len(lines)] = [int(tran.hv_bus[i]),int(tran.lv_bus[i])]
  
buses = net.bus
lds = net.load

bus_ld = {}

for i in range(len(lds)):
    lds.p_kw[i] = lds.p_kw[i]*ld_inc[lds.bus[i]]
    lds.q_kvar[i] = lds.q_kvar[i]*ld_inc[lds.bus[i]]
    bus = lds.bus[i]
    if bus not in bus_ld:
        bus_ld[bus] = 0
    bus_ld[bus] += lds.p_kw[i]/1000
    
total = 0
for i in range(29):
    total += lds.p_kw[i]
print(total)


pandapower.runopp(net)


#print(lines.max_i_ka[14])
#print(lds)
#print(net.gen.max_p_kw)
#print(net.load)
#print(net.bus)

#pplt.simple_plot(net)


res = net.res_line


for r in res:
    print(r)

loading = {}
losses = {}
for i in range(86):
    loading[i] = int(res.loading_percent[i])
    losses[i] = 100*(float(res.p_from_kw[i])+float(res.p_to_kw[i]))/\
                float(res.p_from_kw[i])

#plt.figure()

bus_gen = {}
tg = 0
for i in range(len(gen)):
    bus = gen_bus[i]
    if bus not in bus_gen:
        bus_gen[bus] = 0
    tg -= net.res_gen.p_kw[i]
    bus_gen[bus] -= net.res_gen.p_kw[i]/1000
print(tg)


for i in range(len(lineAB)):
    a = lineAB[i][0]
    b = lineAB[i][1]
    if i < 86:
        if loading[i] > 100:
            plt.plot([a[1],b[1]],[a[0],b[0]],c='r',lw=loading[i]/20,alpha=0.5)
        else:
            plt.plot([a[1],b[1]],[a[0],b[0]],c='gray',lw=loading[i]/20,alpha=0.5)
    else:
        plt.plot([a[1],b[1]],[a[0],b[0]],c='gray',ls='--',alpha=0.5)

for i in bus_loc:
    plt.scatter(bus_loc[i][1],bus_loc[i][0],color='k')
    plt.annotate(i+1, (bus_loc[i][1],bus_loc[i][0]))

for bus in bus_gen:
    plt.scatter(bus_loc[bus][1],bus_loc[bus][0],color='r',s=bus_gen[bus]/8,
                alpha=0.2)
for bus in bus_ld:
    plt.scatter(bus_loc[bus][1],bus_loc[bus][0],color='b',s=bus_ld[bus]/8,
                alpha=0.2)    
plt.show()
