import csv
import matplotlib.pyplot as plt
import numpy as np

    
plt.figure()
files = ['50evs.csv','50evsCtrl.csv']
labels = ['clustered','uniform']
for ii in range(2):
    file = files[ii]
    m = [0.0]*(1440*4)
    with open(file,'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            s = 0
            for i in range(1,len(row)):
                s += float(row[i])
            m[int(row[0])-1440] = s/(len(row)-1)
              

    v = [0.0]*(1440*4)
    with open(file,'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
              se = 0
              for i in range(1,len(row)):
                  se += np.power(float(row[i])-m[int(row[0])-1440],2)


              v[int(row[0])-1440] = se/(len(row)-1)

    u = []
    l = []

    for i in range(len(m)):
        u.append(m[i]+np.sqrt(v[i]))
        l.append(m[i]-np.sqrt(v[i]))

    plt.fill_between(range(1440*4),l,u,alpha=0.2)
    plt.plot(range(1440*4),m,label=labels[ii])
plt.xlim(1440,1440*2)
plt.xticks([2*60+1440,6*60+1440,10*60+1440,14*60+1440,18*60+1440,22*60+1440],
           ['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.grid()
plt.ylabel('Power Demand (kW)')
plt.ylim(0,60)
plt.legend()
plt.tight_layout()
plt.show()

            
          
          
            
