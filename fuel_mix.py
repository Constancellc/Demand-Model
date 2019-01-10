# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

def getBaseLoad(day,month):

    # find right date for day of the week
    calender = {'1':{'1':11,'2':12,'3':13,'4':14,'5':15,'6':16,'7':17},
                '2':{'1':15,'2':16,'3':17,'4':18,'5':19,'6':20,'7':21},
                '3':{'1':14,'2':15,'3':16,'4':17,'5':18,'6':19,'7':20},
                '4':{'1':11,'2':12,'3':13,'4':14,'5':15,'6':16,'7':17},
                '5':{'1':16,'2':17,'3':18,'4':19,'5':20,'6':21,'7':22},
                '6':{'1':13,'2':14,'3':15,'4':16,'5':17,'6':18,'7':19},
                '7':{'1':11,'2':12,'3':13,'4':14,'5':15,'6':16,'7':17},
                '8':{'1':15,'2':16,'3':17,'4':18,'5':19,'6':20,'7':21},
                '9':{'1':12,'2':13,'3':14,'4':15,'5':16,'6':17,'7':18},
                '10':{'1':17,'2':18,'3':19,'4':20,'5':21,'6':22,'7':23},
                '11':{'1':14,'2':15,'3':16,'4':17,'5':18,'6':19,'7':20},
                '12':{'1':12,'2':13,'3':14,'4':15,'5':16,'6':17,'7':18}}

    months = {'1':'-Jan-2016','2':'-Feb-2016','3':'-Mar-2016',
              '4':'-Apr-2016','5':'-May-2016','6':'-Jun-2016',
              '7':'-Jul-2016','8':'-Aug-2016','9':'-Sep-2016',
              '10':'-Oct-2016','11':'-Nov-2016','12':'-Dec-2016'}


    date = str(calender[month][day])+months[month]

    profile = []

    with open('../Documents/DemandData_2011-2016.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != date:
                continue

            profile.append(float(row[4]))
    return profile

def getNewLoads(m):

    profileA = []
    profileB = []
    profileC = []

    with open('../Documents/simulation_results/NTS/national/wed/'+m+'.csv',
              'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if int(row[0]) < 1440:
                continue

            profileA.append(float(row[1])*1000)
            profileB.append(float(row[2])*1000)
            profileC.append(float(row[4])*1000)

    profileA_ = [0]*48
    profileB_ = [0]*48
    profileC_ = [0]*48
    for t in range(1440):
        profileA_[int(t/30)] += profileA[t]/30
        profileB_[int(t/30)] += profileB[t]/30
        profileC_[int(t/30)] += profileC[t]/30
        
    return [profileA_,profileB_,profileC_]


class FuelMix:

    def __init__(self):
        _steam = 16334
        _combined = 32887
        _nuclear = 9361
        _gas = 1680
        _hydro_flow = 1623
        _hydro_pump = 2744
        _wind = 8529
        _solar = 12760
        _renew_oth = 5964

        self.flat_renewable = _renew_oth+_hydro_flow
        self.flat_fossil = _steam+_combined+_gas
        self.flat_nuclear = _nuclear
        self.wind_capacity = _wind
        self.solar_capacity = _solar

        self.wind = {}
        self.solar = {}
        for i in range(12):
            self.wind[str(i+1)] = []
            self.solar[str(i+1)] = []

    def set_renewable_shapes(self,solar,wind):
        for m in self.wind:
            self.wind[m] = wind[m]
            self.solar[m] = solar[m]

    def get_plot_y_values(self,m):
        y0 = [0]*48
        y1 = [self.flat_renewable/1000]*48
        y2 = []
        y3 = []
        y4 = []
        y5 = []
        for t in range(48):
            y2.append(y1[t]+self.solar[m][t]*self.solar_capacity/1000)
            y3.append(y2[-1]+self.wind[m][t]*self.wind_capacity/1000)
            y4.append(y3[-1]+self.flat_nuclear/1000)
            y5.append(y4[-1]+self.flat_fossil/1000)

        return [y0,y1,y2,y3,y4,y5]

    def calc_best_mix(self,p,m):
        renew = []
        for t in range(48):
            renew.append(self.flat_renewable+\
                         self.solar_capacity*self.solar[m][t]+\
                         self.wind[m][t]*self.wind_capacity)

        r = 0
        n = 0
        f = 0

        for t in range(48):
            if p[t] < renew[t]:
                r += p[t]
                continue
            else:
                r += renew[t]
            if p[t]-renew[t] < self.flat_nuclear:
                n += p[t]-renew[t]
                continue
            else:
                n += self.flat_nuclear
            f += p[t]-renew[t]-self.flat_nuclear

        return [r,n,f]

    def compare_demand_mixes(self,p_,m):
        r = []
        for i in range(len(p_)):
            m_ = self.calc_best_mix(p_[i],m)
            r.append(round(100*m_[0]/sum(m_),1))

        return r
        
class Simulation:

    def __init__(self):
        self.best = FuelMix()
        self.worst = FuelMix()

    def set_renew(self,bestSolar,worstSolar,bestWind,worstWind):
        self.best.set_renewable_shapes(bestSolar,bestWind)
        self.worst.set_renewable_shapes(worstSolar,worstWind)

    def get_renewables_range(self,p,m):
        high = self.best.calc_best_mix(p,m)
        low = self.worst.calc_best_mix(p,m)

        return [high[0]/sum(high),low[0]/sum(low)]

    def compare_mix(self,m):
        [p1,p2,p3] = getNewLoads(m)

        high = self.best.compare_demand_mixes([p1,p2,p3],m)
        low = self.worst.compare_demand_mixes([p1,p2,p3],m)

        return [high,low]
        

    def plot_mixes(self,m,d='3'):
        p = getBaseLoad(d,m)
        plt.figure(figsize=(8,5))
        c = ['#99FF99','#FFFF99','#BBCCFF','#FFCCCC','#BBBBBB']
        l = ['Other','Solar','Wind','Nuclear','Fossil']
        p_ = []
        for t in range(48):
            p_.append(p[t]/1000)
        
        plt.subplot(1,2,1)
        y = self.best.get_plot_y_values(m)
        for i in range(len(y)-1):
            plt.fill_between(range(48),y[i],y[i+1],color=c[i],label=l[i])
        plt.plot(p_,c='k')
        [r,n,f] = self.best.calc_best_mix(p,m)
        plt.title('Best Case\n'+str(round(100*r/(r+n+f),1))+'%',y=0.6)
        plt.ylim(0,90)
        plt.xlim(0,47)
        plt.xticks([11,23,35],['06:00','12:00','18:00'])
        plt.grid()
        plt.ylabel('Power (GW)')
        
        plt.subplot(1,2,2)
        y = self.worst.get_plot_y_values(m)
        for i in range(len(y)-1):
            plt.fill_between(range(48),y[i],y[i+1],color=c[i],label=l[i])
        plt.plot(p_,c='k')
        [r,n,f] = self.worst.calc_best_mix(p,m)
        plt.title('Worst Case\n'+str(round(100*r/(r+n+f),1))+'%',y=0.6)
        plt.ylim(0,90)
        plt.xlim(0,47)
        plt.xticks([11,23,35],['06:00','12:00','18:00'])
        plt.grid()
        plt.legend(ncol=3)
        
        plt.tight_layout()
        plt.show()

# get the best and worst solar

best_solar = {}
with open('pv/best_solar.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m = row[0]
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        best_solar[m] = p
        
worst_solar = {}
with open('pv/worst_solar.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m = row[0]
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        worst_solar[m] = p

best_wind = {}
with open('pv/best_wind.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m = row[0]
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        best_wind[m] = p
        
worst_wind = {}
with open('pv/worst_wind.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m = row[0]
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        worst_wind[m] = p

# Now instantiate class
sim = Simulation()
sim.set_renew(best_solar,worst_solar,best_wind,worst_wind)
sim.plot_mixes('1')

baseH = []
dumbH = []
smartH = []
baseL = []
dumbL = []
smartL = []
for m in ['1','4','7','10']:
    [h,l] = sim.compare_mix(m)
    baseH.append(h[0])
    baseL.append(l[0])
    dumbH.append(h[1])
    dumbL.append(l[1])
    smartH.append(h[2])
    smartL.append(l[2])
    
plt.figure()
plt.fill_between(range(4),baseL,baseH,color='g',alpha=0.2)
plt.fill_between(range(4),dumbL,dumbH,color='b',alpha=0.2)

plt.xticks(range(4),['Jan','Apr','Jul','Oct'])
plt.grid()
plt.ylim(0,100)
plt.show()
plt.subplot(2,1,1)
plt.title('Max Renewable Generation')
plt.scatter(range(4),baseH,marker='x',c='b',label='base')
plt.scatter(range(4),smartH,c='g',marker='x',label='smart')
plt.scatter(range(4),dumbH,marker='x',c='r',label='dumb')
plt.legend(ncol=3)
plt.xticks(range(4),['Jan','Apr','Jul','Oct'])
plt.grid()


plt.subplot(2,1,2)
plt.title('Min Renewable Generation')
plt.scatter(range(4),baseL,marker='x',c='b')
plt.scatter(range(4),smartL,marker='x',c='g')
plt.scatter(range(4),dumbL,marker='x',c='r')
plt.xticks(range(4),['Jan','Apr','Jul','Oct'])
plt.grid()
plt.tight_layout()
plt.show()
'''
# installed capacity - MW
steam = 16334
combined = 32887
nuclear = 9361
gas = 1680
hydro_flow = 1623
hydro_pump = 2744
wind = 8529
solar = 2172
renew_oth = 5964

f = steam+combined+gas
n = [nuclear]*1440
print(steam+combined+nuclear+gas+hydro_flow+hydro_pump+wind+solar+renew_oth)
fossil = [f]*1440
flat = [renew_oth+hydro_flow]*1440

w = []
s = []
for t in range(1440):
    w.append(random.random()*wind/2+wind/2)
    s.append(random.random()*solar/2+solar/2)
    
plt.figure()
plt.subplot(1,2,1)
plt.fill_between(range(1440),[0]*1440,flat,color='#99FF99')

y1 = []
y2 = []
y3 = []
y4 = []
for t in range(1440):
    y1.append(flat[t]+s[t])
    y2.append(y1[-1]+w[t])
    y3.append(y2[-1]+nuclear)
    y4.append(y3[-1]+f)

plt.fill_between(range(1440),[0]*1440,flat,color='#99FF99')
plt.fill_between(range(1440),flat,y1,color='#FFFF99')
plt.fill_between(range(1440),y1,y2,color='#BBCCFF')
plt.fill_between(range(1440),y2,y3,color='#FFCCCC')
plt.fill_between(range(1440),y3,y4,color='#BBBBBB')

plt.subplot(1,2,2)
y1 = []
y2 = []
for t in range(1440):
    y1.append(flat[t]+n[t])
    y2.append(y1[-1]+fossil[t])
plt.fill_between(range(1440),[0]*1440,flat,color='#99FF99')
plt.fill_between(range(1440),flat,y1,color='#FFCCCC')
plt.fill_between(range(1440),y1,y2,color='#BBBBBB')

plt.show()
'''
