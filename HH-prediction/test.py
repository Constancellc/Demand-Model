from GP import GaussianProcess
import numpy as np


GP = GaussianProcess()
x = np.matrix(range(9))
y = np.matrix([0.1,-0.9,0.95]*3)#,0.5,1.4,2,0,0.2])
GP.learn_hyperparameters(x,y)
