# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy.ndimage

resultsStem = '../../Documents/simulation_results/NTS/national_stochastic/'

resultsStem2 = '../../Documents/simulation_results/NTS/national/wed/'

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 8

t = np.arange(0,64*60)
plotMonths = {'1':1,'4':2,'7':3,'10':4}
for month in ['1','4','7','10']:
    dumb3 = []
    dumb7 = []
    with open(resultsStem2+month+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            dumb3.append(float(row[2]))
            dumb7.append(float(row[3]))
            
    plt.subplot(2,2,plotMonths[month])
    plt.plot(t,dumb3,color='#5bcc92',label='Uncontrolled')
    #plt.plot(t,dumb7,'y',ls='--',label='Uncontrolled Charging 3kW')
    
months = {'1':'January','4':'April','7':'July','10':'October'}
n = 1
for m in months:
    plt.subplot(2,2,n)
    n += 1
    plt.title(months[m],y=0.88)

    t = []
    base = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    pav = []

    with open(resultsStem+m+'_experienced.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            t.append(float(row[0]))
            base.append(float(row[1]))
            p1.append(float(row[2]))
            p2.append(float(row[3]))
            p3.append(float(row[4]))
            p4.append(float(row[5]))
            p5.append(float(row[6]))
            pav.append(0.05*p1[-1]+0.2*p2[-1]+0.5*p3[-1]+0.2*p4[-1]+0.05*p5[-1])

    p1 = scipy.ndimage.filters.gaussian_filter1d(p1,2)
    p2 = scipy.ndimage.filters.gaussian_filter1d(p2,2)
    p3 = scipy.ndimage.filters.gaussian_filter1d(p3,2)
    p4 = scipy.ndimage.filters.gaussian_filter1d(p4,2)
    p5 = scipy.ndimage.filters.gaussian_filter1d(p5,2)
    
    min1 = []
    max1 = []
    min2 = []
    max2 = []

    for i in range(len(base)):
        lowest = 100
        highest = 0
        for p in [p2,p3,p4]:
            if p[i] < lowest:
                lowest = p[i]
            if p[i] > highest:
                highest = p[i]
                
        min1.append(lowest)
        max1.append(highest)
        
        for p in [p1,p5]:
            if p[i] < lowest:
                lowest = p[i]
            if p[i] > highest:
                highest = p[i]
                
        min2.append(lowest)
        max2.append(highest)
    #plt.subplot(1,2,1)
    plt.plot(t,base,'k',ls=':',label='Base load')
    plt.plot(t,p3,color='#0d50bc',label='Controlled')
    #plt.fill_between(t,min1,max1,color='b',alpha=0.1)
    plt.fill_between(t,min2,max2,color='#7fadff')

    x = np.linspace(26*60,46*60,num=6)
    x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
    plt.xticks(x,x_ticks)
    plt.xlim(24*60,48*60)
    plt.grid()
    #plt.ylim(20,70)

    if n == 2 or n == 4:
        plt.ylabel('Power Demand (GW)')

    if n == 5:
        plt.legend(loc=8)



plt.tight_layout()
plt.savefig('../../Dropbox/papers/smart-charging/national.eps', format='eps', dpi=1000)
plt.show()
