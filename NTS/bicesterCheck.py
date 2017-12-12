import csv
import matplotlib.pyplot as plt

plt.figure(1)

folder = ['bicester3/','bicesterSmart3/']
for i in range(2):
    with open('../../Documents/'+folder[i]+'Mar-Fri.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        p = []
        for row in reader:
            p.append(float(row[1]))
        plt.plot(p)
        print(sum(p))

plt.show()
