import csv
import matplotlib.pyplot as plt

dumb = '../../Documents/My_Electric_avenue_Technical_Data/profiles/unchanged/'
smart = '../../Documents/My_Electric_avenue_Technical_Data/profiles/smart/'

plt.figure(1)
for i in range(1,17):
    plt.subplot(4,4,i)
    profile1 = []
    with open(dumb+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            profile1.append(float(row[0]))
            
    profile2 = []
    with open(smart+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            profile2.append(float(row[0]))

    plt.plot(profile1)
    plt.plot(profile2)

plt.show()
            

