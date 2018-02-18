# packages
import matplotlib.pyplot as plt
import numpy as np
import csv

resultsStem = '../../Documents/simulation_results/NTS/national/'

plotPsuedo = True
plotClustered = False

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 8
plotMonths = {'1':1,'4':2,'7':3,'10':4}
titles = {'1':'January','4':'April','7':'July','10':'October'}

t = np.linspace(0,36,36*60)
x = np.linspace(8,32,num=5)
my_xticks = ['08:00 \n Wed','14:00','20:00','02:00','08:00 \n Thu']

for month in ['1','4','7','10']:
    smart = []
    dumb = []
    base = []
    psuedo = []
    with open(resultsStem+month+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            base.append(float(row[1]))
            dumb.append(float(row[2]))
            smart.append(float(row[3]))
            if plotPsuedo == True:
                psuedo.append(float(row[4]))

    for i in range(1440,2160):
        dumb[i-1440] += dumb[i]-base[i]
        smart[i-1440] += smart[i]-base[i]
        if plotPsuedo == True:
            psuedo[i-1440] += psuedo[i]-base[i]
        
    plt.subplot(2,2,plotMonths[month])
    plt.plot(t,base,ls=':',c='g',label='Base Load')
    plt.plot(t,dumb,label='Uncontrolled Charging')
    
    if plotPsuedo == True:
        plt.plot(t,psuedo,c='b',ls='-.',label='Approximation')       
        plt.plot(t,smart,label='Optimal')
    elif plotClustered == True:
        plt.plot(np.linspace(0,36,num=len(clustered)),clustered,c='b',ls='-.',label='Clustered')       
        plt.plot(t_smart,smartProfile,label='Optimal')
    else:
        plt.plot(t,smart,ls='--',label='Controlled Charging')
    
    if month == '1':
        if plotPsuedo == True or plotClustered == True:
            plt.legend(loc=[0.1,1.1],ncol=2)
        else:
            plt.legend(loc=[-0.2,1.1],ncol=3)
        
    plt.xticks(x, my_xticks)
    if month == '7' or '10':
        plt.xlabel('time')
    if month == '7' or '1':
        plt.ylabel('Power Demand (GW)')
    plt.xlim(6,34)
    plt.ylim(20,85)
    plt.title(titles[month],y=0.8)
    plt.grid()

plt.show()
