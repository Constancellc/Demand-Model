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
        if len(X) > 16000:
            continue
        p = []
        for cell in row:
            p.append(float(cell))
        X.append(p)

print('got it')
with open(stem+'y.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(y) > 16000:
            continue
        y.append(float(row[0]))

print('got it')
clf = svm.SVR()#kernel='linear')
clf.fit(X[:5500], y[:5500])
'''
y2 = clf.predict(X[1500:])
plt.figure()
plt.plot(y[1500:])
plt.plot(y2)
plt.show()
'''
# now to try generating charging profiles from it

usage = X[5505][:48]+X[5570][:48]
charging = [0.0]*47

for t in range(48,96):
    c = clf.predict([usage[t-48:t]+charging[t-48:t-1]])
    charging.append(c)
    
plt.figure()
plt.plot(usage)
plt.plot(charging)
plt.show()
#'''
