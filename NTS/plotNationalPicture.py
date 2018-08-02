# packages
import matplotlib.pyplot as plt
import numpy as np
import csv

resultsStem = '../../Documents/simulation_results/NTS/national/wed/'

plotPsuedo = False
plot7 = True

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 8
plotMonths = {'1':1,'4':2,'7':3,'10':4}
titles = {'1':'January','4':'April','7':'July','10':'October'}

t = np.linspace(0,64,64*60)
x = np.linspace(26,46,num=6)
my_xticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
3839
for month in ['1','4','7','10']:
    smart = []
    dumb3 = []
    dumb7 = []
    base = []
    psuedo = []
    with open(resultsStem+month+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            base.append(float(row[1]))
            dumb3.append(float(row[2]))
            dumb7.append(float(row[3]))
            smart.append(float(row[4]))
            if plotPsuedo == True:
                psuedo.append(float(row[5]))
    plt.figure(1)
    plt.subplot(2,2,plotMonths[month])
    plt.plot(t,base,ls=':',c='g',label='Base Load')
    plt.plot(t,dumb3,label='Uncontrolled Charging 3kW')
    
    if plotPsuedo == True:
        plt.plot(t,psuedo,c='b',ls='-.',label='Approximation')       
        plt.plot(t,smart,label='Optimal')
    else:
        plt.plot(t,smart,ls='--',label='Controlled Charging')

    if plot7 == True:
        plt.plot(t,dumb7,label='Uncontrolled Charging 7kW')
    
    if month == '1':
        if plotPsuedo == True or plot7 == True:
            plt.legend(loc=[0.1,1.1],ncol=3)
        else:
            plt.legend(loc=[-0.2,1.1],ncol=3)
        
    plt.xticks(x, my_xticks)
    if month == '7' or '10':
        plt.xlabel('time')
    if month == '7' or '1':
        plt.ylabel('Power Demand (GW)')
    plt.xlim(24,48)
    plt.ylim(0,70)
    plt.title(titles[month],y=0.8)
    plt.grid()

    if month == '1':
        plt.figure(figsize=(5,4)) # January only
        plt.rcParams["font.size"] =9
        plt.plot(t,base,ls=':',c='k',label='Base')
        plt.plot(t,dumb3,label='Uncontrolled')
        plt.plot(t,smart,ls='--',label='Optimal')
        plt.plot(t,psuedo,label='Approximate')
        plt.ylabel('Power Demand (GW)')
        plt.xticks(x, my_xticks)
        plt.xlabel('time')
        plt.xlim(24,48)
        #plt.ylim(0,70)
        plt.legend(ncol=2)
        plt.grid()
        plt.tight_layout()
        plt.savefig('../../Documents/policy-summary.pdf', format='pdf', dpi=1000)


plt.show()
