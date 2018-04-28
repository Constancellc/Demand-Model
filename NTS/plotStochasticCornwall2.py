# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy.ndimage

resultsStem = '../../Documents/simulation_results/NTS/cornwall2/'


plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 8

    
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
    base4 = []
    base5 = []
    p1 = []
    p2 = []
    p3 = []
    p5 = []
    p4 = []
    pav = []

    with open(resultsStem+m+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            t.append(float(row[0]))
            base1.append(float(row[1]))
            base2.append(float(row[2]))
            base3.append(float(row[3]))
            base4.append(float(row[4]))
            base5.append(float(row[5]))
            p1.append(float(row[6]))
            p2.append(float(row[7]))
            p3.append(float(row[8]))
            p4.append(float(row[10]))
            p5.append(float(row[9]))

    p1 = scipy.ndimage.filters.gaussian_filter1d(p1,2)
    p2 = scipy.ndimage.filters.gaussian_filter1d(p2,2)
    p3 = scipy.ndimage.filters.gaussian_filter1d(p3,2)
    p4 = scipy.ndimage.filters.gaussian_filter1d(p4,2)
    p5 = scipy.ndimage.filters.gaussian_filter1d(p5,2)

    
 
    #plt.fill_between(t,p1,p5,color='#dddddd')
    plt.fill_between(t,p1,p2,color='#b7d2ff')
    plt.fill_between(t,p5,p4,color='#b7d2ff')
    plt.fill_between(t,p2,p5,color='#7fadff')
    #plt.fill_between(t,p2,p4,color='#82abed')
    plt.plot(t,base1,'k',ls=':',label='Max Net Demand')
    plt.plot(t,base5,'k',ls=':',label='Min Net Demand')
    plt.plot(t,p3,color='#0d50bc',label='Including EVs')

    x = np.linspace(26*60,46*60,num=6)
    x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
    plt.xticks(x,x_ticks)
    plt.xlim(24*60,48*60)
    plt.ylim(-50,600)
    plt.grid()

    if n == 2 or n == 4:
        plt.ylabel('Power Demand (MW)')

    if n == 2:
        plt.legend(loc=8)



plt.tight_layout()
#plt.savefig('../../Dropbox/papers/smart-charging/cornwall2.eps', format='eps', dpi=1000)
plt.show()
