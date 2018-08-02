# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy.ndimage

resultsStem = '../../Documents/simulation_results/NTS/national_stochastic/'

resultsStem2 = '../../Documents/simulation_results/NTS/national/wed/'

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 10

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
            dumb7.append(float(row[3])-float(row[1]))
            
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
    base = []
    base = []
    base = []
    d3 = []
    d7 = []
    p8 = []
    tt = 0

    with open(resultsStem+m+'_experienced.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            t.append(float(row[0]))
            base.append(float(row[2]))
            d3.append(dumb3[10*tt]+float(row[2]))
            d7.append(dumb7[10*tt]+float(row[2]))
            tt += 1
            p8.append(float(row[11]))
            #pav.append(0.05*p1[-1]+0.2*p2[-1]+0.5*p3[-1]+0.2*p4[-1]+0.05*p5[-1])


    p8 = scipy.ndimage.filters.gaussian_filter1d(p8,2)
    
 
    #plt.subplot(1,2,1)
    plt.plot(t,base,'k',ls=':',label='Min Base')
    plt.plot(t,d3,color='g',label='Uncontrolled 3.5 kW')
    plt.plot(t,d7,color='r',label='Uncontrolled 7 kW')
    plt.plot(t,p8,color='#0d50bc',label='Controlled')

    
    x = np.linspace(26*60,46*60,num=6)
    x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
    plt.xticks(x,x_ticks)
    plt.xlim(24*60,48*60)
    plt.grid()
    plt.ylim(20,70)

    if n == 2 or n == 4:
        plt.ylabel('Power Demand (GW)')

    if n == 4:
        plt.legend(loc=6)

plt.tight_layout()
plt.show()
