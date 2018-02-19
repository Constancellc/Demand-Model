import numpy as np
import scipy.optimize as opt
'''
ok, here is the deal.

I think I want to make a gaussian process class

I definitely want to make a covariance matrix class



'''

class CovMatrix:
    def __init__(self,x1,x2,theta0):
        # storing the hyper-parameters
        self.h1 = theta0[0]
        self.l1 = theta0[1]
        self.h2 = theta0[2]
        self.h3 = theta0[3]
        self.l2 = 48 # 1 day
        self.l3 = 336 # 1 week

        # storing the input vectors
        self.x1 = x1
        self.x2 = x2

        self.n = x1.shape[1]
        self.m = x2.shape[1]

        if self.n == self.m:
            self.square = True
        else:
            self.square = False
            
        self.calc_matrix()
        
    def calc_matrix(self):
        # initialising the matrix
        self.K1 = np.matrix(np.zeros((self.n,self.m)))
        self.K2 = np.matrix(np.zeros((self.n,self.m)))
        self.K3 = np.matrix(np.zeros((self.n,self.m)))

        def se(a,b,h,l):
            return h*h*np.exp(-np.power(a-b,2)/(2*l*l))
        def p(a,b,h,l):
            return h*h*np.exp(-2*np.power(np.sin((a-b)/2)/l,2))

        if self.square is True:
            for i in range(self.n):
                for j in range(self.n):
                    self.K1[i,j] = se(self.x1[0,i],self.x2[0,j],self.h1,self.l1)
                    self.K2[i,j] = p(self.x1[0,i],self.x2[0,j],self.h2,self.l2)
                    self.K3[i,j] = p(self.x1[0,i],self.x2[0,j],self.h3,self.l3)

                    self.K1[j,i] = self.K1[i,j]
                    self.K2[j,i] = self.K2[i,j]
                    self.K3[j,i] = self.K3[i,j]
        else:
            for i in range(self.n):
                for j in range(self.m):
                    self.K1[i,j] = se(self.x1[0,i],self.x2[0,j],self.h1,self.l1)
                    self.K2[i,j] = p(self.x1[0,i],self.x2[0,j],self.h2,self.l2)
                    self.K3[i,j] = p(self.x1[0,i],self.x2[0,j],self.h3,self.l3)

        
        self.K = self.K1+self.K2+self.K3

        self.foundInv = False
        self.foundChol = False

    def update_hyperparameters(self,theta1):

        self.h1 = theta1[0]
        self.l1 = theta1[1]
        self.h2 = theta1[2]
        self.h3 = theta1[3]

        self.calc_matrix()       

    def inv(self,b=[],sigma=0):
        # check square
        if self.square == False:
            raise Exception()

        if sigma > 0:
            self.K += sigma*np.eye(self.n)
        
        if len(b) == 0:
            if self.foundInv == False:
                self.iK = np.linalg.inv(self.K)
                self.foundInv = True
            if sigma > 0:
                self.K -= sigma*np.eye(self.n)
            return self.iK
            
        else:
            '''
            if self.foundInv == False:
                self.iK = np.linalg.inv(self.K)
                self.foundInv = True
            return self.iK*b
            '''
            # cholesky decomposition to speed up inversion
            if self.foundChol == False:
                self.L = np.linalg.cholesky(self.K)
                self.iL = np.linalg.inv(self.L)
                self.iU = np.linalg.inv(self.L.H)
                self.foundChol = True
            if sigma > 0:
                self.K -= sigma*np.eye(self.n)
            return self.iU*self.iL*b

    def det(self):
        return np.linalg.det(self.K)
    
    def set_training_pts(self,y):
        self.y = y

    def f(self,theta):
        mean = theta[0]
        d = self.y-np.matrix([mean]*len(self.y))
        d = d.T

        self.update_hyperparameters(theta[1:])

        f = np.log(self.det()) + d.T*self.inv(d)

        #print(f)
        return f

    def g(self,theta):
        mean = theta[0]
        d = self.y-np.matrix([mean]*len(self.y))
        d = d.T
        
        self.update_hyperparameters(theta[1:])

        # check k(x,x)
        if self.x1.all != self.x2.all:
            raise Exception()
        
        g = [0.0]*5

        dKdh1 = 2*self.K1/self.h1
        dKdh2 = 2*self.K2/self.h2
        dKdh3 = 2*self.K3/self.h3
        
        dKdl1 = np.matrix(np.zeros((self.n,self.m)))
        for i in range(self.n):
            for j in range(self.m):
                dKdl1[i,j] = np.power(self.x1[0,i]-self.x2[0,j],2)*\
                             self.K1[i,j]/np.power(self.l1,3)
                dKdl1[j,i] = dKdl1[i,j]

        g[0] = -2*self.inv(d)[0,0]
        g[1] = (np.trace(self.inv(dKdh1))-d.T*self.inv(dKdh1)*self.inv(d))[0,0]
        g[2] = (np.trace(self.inv(dKdl1))-d.T*self.inv(dKdl1)*self.inv(d))[0,0]
        g[3] = (np.trace(self.inv(dKdh2))-d.T*self.inv(dKdh2)*self.inv(d))[0,0]
        g[4] = (np.trace(self.inv(dKdh3))-d.T*self.inv(dKdh3)*self.inv(d))[0,0]

        #print(g)                       
        return g

    def check_derivatives(self,theta):
        f0 = self.f(theta)
        g0 = self.g(theta)
        for i in range(len(theta)):
            theta[i] += 0.001
            f = self.f(theta)
            theta[i] -= 0.001
            print('Checking gradient '+str(i+1))
            print(g0[i])
            print((f-f0)/0.001)
            
                
class GaussianProcess:
    def __init__(self):
        self.theta = None
        self.x = None
        self.y = None

    def learn_hyperparameters(self,x,y,theta0=['',2,0.1,3,4]):
        # check length of x and y the same

        self.x = x
        self.y = y.T

        # set inital mean estimate to the average
        if theta0[0] == '':
            n = x.size
            theta0[0] = 0
            for i in range(n):
                theta0[0] += y[0,i]/n
        self.cov = CovMatrix(x,x,theta0)
        self.cov.set_training_pts(y)

        # manually adding noise
        #self.cov.K = self.cov.K + 1e-3*np.eye(self.cov.n)
        #self.cov.check_derivatives(theta0)
        self.theta = opt.fmin_tnc(self.cov.f,theta0,fprime=self.cov.g,
                                  bounds=[[0.01,5]]*5)[0]
        print(self.theta)
        self.cov.update_hyperparameters(self.theta[1:])

    def train(x,y,theta0=[1.0]*5):
        self.x = x
        self.y = y

        if self.theta is None:
            print('need to learn hyperparameters first')
        # set up covariance matrix of right size
        self.cov = CovMatrix(x,x,self.theta)

    def predict(self,x_):
        m = np.matrix([self.theta[0]]*x_.size).T
        d = self.y-np.matrix([self.theta[0]]*self.y.size).T
        K2 = CovMatrix(x_,self.x,self.theta)
        m += K2.K*self.cov.inv(d,sigma=1e-3)

        cov = CovMatrix(x_,x_,self.theta).K-K2.K*self.cov.inv(K2.K.T,sigma=1e-3)
        var = np.diag(cov)
        m = np.squeeze(np.asarray(m))
        return [m,var]
