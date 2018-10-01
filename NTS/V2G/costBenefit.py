import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt



plt.figure()
#plt.xlim(0,30)
#plt.ylim(0,120)

for pen in [50,100]:
    data = {}
    for p in range(40):
        data[p] = []
        
    with open('../../../Documents/simulation_results/NTS/v2g/v2g_lf'+
              str(pen)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            
            if float(row[2]) < 10:
                continue
            p = 100*(float(row[1])-float(row[3]))/float(row[1])
            t = 100*(float(row[4])-float(row[2]))/float(row[2])

            data[int(p)].append(t)
    
            #x.append((float(row[1])-float(row[3])))
            #y.append((float(row[4])-float(row[2])))
    #plt.scatter(x,y)
    x = []
    m = []
    l = []
    u = []

    for p in range(40):
        if len(data[p]) < 2:
            continue
        x.append(p)
        m.append(sum(data[p])/len(data[p]))
        v = 0
        for i in range(len(data[p])):
            v += abs(data[p][i]-m[-1])/len(data[p])
        l.append(m[-1]-v)
        u.append(m[-1]+v)

    plt.plot(x,m)
    plt.fill_between(x,l,u,alpha=0.2)
        

    

plt.show()
