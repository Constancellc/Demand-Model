import csv
import matplotlib.pyplot as plt

months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov',
          'dec']

stem = '../../Documents/cornwall-pv-predictions/'

plt.figure(1)
for i in range(0,len(months)):
    plt.subplot(4,3,i+1)
    plt.title(months[i],y=0.9)
    plt.ylim(0,600000)
    plt.xlim(0,47)
    with open(stem+months[i]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            profile = []
            for j in range(0,48):
                profile.append(float(row[j]))
            plt.plot(profile)

plt.show()
