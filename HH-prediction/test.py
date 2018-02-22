from GP import GaussianProcess
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

'''
# using 50 random training pts from first 500 hrs
chosen = []
while len(chosen) < 300:
    ran = int(random.random()*700)
    if ran not in chosen:
        chosen.append(ran)
x_train = []
y_train = []
chosen = sorted(chosen)
for i in range(300):
    x_train.append(x[chosen[i]])
    y_train.append(y[chosen[i]])

x_train = np.matrix(x_train)
y_train = np.matrix(y_train)
'''
x_train = np.matrix(x[:700])
y_train = np.matrix(y[:700])
x_test = x[700:850]
y_test = y[700:850]
#'''
GP = GaussianProcess()
theta = [0.13456641,0.08,0.16965769,1.30353067,0.145682,0.03243102]
GP.train(x_train,y_train,theta)
#GP.learn_hyperparameters(x_train,y_train)
test = np.arange(1,850,1)
[m,var] = GP.predict(np.matrix(test))
'''
u = copy.copy(m)
l = copy.copy(m)
for i in range(len(m)):
    u[i] += 2*np.sqrt(var[i])
    l[i] -= 2*np.sqrt(var[i])
'''

# creating x ticks
x_ticks = []
px = []
for i in range(int(len(test)/48)):
    px.append(48*i+48)
    x_ticks.append('00:00')
plt.figure(1)
plt.plot(test,m,label='Predicted')
plt.plot(x_test,y_test,label='Observed')
plt.legend()
plt.ylabel('Power (kW)')
plt.xlabel('Time')
plt.xticks(px,x_ticks)
plt.xlim(0,len(test))
plt.grid()

#plt.plot(test,u)
#plt.plot(test,l)
plt.scatter(np.squeeze(np.asarray(x_train)),np.squeeze(np.asarray(y_train)))
plt.show()

