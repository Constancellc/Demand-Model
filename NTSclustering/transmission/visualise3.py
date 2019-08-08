import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from mpl_toolkits.basemap import Basemap
from matplotlib import cm

import pandapower
import pandapower.networks as pn
import pandapower.plotting as pplt

net = pn.GBreducednetwork()
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=59,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
#net = pn.GBnetwork()
lines = net.line

tran = net.trafo
gen = net.gen  
buses = net.bus
lds = net.load

stor = []
ld_inc = {}
with open('substation_predictions.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        stor.append(float(row[1])/100)
        ld_inc[int(row[0])-1] = 1+(float(row[1])/100)

ld_inc2 = {}
with open('2030_substation.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        s = int(row[0])-1
        ld_inc2[s] = 1+(stor[s]*float(row[1])/100)

print(ld_inc2)
gen_bus = {}

total = 0
for i in range(29):
    total += lds.p_kw[i]
print(total)

pandapower.runopp(net)
res = net.res_line

tot = 0
for l in res.pl_kw:
    tot+= l
print(tot)


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
        phi = np.arctan((b[0]-a[0])/(b[1]-a[1]))
        phi += np.pi/2
        a_ = [a[0]+10000*np.sin(phi),a[1]+10000*np.cos(phi)]
        b_ = [b[0]+10000*np.sin(phi),b[1]+10000*np.cos(phi)]
        #a_ = [a[0]+10000,a[1]+10000]
        #b_ = [b[0]+10000,b[1]+10000]
            
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


bus_ld = {}
for i in range(len(lds)):
    lds.p_kw[i] = 1.02*lds.p_kw[i]*ld_inc[lds.bus[i]]
    lds.q_kvar[i] = 1.02*lds.q_kvar[i]*ld_inc[lds.bus[i]]
    bus = lds.bus[i]
    if bus not in bus_ld:
        bus_ld[bus] = 0
    bus_ld[bus] += lds.p_kw[i]/1000
total = 0
for i in range(29):
    total += lds.p_kw[i]
print(total)




#print(lines.max_i_ka[14])
#print(lds)
#print(net.gen.max_p_kw)
#print(net.load)
#print(net.bus)

#pplt.simple_plot(net)


loading = {}
losses = {}
for i in range(86):
    loading[i] = 0
    losses[i] = 0


tot = 0
for i in range(86):
    tot += res.pl_kw[i]
print(tot)
bad = []
for li in range(86):
    lines.in_service[li] = False

    pandapower.runopp(net)
    res = net.res_line
        
    for i in range(86):
        if int(res.loading_percent[i]) >= loading[i]:
            loading[i] = int(res.loading_percent[i])
            if loading[i] > 100:
                bad.append(i)
    lines.in_service[li] = True
print(bad)
#bad = [1, 0, 3, 2, 8, 15, 14]
'''
bad = [2,3]
bad30 = [8]
bad100 = [1,0]

pandapower.runopp(net)
for i in range(86):
    loading[i] = int(res.loading_percent[i])
    #losses[i] = 100*(float(res.p_from_kw[i])+float(res.p_to_kw[i]))/\
    #                float(res.p_from_kw[i])
#plt.figure()

'''
bus_gen = {}
tg = 0
for i in range(len(gen)):
    bus = gen_bus[i]
    if bus not in bus_gen:
        bus_gen[bus] = 0
    tg -= net.res_gen.p_kw[i]
    bus_gen[bus] -= net.res_gen.p_kw[i]/1000


    '''
for i in range(len(lineAB)):
    a = lineAB[i][0]
    b = lineAB[i][1]
    plt.plot([a[1],b[1]],[a[0],b[0]],c='gray',alpha=0.5,zorder=0)
    if i < 86:
        plt.plot([a[1],b[1]],[a[0],b[0]],c='gray',lw=loading[i]/20,alpha=0.5)
    else:
        plt.plot([a[1],b[1]],[a[0],b[0]],c='gray',ls='--',alpha=0.5)'''

#for i in bus_loc:
    #plt.scatter(bus_loc[i][1],bus_loc[i][0],color='k')
    #plt.annotate(i+1, (bus_loc[i][1],bus_loc[i][0]))
'''
for bus in bus_gen:
    plt.scatter(bus_loc[bus][1],bus_loc[bus][0],color='r',s=bus_gen[bus]/8,
                alpha=0.2)'''


fig=plt.figure(figsize=(5,8))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=59,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
m.drawcoastlines()



for i in range(len(lineAB)):
    a = lineAB[i][0]
    b = lineAB[i][1]
    if i < 86:
            #plt.plot([a[1],b[1]],[a[0],b[0]],lw=6,c='#FF9999',zorder=1)
        plt.plot([a[1],b[1]],[a[0],b[0]],lw=2,c=cm.viridis(loading[i]/100))
        
        if i in bad:
            plt.scatter([(a[1]+b[1])/2],[(a[0]+b[0])/2],marker='o',c='None',
                        edgecolor='r',s=40,zorder=3,linewidth=1)
        '''
        
        if i in bad30:
            plt.scatter([(a[1]+b[1])/2],[(a[0]+b[0])/2],marker='s',c='None',
                        edgecolor='r',s=50,zorder=3,linewidth=2)
        
        if i in bad100:
            plt.scatter([(a[1]+b[1])/2],[(a[0]+b[0])/2],marker='d',c='None',
                        edgecolor='r',s=40,zorder=3,linewidth=2)
        if i in bad2:
            plt.scatter([(a[1]+b[1])/2],[(a[0]+b[0])/2],marker='o',c='None',
                        edgecolor='b',s=30,zorder=3)
        '''
    else:
        plt.plot([a[1],b[1]],[a[0],b[0]],lw=2,c=cm.viridis(0.1))

for i in bus_loc:
    plt.scatter(bus_loc[i][1],bus_loc[i][0],color='k',zorder=3)


plt.scatter([5e5],[1.55e6],marker='o',c='None',edgecolor='r',s=30)
plt.annotate('N-1 Violation',(5.35e5,1.54e6))
plt.plot([4.7e5,8.4e5],[1.59e6,1.59e6],c='gray',lw=1)
plt.plot([4.7e5,4.7e5],[1.52e6,1.59e6],c='gray',lw=1)
plt.plot([4.7e5,8.4e5],[1.52e6,1.52e6],c='gray',lw=1)
plt.plot([8.4e5,8.4e5],[1.52e6,1.59e6],c='gray',lw=1)

top = 1450000
btm = 715000

for i in range(100):
    y1 = btm+(top-btm)*(i/100)
    y2 = btm+(top-btm)*((i+1)/100)
    plt.plot([770000,770000],[y1,y2],lw=6,c=cm.viridis(2*i/100-0.5))

tcks = ['0%','20%','40%','60%','80%','100%']
#tcks = ['<50%','60%','70%','80%','90%','100%']
for i in range(6):
    y_ = btm+(top-btm)*(i/5)-10000
    plt.annotate('- '+tcks[i],(780000,y_))
    
plt.savefig('../../../Dropbox/thesis/chapter5/img/transmission_n-1_100.pdf',
            bbox_inches='tight')
plt.show()
