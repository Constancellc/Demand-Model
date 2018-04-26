# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy.ndimage

resultsStem = '../../Documents/simulation_results/NTS/cornwall/'


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
    base = []
    dumb = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    pav = []

    with open(resultsStem+m+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            t.append(float(row[0]))
            dumb.append(float(row[1])+float(row[2]))
            base.append(float(row[2]))
            p1.append(float(row[3]))
            p2.append(float(row[4]))
            p3.append(float(row[5]))
            p4.append(float(row[6]))
            p5.append(float(row[7]))

    p1 = scipy.ndimage.filters.gaussian_filter1d(p1,2)
    p2 = scipy.ndimage.filters.gaussian_filter1d(p2,2)
    p3 = scipy.ndimage.filters.gaussian_filter1d(p3,2)
    p4 = scipy.ndimage.filters.gaussian_filter1d(p4,2)
    p5 = scipy.ndimage.filters.gaussian_filter1d(p5,2)

    pmin = []
    pmax = []

    for tt in range(len(p1)):
        pmin.append(min([p2[tt],p3[tt],p4[tt]]))
        pmax.append(max([p2[tt],p3[tt],p4[tt]]))


    #plt.subplot(1,2,1)
    plt.plot(t,base,'k',ls=':',label='Base load')
    plt.plot(t,dumb,color='#5bcc92',label='Uncontrolled')
    plt.plot(t,p3,color='#0d50bc',label='Controlled')
    plt.fill_between(t,p1,p2,color='#c0d6f9')
    plt.fill_between(t,pmin,pmax,color='#7fadff')
    plt.fill_between(t,p4,p5,color='#c0d6f9')

    x = np.linspace(26*60,46*60,num=6)
    x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
    plt.xticks(x,x_ticks)
    plt.xlim(24*60,48*60)
    plt.grid()
    plt.ylim(50,750)

    if n == 2 or n == 4:
        plt.ylabel('Power Demand (MW)')

    if n == 2:
        plt.legend(loc=8)



plt.tight_layout()
#plt.savefig('../../Dropbox/papers/smart-charging/cornwall.eps', format='eps', dpi=1000)
plt.show()
