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


theta0 = [1,10]

for i in range(1):
    
    # using 350 random training pts from first 5000 hrs
    chosen = []
    while len(chosen) < 40:
        ran = int(random.random()*200)
        if ran not in chosen:
            chosen.append(ran)
    x_train = []
    y_train = []
    chosen = sorted(chosen)
    for i in range(40):
        x_train.append(x[chosen[i]])
        y_train.append(y[chosen[i]])

    x_train = np.matrix(x_train)
    y_train = np.matrix(y_train)

    '''
    x_train = np.matrix(x[:60])
    y_train = np.matrix(y[:60])
    #theta = [0.193,5.402,0.564]
    '''
    #GP.train(x_train,y_train,theta)
    
    GP = GaussianProcess(TwoPeriodicMult)
    '''
    GP.learn_hyperparameters(x_train,y_train,theta0)
    theta0 = GP.theta
    '''


#'''    

x_train = np.matrix(x[:450])
y_train = np.matrix(y[:450])
x_test = x[450:500]
y_test = y[450:500]
#'''
GP.train(x_train,y_train,[1,0.1,0.1])
test = np.arange(0,500)
[m,var] = GP.predict(np.matrix(test))

u = copy.copy(m)
l = copy.copy(m)
for i in range(len(m)):
    u[i] += 2*np.sqrt(var[i])
    l[i] -= 2*np.sqrt(var[i])


# creating x ticks
x_ticks = []
px = []
for i in range(int(len(test)/48)):
    px.append(48*i+48)
    x_ticks.append('00:00')

'''
plt.figure(1)
plt.plot(test,m)
plt.fill_between(test,u,l,alpha=0.2)
plt.scatter(np.squeeze(np.asarray(x_train)),np.squeeze(np.asarray(y_train)))

'''
plt.figure(1)
plt.subplot(2,1,1)
plt.title('Training')
plt.plot(test[:x_train.size],m[:x_train.size])
plt.fill_between(test[:x_train.size],u[:x_train.size],l[:x_train.size],alpha=0.2)
plt.scatter(np.squeeze(np.asarray(x_train)),np.squeeze(np.asarray(y_train)))

plt.subplot(2,1,2)
plt.title('Testing')
plt.plot(test[x_train.size:],m[x_train.size:],label='Predicted')
plt.fill_between(test[x_train.size:],u[x_train.size:],
                 l[x_train.size:],alpha=0.2)
plt.plot(x_test,y_test,label='Observed')
plt.legend()
'''
#plt.legend()
#plt.ylabel('Power (kW)')
#plt.xlabel('Time')
#plt.xticks(px,x_ticks)
#plt.xlim(0,len(test))
#plt.grid()

#plt.plot(test,u)
#plt.plot(test,l)
#'''
plt.show()

