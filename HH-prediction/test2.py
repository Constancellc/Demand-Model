from GP import GaussianProcess, Periodic, TwoPeriodicMult
import numpy as np
import matplotlib.pyplot as plt
import copy
import csv
import random
#'''

x = []
y = []
with open('../../Documents/sharonb/7591/csv/5110.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x.append(float(row[0]))
        y.append(float(row[1]))


x_train = np.matrix([1,2,4,6])
y_train = np.matrix([2.1,2.3,1.8,2.0])
#'''
GP = GaussianProcess(Periodic)
#theta = [0.13456641,0.08,0.16965769,1.30353067,0.145682,0.03243102]
#GP.train(x_train,y_train,theta)
GP.learn_hyperparameters(x_train,y_train,[1]*2)
#hp = GP.cov.map_likelihood(0.1,20,0.1,0.1,20,0.1)
#plt.figure(1)
#plt.imshow(hp)
#plt.show()
test = np.arange(0,8,0.1)
[m,var] = GP.predict(np.matrix(test))

u = copy.copy(m)
l = copy.copy(m)
for i in range(len(m)):
    u[i] += 2*np.sqrt(var[i])
    l[i] -= 2*np.sqrt(var[i])

    
plt.figure(1)
plt.plot(test,m)
plt.fill_between(test,u,l,alpha=0.2)
plt.scatter(np.squeeze(np.asarray(x_train)),np.squeeze(np.asarray(y_train)))

plt.show()

