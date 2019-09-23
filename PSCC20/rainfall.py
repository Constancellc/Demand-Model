import csv
import random
import matplotlib.pyplot as plt

res = {}
with open('res.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[2] not in res:
            res[row[2]] = []
        res[row[2]].append([float(row[0]),float(row[1]),float(row[3]),
                            float(row[4])])

plt.figure()
for s in res:
    print(s)
    r = [0]*100
    n = [0]*100
    for i in range(len(res[s])):
        r[int(res[s][i][0])] += (res[s][i][3]-res[s][i][2])/1539
        n[int(res[s][i][0])] += 1

    for i in range(len(n)):
        r[i] = r[i]/n[i]

    plt.plot(r[i],label=s)
plt.show()

