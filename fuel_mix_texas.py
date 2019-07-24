# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random


def interpolate(f):
    f2 = []
    for i in range(23):
        f2.append(f[i])
        f2.append((f[i]+f[i+1])/2)
    f2.append(f[23])
    f2.append((f[23]+f[0])/2)
    return f2

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
    
    tm = ['sp','su','au','wt']
    profileA = []
    profileB = []
    profileC = []

    p = getHighest(m)
    for i in range(48):
        profileA.append(

    with open('../Documents/simulation_results/NHTS/national/wed/'+m+'.csv',
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

    c = (sum(profileC_)-sum(profileA_))/sum(profileA_) # % increase in load due to charging

    s1 = 1+c*0.12 # percentage increase in losses between uncontrolled and controlled

    for t in range(48):
        profileB_[t] = profileB_[t]*s1

        
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

        self.flat_renewable = 980
        self.flat_fossil = _46000
        self.flat_nuclear = 4700
        self.wind_capacity = 22600
        self.solar_capacity = 2900

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
        y1 = []#self.flat_renewable/1000]*48
        y2 = []
        y3 = []
        y4 = []
        y5 = []
        for t in range(48):
            y1.append(y0[t]+self.solar[m][t]*self.solar_capacity/1000)
            y2.append(y1[-1]+self.wind[m][t]*self.wind_capacity/1000)
            y3.append(y2[-1]+self.flat_renewable/1000)
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

    def set_renew(self,solarShape,_bestWind,_worstWind):
        # first rescale
        sc = max(solarShape)
        wc = max(_bestWind)
        bestSolar = []
        bestWind = []
        worstSolar = []
        worstWind = []

        for i in range(48):
            bestSolar.append(solarShape[i]*0.95/sc)
            worstSolar.append(solarShape[i]*0.25/sc)
            bestWind.append(_bestWind[i]/wc)
            worstWind.append(_worstWind[i]/wc)
        
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
        p = getBaseLoad(d,m[1])
        plt.figure(figsize=(9,3.5))
        plt.rcParams["font.family"] = 'serif'
        plt.rcParams["font.size"] = '11'
        c = ['#FFFF99','#BBCCFF','#99FF99','#FFCCCC','#BBBBBB']
        l = ['Solar','Wind','Other','Nuclear','Fossil']
        p_ = []
        for t in range(48):
            p_.append(p[t]/1000)
        
        plt.subplot(1,2,1)
        y = self.best.get_plot_y_values(m[1])
        for i in range(len(y)-1):
            plt.fill_between(range(48),y[i],y[i+1],color=c[i],label=l[i])
        plt.plot(p_,c='k')
        [r,n,f] = self.best.calc_best_mix(p,m[1])
        plt.title('Best Case\n'+str(round(100*r/(r+n+f),1))+'%',y=0.6)
        plt.ylim(0,90)
        plt.xlim(0,47)
        plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
        plt.grid()
        plt.ylabel('Power (GW)')
        
        plt.subplot(1,2,2)
        p = getBaseLoad(d,m[0])
        p_ = []
        for t in range(48):
            p_.append(p[t]/1000)
        y = self.worst.get_plot_y_values(m[0])
        for i in range(len(y)-1):
            plt.fill_between(range(48),y[i],y[i+1],color=c[i],label=l[i])
        plt.plot(p_,c='k')
        [r,n,f] = self.worst.calc_best_mix(p,m[0])
        plt.title('Worst Case\n'+str(round(100*r/(r+n+f),1))+'%',y=0.6)
        plt.ylim(0,90)
        plt.xlim(0,47)
        plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
        plt.grid()
        plt.legend(ncol=3)
        plt.grid(ls=':')
        plt.tight_layout()
        plt.savefig('../Dropbox/thesis/chapter5/img/fuelmix.eps', format='eps',
                    dpi=300, bbox_inches='tight', pad_inches=0)
        plt.show()

# get the best and worst solar
solar_shape = [0]
with open('pv/best_solar.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
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
with open('pv/w0orst_wind.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = []
        for i in range(1,len(row)):
            p.append(float(row[i]))
        if sum(p) < sum(worst_wind):
            worst_wind = p

# Now instantiate class
sim = Simulation()
sim.set_renew(solar_shape,best_wind,worst_wind)
sim.plot_mixes(['1','7'])

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
    
plt.figure(figsize=(8.5,3))
plt.subplot(1,2,1)
plt.title('Max Renewable Generation')
plt.bar(np.arange(4)-0.2,baseH,width=0.2,color='gray',label='base',zorder=2)
plt.bar(np.arange(4),dumbH,width=0.2,color='b',label='dumb',zorder=2)
plt.bar(np.arange(4)+0.2,smartH,width=0.2,color='r',label='smart',zorder=2)

plt.ylim(0,60)
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
plt.ylim(0,60)
plt.grid(ls=':',zorder=0)
plt.tight_layout()
plt.savefig('../Dropbox/thesis/chapter5/img/fuelmix2.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0)
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
