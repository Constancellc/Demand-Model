import random
import scipy.special as sp
import numpy as np
from numpy import log

class Inference:
    def __init__(self,pdf):
        self.pdf = pdf
        self.N = sum(pdf)

        for i in range(len(pdf)):
            self.pdf[i] = self.pdf[i]/self.N

        # find mean
        self.x_ = 0.0
        self.logx_ = 0.0
        for i in range(len(pdf)):
            self.x_ += self.pdf[i]*i
            if i > 0:
                self.logx_ += self.pdf[i]*log(i)
    
    def fit_gamma(self):
        best = None
        highest = -1000000000
        for a in np.arange(0.1,100,0.01):
            f = self.N*((a-1)*self.logx_-log(sp.gamma(a))-a*log(self.x_/a)-a)
            if f > highest:
                highest = f
                best = a

        if best == None:
            print(f)
            
        a = best
        b = self.x_/a

        return [a,b]

    def fit_normal(self):

        sd = 0.0
        for i in range(len(self.pdf)):
            sd += self.pdf[i]*self.N*np.power(i-self.x_,2)
            
        best = None
        lowest = 10000000
        
        for v in np.arange(0.1,3600,0.1):
            f = 0.5*(self.N*log(v)+(1/v)*sd)
            if f < lowest:
                lowest = f
                best = v

        return [self.x_,np.sqrt(best)]
        
