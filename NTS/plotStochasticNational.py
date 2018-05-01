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
            dumb3.append(float(row[2])-float(row[1]))
            dumb7.append(float(row[3]))
            
    #plt.subplot(2,2,plotMonths[month])
    #plt.plot(t,dumb3,color='#5bcc92',label='Uncontrolled')
    #plt.plot(t,dumb7,'y',ls='--',label='Uncontrolled Charging 3kW')
    
months = {'1':'January','4':'April','7':'July','10':'October'}
n = 1
for m in months:
    plt.subplot(2,2,n)
    n += 1
    plt.title(months[m],y=0.88)

    t = []
    base1 = []
    base2 = []
    base3 = []
    d1 = []
    d2 = []
    d3 = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    p5 = []
    p6 = []
    p7 = []
    p8 = []
    p9 = []
    #pav = []
    tt = 0

    with open(resultsStem+m+'_experienced.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            t.append(float(row[0]))
            base1.append(float(row[1]))
            base2.append(float(row[2]))
            base3.append(float(row[3]))
            d1.append(dumb3[10*tt]+float(row[1]))
            d2.append(dumb3[10*tt]+float(row[2]))
            d3.append(dumb3[10*tt]+float(row[3]))
            tt += 1
            p1.append(float(row[4]))
            p2.append(float(row[5]))
            p3.append(float(row[6]))
            p4.append(float(row[7]))
            p5.append(float(row[8]))
            p6.append(float(row[9]))
            p7.append(float(row[10]))
            p8.append(float(row[11]))
            p9.append(float(row[12]))
            #pav.append(0.05*p1[-1]+0.2*p2[-1]+0.5*p3[-1]+0.2*p4[-1]+0.05*p5[-1])

    p1 = scipy.ndimage.filters.gaussian_filter1d(p1,2)
    p2 = scipy.ndimage.filters.gaussian_filter1d(p2,2)
    p3 = scipy.ndimage.filters.gaussian_filter1d(p3,2)
    p4 = scipy.ndimage.filters.gaussian_filter1d(p4,2)
    p5 = scipy.ndimage.filters.gaussian_filter1d(p5,2)
    p6 = scipy.ndimage.filters.gaussian_filter1d(p6,2)
    p7 = scipy.ndimage.filters.gaussian_filter1d(p7,2)
    p8 = scipy.ndimage.filters.gaussian_filter1d(p8,2)
    p9 = scipy.ndimage.filters.gaussian_filter1d(p9,2)
    
    min1 = []
    max1 = []
    min2 = []
    max2 = []

    for i in range(len(base1)):
        lowest = 100
        highest = 0
        for p in [p1,p2,p3,p4,p5,p6,p7,p8,p9]:
            if p[i] < lowest:
                lowest = p[i]
            if p[i] > highest:
                highest = p[i]
                
        min1.append(lowest)
        max1.append(highest)
        
        lowest = 100
        highest = 0
        for p in [p4,p5,p6]:
            if p[i] < lowest:
                lowest = p[i]
            if p[i] > highest:
                highest = p[i]
                
        min2.append(lowest)
        max2.append(highest)
    #plt.subplot(1,2,1)
    plt.plot(t,base1,'k',ls=':',label='Base load')
    plt.plot(t,base3,'k',ls=':')
    plt.fill_between(t,d1,d3,color='g',alpha=0.1)
    plt.plot(t,d2,color='g',label='Uncontrolled')
    plt.plot(t,p5,color='#0d50bc',label='Controlled')
    plt.fill_between(t,min1,max1,color='b',alpha=0.1)
    plt.fill_between(t,min2,max2,color='#7fadff')

    x = np.linspace(26*60,46*60,num=6)
    x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
    plt.xticks(x,x_ticks)
    plt.xlim(24*60,48*60)
    plt.grid()
    plt.ylim(20,70)

    if n == 2 or n == 4:
        plt.ylabel('Power Demand (GW)')

    if n == 5:
        plt.legend(loc=8)

plt.tight_layout()
#plt.savefig('../../Dropbox/papers/smart-charging/national.eps', format='eps', dpi=1000)
plt.show()
