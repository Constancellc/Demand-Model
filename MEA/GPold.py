import csv
import numpy as np

class Covariance:

    def __init__(self,r,c):
        self.K = np.zeros(r,c)
        self.size = [r,c]

class K_SE(Covariance):

    def __init__(self,h,l):
        self.h = h
        self.l = l

    def updateHypers(self,x):
        self.h = x[0]
        self.l = x[1]

    def single(self,a,b):
        return self.h*self.h*np.exp(-np.power(a-b,2)/(self.l*self.l))

    def value(self,a,b):
        for i in range(len(a)):
            for j in range(i,len(b)):
                self.K[i][j] = self.single(a[i],b[j])
                self.K[j][i] = self.K[i][j]
        return self.K

    def dh(self,a,b):
        

class GaussianProcess:

    def __init__(self,cov):
    
