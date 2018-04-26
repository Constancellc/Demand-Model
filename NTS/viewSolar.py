import csv
import matplotlib.pyplot as plt


ms = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun','7':'Jul',
      '8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}

plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
x_ticks = ['04:00','12:00','20:00']
xx = [8,24,40]
for mo in range(1,13):
    times = []
    for i in range(48):
        times.append([])
    with open('../../Documents/cornwall-pv-predictions/'+ms[str(mo)]+'.csv',
              'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for i in range(48):
                times[i].append(float(row[i])/5600)
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []

    for t in range(48):
        x = sorted(times[t])
        N = len(x)

        c = 0
        s = []
        while c < int(N*0.05):
            s.append(x[c])
            c += 1
        p1.append(sum(s)/len(s))
        
        s = []
        while c < int(N*0.25):
            s.append(x[c])
            c += 1
        p2.append(sum(s)/len(s))
        
        s = []
        while c < int(N*0.75):
            s.append(x[c])
            c += 1
        p3.append(sum(s)/len(s))
        
        s = []
        while c < int(N*0.95):
            s.append(x[c])
            c += 1
        p4.append(sum(s)/len(s))
        
        s = []
        while c < N:
            s.append(x[c])
            c += 1
        p5.append(sum(s)/len(s))
    plt.subplot(4,3,mo)
    plt.title(ms[str(mo)],y=0.65)
    plt.fill_between(range(48),p1,p5,color='#c0d6f9')
    plt.fill_between(range(48),p2,p4,color='#7fadff')
    plt.plot(p3,'b')
    plt.ylim(0,95)
    plt.grid()
    plt.xticks(xx,x_ticks)
    plt.xlim(0,48)

    
    for t in range(48):
        p1[t] = p1[t]*5600 # % to kW for cornwall
        p2[t] = p2[t]*5600
        p3[t] = p3[t]*5600
        p4[t] = p4[t]*5600
        p5[t] = p5[t]*5600
        
    with open('../../Documents/cornwall-pv-predictions/av-'+ms[str(mo)]+'.csv',
              'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(p1)
        writer.writerow(p2)
        writer.writerow(p3)
        writer.writerow(p4)
        writer.writerow(p5)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/smart-charging/pv.eps', format='eps', dpi=1000)

plt.show()
