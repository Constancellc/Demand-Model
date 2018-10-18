import csv
import matplotlib.pyplot as plt
import random

c = 0
hhProfiles = {}
with open('../../../Documents/pecan-street/1min-texas/profiles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = [0.0]*1440
        for t in range(1440):
            p[int(t)] += float(row[t])
        hhProfiles[c] = p
        c += 1

plt.figure()
for i in range(4):
    plt.subplot(2,2,i+1)
    plt.plot(hhProfiles[int(random.random()*c)])
plt.show()
