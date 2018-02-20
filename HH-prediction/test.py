from GP import GaussianProcess
import numpy as np
import matplotlib.pyplot as plt
import copy
import csv

#'''

x = []
y = []
with open('../../Documents/sharonb/7591/csv/5110.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x.append(float(row[0]))
        y.append(float(row[1]))
        
x_train = np.matrix(x[:50])
y_train = np.matrix(y[:50])
#'''
GP = GaussianProcess()
#GP.train(np.matrix(range(10)),np.matrix([0.2,0.3]*5),[0.3,1.3,4,0.5,0.2])
GP.learn_hyperparameters(x_train,y_train)
test = np.arange(1,10,0.1)
[m,var] = GP.predict(np.matrix(test))

u = copy.copy(m)
l = copy.copy(m)
for i in range(len(m)):
    u[i] += 2*np.sqrt(var[i])
    l[i] -= 2*np.sqrt(var[i])
    
plt.figure(1)
plt.plot(test,m)
plt.plot(test,u)
plt.plot(test,l)
plt.scatter(np.squeeze(np.asarray(x_train)),np.squeeze(np.asarray(y_train)))
plt.show()

