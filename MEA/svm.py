import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

stem = '../../Documents/My_Electric_avenue_Technical_Data/training/'

X = []
y = []
with open(stem+'X.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(X) > 1600:
            continue
        p = []
        for cell in row:
            p.append(float(cell))
        X.append(p)

print('got it')
with open(stem+'y.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(y) > 1600:
            continue
        y.append(float(row[0]))

print('got it')
clf = svm.SVR(kernel='linear')
clf.fit(X[:1500], y[:1500])

#y2 = clf.predict(X[1500])

# now to try generating charging profiles from it

usage = X[1525][:48]+X[1535][:48]
charging = [0.0]*47

for t in range(48,98):
    c = clf.predict([usage[t-48:t]+charging[t-48:t-1]])
    charging.append(c)
    
plt.figure()
plt.plot(usage)
plt.plot(charging)
plt.show()
