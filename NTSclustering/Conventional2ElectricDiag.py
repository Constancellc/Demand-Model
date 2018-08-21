import csv
import matplotlib.pyplot as plt

chargingPdf = {}
for i in range(5):
    chargingPdf[i] = []

with open('chargePdfW.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(5):
            for t in range(30):
                chargingPdf[i].append(float(row[i+1])/3000)

p = chargingPdf[1]               
plt.figure()
plt.subplot(2,2,1)
plt.plot(p)

for t in range(8*60+14,8*60+55):
    p[t] = 0
for t in range(16*60+44,
