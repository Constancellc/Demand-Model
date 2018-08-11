import csv
import numpy as np
import numpy.linalg as lin
import random

class K_SE():

    def __init__(self,X,y,h,l):
        self.h = h
        self.l = l
        self.X = X
        self.y = y
        self.K = self.calculate(X,X)

    def single(self,a,b):
        return self.h*self.h*np.exp(-np.power(a-b,2)/(self.l*self.l))

    def calculate(self,a,b):
        K = np.zeros((len(a),len(b)))
        for i in range(len(a)):
            for j in range(len(b)):
                K[i][j] = self.single(a[i],b[j])
        return K

    def updateHypers(self,theta):
        self.h = theta[0]
        self.l = theta[1]
        self.K = self.calculate(self.X,self.X)

    def lInv(self,b):
        L = lin.cholesky(self.K)
        return lin.solve(L.T,lin.solve(L,b))

    def predict(self,x_):
        d = self.y # zero mean
        K_ = self.calculate(x_,self.X)
        return np.matmul(K_,self.lInv(d))

class K_mult_SE():

    def __init__(self,X,h1,h2,l,alpha):
        # I actually need to do some thinking about whether we should use the
        # same or different h and l for the streams. Probs different tbh

        # also, have i decided what we are actually predicting (hh or charging)

        # another thought - the x values for all of my training pts will be
        # duplicates. Is this a problem? It should simplify computation...
        self.h1 = h1
        self.h2 = h2
        self.alpha = alpha
        self.l = l
        self.X = X
        #self.y = y
        #self.y1 = y1
        #self.y2 = y2
        self.K = self.calculate(X,X)

    def calculate(self,a,b):
        self.K0 = K_SE(self.X,None,1,self.l).calculate(a,b)
        K = np.concatenate((np.concatenate(\
            (self.h1*self.h1*self.K0,self.alpha*self.h1*self.h2*self.K0),
            axis=1),np.concatenate(\
            (self.alpha*self.h1*self.h2*self.K0,self.h2*self.h2*self.K0),
            axis=1)),axis=0)
        return K

    def updateHypers(self,x):
        self.h1 = x[0]
        self.h2 = x[1]
        self.alpha = x[2]
        self.l = x[4]
        self.K = self.calculate(self.X,self.X)

    def lInv(self,A,b):
        L = lin.cholesky(A)
        return lin.solve(L.T,lin.solve(L,b))

    def predict1given2(self,y1):
        # assume that we are only predicting the second series given first
        d = y1 # zero mean
        K_ = self.alpha*self.h1*self.h2*self.K0
        K = self.K0*self.h2*self.h2
        return np.matmul(K_,self.lInv(K,y1))

n = 4
x = np.array(range(n))
y = np.zeros((n,1))
for i in range(n):
    y[i] = random.random()
print(y)
test = K_mult_SE(x,1,2,1,0.3)
print(test.predict1given2(y))
    
