import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'

l_ = []
X_ = []
with open(stem+'lsoaX.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        l_.append(row[0])
        p = []
        for i in range(1,len(row)-1):
            p.append(float(row[i]))
        X_.append(p)

ls = []
Xs = []
# also predict increase for transmission while we're at it
with open('../transmission/substation_param.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        ls.append(row[0])
        p = []
        for i in range(1,len(row)-1):
            p.append(float(row[i]))
        Xs.append(p)

        

mu = []
for i in range(6):
    x = []
    for j in range(len(X_)):
        x.append(X_[j][i])
    mu.append(sum(x)/len(x))
si = []
for i in range(6):
    x = []
    for j in range(len(X_)):
        x.append(np.power(X_[j][i]-mu[i],2))
    si.append(np.sqrt(sum(x)/len(x)))
print(mu)
print(si)

for j in range(len(Xs)):
    for i in range(6):
        Xs[j][i] = (Xs[j][i]-mu[i])/si[i]

    
y = []
y_2 = []
y_3 = []
y_ = []
locs = []
with open(stem+'peaks.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs.append(row[0])
        y.append(100*(float(row[2])-float(row[1]))/float(row[1]))
        y_.append(np.log((float(row[2])-float(row[1]))/float(row[1])))


my = sum(y_)/len(y)
x = []
for i in range(len(y)):
    x.append(np.power(y_[i]-my,2))
sy = np.sqrt(sum(x)/len(x))

for i in range(len(y)):
    y_2.append((y_[i]-my)/sy)
print(my)
print(sy)
'''
my = sum(y_)/len(y)
x = []
for i in range(len(y)):
    x.append(np.power(y_[i]-my,2))
sy = np.sqrt(sum(x)/len(x))

for i in range(len(y)):
    y_3.append((y[i]-my)/sy)
print(my)
print(sy)
'''

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
    for i in range(6):
        X[-1][i] = (X[-1][i]-mu[i])/si[i]

    
X = np.array(X)
y = np.array(y)

reg = LinearRegression().fit(X,y_2)

y2 = reg.predict(X)

e = 0
for i in range(len(y)):
    f = y2[i]*sy+my
    e += np.power(100*np.power(np.e,f)-y[i],2)/len(y)
print(e)


reg = LinearRegression().fit(X, np.array(y_))
'''
y3_ = reg.predict(X)
y3 = []

e2 = 0
for i in range(len(y)):
    y3.append(100*np.power(np.e,y3_[i]))
    e2 += np.power(y3[i]-y[i],2)/len(y)

print(e2)
'''


c = reg.coef_
print(list(c))
with open(stem+'w.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(list(c))


for i in range(len(X_)):
    for j in range(6):
        X_[i][j] = (X_[i][j]-mu[j])/si[j]
yp = reg.predict(X_)

with open(stem+'lsoaPred.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(yp)):
        writer.writerow([l_[i],100*np.power(np.e,yp[i]*sy+my)])


        
ys = reg.predict(Xs)
with open('../transmission/substation_predictions.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(ys)):
        writer.writerow([ls[i],100*np.power(np.e,ys[i]*sy+my)])
plt.figure()
plt.plot(sorted(y))
plt.plot(sorted(y2))
plt.plot(sorted(y3))
plt.show()
