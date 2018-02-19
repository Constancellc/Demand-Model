from GP import GaussianProcess
import numpy as np
import matplotlib.pyplot as plt
import copy

GP = GaussianProcess()
x = np.matrix([2,4,6])
y = np.matrix([1,2,1])#,0.5,1.4,2,0,0.2])
GP.learn_hyperparameters(x,y)
[m,var] = GP.predict(np.matrix(range(9)))

u = copy.copy(m)
l = copy.copy(m)
for i in range(len(m)):
    u[i] += var[i]
    l[i] -= var[i]
    
plt.figure(1)
plt.plot(m)
plt.plot(u)
plt.plot(l)
plt.scatter(np.squeeze(np.asarray(x)),np.squeeze(np.asarray(y)))
plt.show()
