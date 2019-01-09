# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random


'''
So far I've basically just made a capacity picture

I need to make a function which:

inputs: month, power demand
output: best & worst case fuel mix

to do list:
- get highest and lowest profiles for solar as % of generation for each month
- get same for wind
- work out code structure

'''



class FuelMix:

    def __init__(self):
        _steam = 16334
        _combined = 32887
        _nuclear = 9361
        _gas = 1680
        _hydro_flow = 1623
        _hydro_pump = 2744
        _wind = 8529
        _solar = 2172
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
        y1 = [self.flat_renewable]*48
        y2 = []
        y3 = []
        y4 = []
        y5 = []
        for t in range(48):
            y2.append(y1[t]+self.solar[m][t]*self.solar_capacity)
            y3.append(y2[-1]+self.wind[m][t]*self.wind_capacity)
            y4.append(y3[-1]+self.flat_nuclear)
            y5.append(y4[-1]+self.flat_fossil)

        return [y1,y2,y3,y4,y5]

    def calc_best_mix(self,p,m):
        renew = []
        for t in range(48):
            renew.append(flat_renewable+self.solar_capacity*self.solar[m][t]+\
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

    def plot_mixes(self,p,m):
        plt.figure()
        c = ['#99FF99','#FFFF99','#BBCCFF','#FFCCCC','#BBBBBB']
        l = ['Other','Solar','Wind','Nuclear','Fossil']
        
        plt.subplot(1,2,1)
        y = self.best.get_plot_y_values(m)
        y = [[0]*48,y]
        for i in range(len(y)-1):
            plt.fill_between(range(48),y[i],y[i+1],color=c[i],label=l[i])
        plt.plot(p,c='k')
        
        
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
