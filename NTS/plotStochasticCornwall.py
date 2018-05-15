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
    base1 = []
    base2 = []
    base3 = []
    base4 = []
    base5 = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    p6 = []
    p7 = []
    p8 = []
    p9 = []
    p10 = []
    p11 = []
    p12 = []
    p13 = []
    p14 = []
    p15 = []
    pav = []

    with open(resultsStem+m+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        #next(reader)
        for row in reader:
            t.append(float(row[0]))
            base1.append(float(row[1]))
            base2.append(float(row[2]))
            base3.append(float(row[3]))
            p1.append(float(row[4]))
            p2.append(float(row[5]))
            p3.append(float(row[6]))
            p4.append(float(row[7]))
            p5.append(float(row[8]))
            p6.append(float(row[9]))
            p7.append(float(row[10]))
            p8.append(float(row[11]))
            p9.append(float(row[12]))
            p10.append(float(row[13]))
            p11.append(float(row[14]))
            p12.append(float(row[15]))
            p13.append(float(row[16]))
            p14.append(float(row[17]))
            p15.append(float(row[18]))

    p1 = scipy.ndimage.filters.gaussian_filter1d(p1,2)
    p2 = scipy.ndimage.filters.gaussian_filter1d(p2,2)
    p3 = scipy.ndimage.filters.gaussian_filter1d(p3,2)
    p4 = scipy.ndimage.filters.gaussian_filter1d(p4,2)
    p5 = scipy.ndimage.filters.gaussian_filter1d(p5,2)
    p6 = scipy.ndimage.filters.gaussian_filter1d(p6,2)
    p7 = scipy.ndimage.filters.gaussian_filter1d(p7,2)
    p8 = scipy.ndimage.filters.gaussian_filter1d(p8,2)
    p9 = scipy.ndimage.filters.gaussian_filter1d(p9,2)
    p10 = scipy.ndimage.filters.gaussian_filter1d(p10,2)
    p11 = scipy.ndimage.filters.gaussian_filter1d(p11,2)
    p12 = scipy.ndimage.filters.gaussian_filter1d(p12,2)
    p13 = scipy.ndimage.filters.gaussian_filter1d(p13,2)
    p14 = scipy.ndimage.filters.gaussian_filter1d(p14,2)
    p15 = scipy.ndimage.filters.gaussian_filter1d(p15,2)

    min1 = [1000.0]*len(t)
    max1 = [0.0]*len(t)
    min2 = [1000.0]*len(t)
    max2 = [0.0]*len(t)

    for tt in range(len(p1)):
        for p in [p7,p8,p9,p10]:
            if p[tt] > max1[tt]:
                max1[tt] = p[tt]
            if p[tt] < min1[tt]:
                min1[tt] = p[tt]

    for tt in range(len(p1)):
        for p in [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15]:
            if p[tt] > max2[tt]:
                max2[tt] = p[tt]
            if p[tt] < min2[tt]:
                min2[tt] = p[tt]
            

 
    #plt.fill_between(t,p1,p5,color='#dddddd')
    plt.fill_between(t,min2,max2,color='#b7d2ff')
    #plt.fill_between(t,p5,p4,color='#b7d2ff')
    plt.fill_between(t,min1,max1,color='#b56bff')
    #plt.fill_between(t,p7,p9,color='r')#82abed')
    plt.plot(t,base1,'k',ls=':',label='Max Net Demand')
    plt.plot(t,base3,'k',ls=':',label='Min Net Demand')
    plt.plot(t,p8,color='#0d50bc',label='Including EVs')

    x = np.linspace(26*60,46*60,num=6)
    x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
    plt.xticks(x,x_ticks)
    plt.xlim(24*60,48*60)
    plt.ylim(200,650)
    plt.grid()

    if n == 2 or n == 4:
        plt.ylabel('Power Demand (MW)')

    if n == 2:
        plt.legend(loc=8)


plt.tight_layout()
plt.savefig('../../Dropbox/papers/smart-charging/cornwall.eps', format='eps', dpi=1000)
plt.show()
