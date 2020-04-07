import csv
import matplotlib.pyplot as plt

plt.figure()
stem = '../../Documents/simulation_results/NTS/national/'
for s in ['wtr','atm','spr','smr']:
    m1 = []
    m2 = []
    with open(stem+'uncontrolled_'+s+'.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            m1.append(float(row[1]))
            m2.append(float(row[2]))
    plt.subplot(2,1,1)
    plt.plot(m1)
    plt.subplot(2,1,2)
    plt.plot(m2)
plt.show()
