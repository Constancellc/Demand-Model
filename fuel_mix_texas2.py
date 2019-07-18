import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import copy

stem = '../Documents/simulation_results/NHTS/national/'
def interpolate(f):
    f2 = []
    for i in range(23):
        f2.append(f[i])
        f2.append((f[i]+f[i+1])/2)
    f2.append(f[23])
    f2.append((f[23]+f[0])/2)
    return f2


def fill(p,new):
    p_ = copy.deepcopy(p)
    while new > 0:
        lwst = np.argmin(p_)
        p_[lwst] += 0.01
        new -= 0.01

    return p_

def getHighest(month):
    hi = [0]*24
    profiles = {}
    with open('../Documents/elec_demand/Native_Load_2018.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            m = str(int(row[0][:2]))
            if m != month:
                continue
            d = int(row[0][3:5])
            h = int(row[0][11:13])-1

            if d not in profiles:
                profiles[d] = [0]*24

            profiles[d][h] = float(row[-1].replace(',',''))/1000
    for d in profiles:
        if sum(profiles[d]) > sum(hi):
            hi = profiles[d]

    return interpolate(hi)

def getLowest(month):
    hi = [1e10]*24
    profiles = {}
    with open('../Documents/elec_demand/Native_Load_2018.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            m = str(int(row[0][:2]))
            if m != month:
                continue
            d = int(row[0][3:5])
            h = int(row[0][11:13])-1

            if d not in profiles:
                profiles[d] = [0]*24

            profiles[d][h] = float(row[-1].replace(',',''))/1000
    for d in profiles:
        if sum(profiles[d]) < sum(hi):
            hi = profiles[d]

    return interpolate(hi)

solar_shape = [0]
with open('pv/best_solar.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in ['5','8']:
            continue
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        if sum(p) > sum(solar_shape):
            solar_shape = p

best_wind = [0]
with open('pv/best_wind.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        if sum(p) > sum(best_wind):
            best_wind = p
        
worst_wind = [1e100]
with open('pv/worst_wind.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        if sum(p) < sum(worst_wind):
            worst_wind = p

wind_capacity = 22600
solar_capacity = 2900
flat_renewable = 980
flat_fossil = 46000
flat_nuclear = 4700

best_solar = [0]*48
worst_solar = [0]*48
wc = max(best_wind)
sc = max(solar_shape)
for t in range(48):
    worst_wind[t] = worst_wind[t]*wind_capacity/wc
    best_wind[t] = best_wind[t]*wind_capacity/wc
    best_solar[t] = solar_shape[t]*solar_capacity/sc
    worst_solar[t] = solar_shape[t]*0.2*solar_capacity/sc

def get_plot_y_values(solar,wind):
    y0 = [0]*48
    y1 = []#self.flat_renewable/1000]*48
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    for t in range(48):
        y1.append(y0[t]+solar[t]/1000)
        y2.append(y1[-1]+wind[t]/1000)
        y3.append(y2[-1]+flat_renewable/1000)
        y4.append(y3[-1]+flat_nuclear/1000)
        y5.append(y4[-1]+flat_fossil/1000)

    return [y0,y1,y2,y3,y4,y5]

def calc_fuel_mix(p,solar,wind):
    renew = []
    for t in range(48):
        renew.append((flat_renewable+solar[t]+wind[t])/1000)

    r = 0
    n = 0
    for t in range(48):
        if p[t] < renew[t]:
            r += p[t]
            continue
        else:
            r += renew[t]
            n += p[t]-renew[t]

    return round(100*r/(r+n),1)


plt.figure(figsize=(9,3.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '11'
c = ['#FFFF99','#BBCCFF','#99FF99','#FFCCCC','#BBBBBB']
l = ['Solar','Wind','Other','Nuclear','Fossil']
p = getHighest('2')
plt.subplot(1,2,2)
plt.plot(p,c='k')
plt.title('Worst Case\n'+str(calc_fuel_mix(p,worst_solar,
                                          worst_wind))+'%',y=0.6)
# get solar
solar = []
y = get_plot_y_values(worst_solar,worst_wind)
for i in range(len(y)-1):
    plt.fill_between(range(48),y[i],y[i+1],color=c[i],label=l[i])
plt.ylim(0,90) 
p = getLowest('7')
plt.legend(ncol=3)
plt.xlim(0,47)
plt.grid(ls=':')

plt.subplot(1,2,1)
plt.xlim(0,47)
plt.plot(p,c='k')
plt.title('Best Case\n'+str(calc_fuel_mix(p,best_solar,
                                          best_wind))+'%',y=0.6)
plt.ylim(0,90) 
# get solar
solar = []
y = get_plot_y_values(best_solar,best_wind)
for i in range(len(y)-1):
    plt.fill_between(range(48),y[i],y[i+1],color=c[i],label=l[i])

plt.grid(ls=':')
plt.ylabel('Power Demand (GW)')
plt.tight_layout()
plt.savefig('../Dropbox/thesis/chapter5/img/tx_fuelmix.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0)


baseH = []
dumbH = []
smartH = []
baseL = []
dumbL = []
smartL = []
fg = 'sp'


tm = ['sp','su','au','wt']
m = {'sp':'4','su':'7','au':'10','wt':'1'}
for i in range(4):
    u = [0]*288
    pH = getHighest(m[tm[i]])
    pL = getLowest(m[tm[i]])

    with open(stem+'uncontrolled_'+tm[i]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if int(row[0]) < 288:
                continue
            try:
                u[int(int(row[0])/5)] += float(row[2])/5000000
            except:
                print(row[0])

    re = copy.deepcopy(sum(u)/6)

    for t in range(288):
        u[t] = u[t]*1.12

    baseH.append(calc_fuel_mix(pL,best_solar,best_wind))
    baseL.append(calc_fuel_mix(pH,worst_solar,worst_wind))

    pH2 = copy.deepcopy(pH)
    pL2 = copy.deepcopy(pL)
    for t in range(288):
        pH2[int(t/6)] += u[t]/6
        pL2[int(t/6)] += u[t]/6

    dumbH.append(calc_fuel_mix(pL2,best_solar,best_wind))
    dumbL.append(calc_fuel_mix(pH2,worst_solar,worst_wind))

    pH3 = fill(pH,re)
    pL3 = fill(pL,re)

    smartH.append(calc_fuel_mix(pL3,best_solar,best_wind))
    smartL.append(calc_fuel_mix(pH3,worst_solar,worst_wind))
    
    
   
plt.figure(figsize=(8.5,3))
plt.subplot(1,2,1)
plt.title('Max Renewable Generation')
plt.bar(np.arange(4)-0.2,baseH,width=0.2,color='gray',label='base',zorder=2)
plt.bar(np.arange(4),dumbH,width=0.2,color='b',label='dumb',zorder=2)
plt.bar(np.arange(4)+0.2,smartH,width=0.2,color='r',label='smart',zorder=2)

plt.ylim(0,70)
plt.ylabel('Renewables Fuel Mix (%)')
plt.xticks(range(4),['Jan','Apr','Jul','Oct'])
plt.grid(ls=':',zorder=0)


plt.subplot(1,2,2)
plt.title('Min Renewable Generation')
plt.bar(np.arange(4)-0.2,baseL,width=0.2,color='gray',label='No Charging',zorder=2)
plt.bar(np.arange(4),dumbL,width=0.2,color='b',label='Uncontrolled',zorder=2)
plt.bar(np.arange(4)+0.2,smartL,width=0.2,color='r',label='Controlled',zorder=2)
plt.xticks(range(4),['Jan','Apr','Jul','Oct'],zorder=2)
plt.legend(ncol=1)
plt.ylim(0,70)
plt.grid(ls=':',zorder=0)
plt.tight_layout()
plt.savefig('../Dropbox/thesis/chapter5/img/tx_fuelmix2.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()


