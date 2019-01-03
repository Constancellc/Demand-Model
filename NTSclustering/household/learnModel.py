import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'

y = []
y_ = []
locs = []
with open(stem+'peaks.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs.append(row[0])
        y.append(100*(float(row[2])-float(row[1]))/float(row[1]))
        y_.append(np.log((float(row[2])-float(row[1]))/float(row[1])))

NTS = {}
with open(stem+'NTSparams.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in locs:
            continue
        NTS[row[0]] = [float(row[1]),float(row[2]),float(row[3]),
                       float(row[4])]

cens = {}
with open(stem+'censusParams.csv','r',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in locs:
            continue
        cens[row[0]] = [float(row[1]),float(row[2])]#,float(row[3])]
        #cens[row[0]] = [float(row[2]),float(row[3])]

X = []
for l in locs:
    X.append(NTS[l]+cens[l])
X = np.array(X)
y = np.array(y)

reg = LinearRegression().fit(X, y)

y2 = reg.predict(X)

e = 0
for i in range(len(y)):
    e += np.power(y2[i]-y[i],2)/len(y)
print(e)


reg = LinearRegression().fit(X, np.array(y_))

y3_ = reg.predict(X)
y3 = []

e2 = 0
for i in range(len(y)):
    y3.append(100*np.power(np.e,y3_[i]))
    e2 += np.power(y3[i]-y[i],2)/len(y)

print(e2)


c = reg.coef_
print(list(c))
with open(stem+'w.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(list(c))

l = []
X_ = []
with open(stem+'lsoaX.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        l.append(row[0])
        p = []
        for i in range(1,len(row)-1):
            p.append(float(row[i]))
        X_.append(p)

yp = reg.predict(X_)

with open(stem+'lsoaPred.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(yp)):
        writer.writerow([l[i],100*np.power(np.e,yp[i])])
plt.figure()
plt.plot(sorted(y))
plt.plot(sorted(y2))
plt.plot(sorted(y3))
plt.show()
