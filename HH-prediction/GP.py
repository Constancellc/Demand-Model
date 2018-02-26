import numpy as np
import scipy.optimize as opt
'''
ok, here is the deal.

I think I want to make a gaussian process class

I definitely want to make a covariance matrix class



'''

def se(a,b,h,l):
    return h*h*np.exp(-np.power(a-b,2)/(2*l*l))
def p(a,b,h,l,omega):
    return h*h*np.exp(-2*np.power(np.sin((omega*(a-b))/2)/l,2))

class CovMatrix:
    def __init__(self,x1,x2,theta,func):
        # storing the hyper-parameters
        self.theta = theta

        # storing the input vectors
        self.x1 = x1
        self.x2 = x2

        self.n = x1.shape[1]
        self.m = x2.shape[1]

        if self.n == self.m:
            self.square = True
        else:
            self.square = False

        self.func = func
        self.calc_matrix()
        
    def calc_matrix(self):
        # initialising the matrix
        self.K = np.matrix(np.zeros((self.n,self.m)))

        if self.square is True:
            for i in range(self.n):
                for j in range(self.n):
                    self.K[i,j] = self.func(self.x1[0,i],self.x2[0,j])

                    self.K[j,i] = self.K[i,j]
        else:
            for i in range(self.n):
                for j in range(self.m):
                    self.K[i,j] = self.func(self.x1[0,i],self.x2[0,j])

        self.foundInv = False
        self.foundChol = False

    def add_noise(self,sigma):

        if self.square == False:
            return ''

        else:
            self.K += sigma*np.eye(self.n)

    #def update_hyperparameters(self,theta1):

        #self.theta = theta1
        #self.calc_matrix()       

    def inv(self,b=[],sigma=0):
        # check square
        if self.square == False:
            raise Exception()
        
        if len(b) == 0:
            if self.foundInv == False:
                self.iK = np.linalg.inv(self.K)
                self.foundInv = True
            return self.iK
            
        else:
            # cholesky decomposition to speed up inversion
            if self.foundChol == False:
                self.L = np.linalg.cholesky(self.K)
                self.iL = np.linalg.inv(self.L)
                self.iU = np.linalg.inv(self.L.H)
                self.foundChol = True
                
            if len(b) == 1:
                return self.iU*self.iL*b.T
            else:
                return self.iU*self.iL*b

    def det(self):
        return np.linalg.det(self.K)
    
    def set_training_pts(self,y):
        self.y = y

        d = []
        mean = 0
        for i in range(y.size):
            mean += y[0,i]/y.size
        for i in range(y.size):
            d.append(y[0,i]-mean)
        self.d = np.matrix(d).T

    def f(self,theta):

        self.update_hyperparameters(theta)
        self.add_noise(1e-5)

        f = np.log(self.det()) + self.d.T*self.inv(self.d)

        return f

    def check_derivatives(self,theta):
        f0 = self.f(theta)
        g0 = self.g(theta)
        for i in range(len(theta)):
            theta[i] += 0.000001
            f = self.f(theta)
            theta[i] -= 0.000001
            print('Checking gradient '+str(i+1))
            print(g0[i])
            print((f-f0)/0.000001)

class Periodic(CovMatrix):

    def __init__(self,x1,x2,theta):
        self.h = theta[0]
        self.l = theta[1]
        
        self.T = 48
        self.omega = 2*np.pi/self.T

        def func(a,b):
            return p(a,b,self.h,self.l,self.omega)
        
        CovMatrix.__init__(self,x1,x2,theta,func)


    def update_hyperparameters(self,theta1):
        
        self.h = theta1[0]
        self.l = theta1[1]
        
        def func(a,b):
            return p(a,b,self.h,self.l,self.omega)
        
        self.func = func
        self.calc_matrix()
        
    def g(self,theta):
        
        self.update_hyperparameters(theta)
        self.add_noise(1e-5)

        # check k(x,x)
        if self.x1.all != self.x2.all:
            raise Exception()
        
        g = [0.0]*len(theta)

        dKdh = 2*self.K/theta[0]
        dKdl = np.matrix(np.zeros((self.n,self.m)))
        for i in range(self.n):
            for j in range(self.m):
                dij = self.x1[0,i]-self.x2[0,j]
                dKdl[i,j] = np.power(2*np.sin(dij*self.omega/2),2)*self.K[i,j]\
                            /np.power(self.l,3)
                dKdl[j,i] = dKdl[i,j]
                
        g[0] = (np.trace(self.inv(dKdh))-self.d.T*self.inv(dKdh)*self.inv(self.d))[0,0]
        g[1] = (np.trace(self.inv(dKdl))-self.d.T*self.inv(dKdl)*self.inv(self.d))[0,0] 
                    
        return g

'''

class CovMatrix3:
    def __init__(self,x1,x2,theta0):
        # storing the hyper-parameters
        self.h1 = theta0[0]
        self.l1 = theta0[1]
        self.h2 = theta0[2]
        self.l2 = theta0[3]
        self.h3 = theta0[4]
        self.l3 = theta0[5] 

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

        if self.square is True:
            for i in range(self.n):
                for j in range(self.n):
                    self.K1[i,j] = se(self.x1[0,i],self.x2[0,j],self.h1,self.l1)
                    self.K2[i,j] = p(self.x1[0,i],self.x2[0,j],self.h2,self.l2,
                                     2*np.pi/48) # one day
                    self.K3[i,j] = p(self.x1[0,i],self.x2[0,j],self.h3,self.l3,
                                     2*np.pi/336) # one week

                    self.K1[j,i] = self.K1[i,j]
                    self.K2[j,i] = self.K2[i,j]
                    self.K3[j,i] = self.K3[i,j]
        else:
            for i in range(self.n):
                for j in range(self.m):
                    self.K1[i,j] = se(self.x1[0,i],self.x2[0,j],self.h1,self.l1)
                    self.K2[i,j] = p(self.x1[0,i],self.x2[0,j],self.h2,self.l2,
                                     2*np.pi/48) # one day)
                    self.K3[i,j] = p(self.x1[0,i],self.x2[0,j],self.h3,self.l3,
                                     2*np.pi/336) # one week

        
        self.K = self.K1+self.K2+self.K3

        self.foundInv = False
        self.foundChol = False

    def add_noise(self,sigma):

        if self.square == False:
            return ''

        else:
            self.K += sigma*np.eye(self.n)

    def update_hyperparameters(self,theta1):

        self.h1 = theta1[0]
        self.l1 = theta1[1]
        self.h2 = theta1[2]
        self.l2 = theta1[3]
        self.h3 = theta1[4]
        self.l3 = theta1[5] 

        self.calc_matrix()       

    def inv(self,b=[],sigma=0):
        # check square
        if self.square == False:
            raise Exception()
        
        if len(b) == 0:
            if self.foundInv == False:
                self.iK = np.linalg.inv(self.K)
                self.foundInv = True
            return self.iK
            
        else:
            # cholesky decomposition to speed up inversion
            if self.foundChol == False:
                self.L = np.linalg.cholesky(self.K)
                self.iL = np.linalg.inv(self.L)
                self.iU = np.linalg.inv(self.L.H)
                self.foundChol = True
                
            if len(b) == 1:
                return self.iU*self.iL*b.T
            else:
                return self.iU*self.iL*b

    def det(self):
        return np.linalg.det(self.K)
    
    def set_training_pts(self,y):
        self.y = y

        d = []
        mean = 0
        for i in range(y.size):
            mean += y[0,i]/y.size
        for i in range(y.size):
            d.append(y[0,i]-mean)
        self.d = np.matrix(d).T

    def f(self,theta):

        self.update_hyperparameters(theta)
        self.add_noise(1e-3)

        f = np.log(self.det()) + self.d.T*self.inv(self.d)

        return f

    def g(self,theta):
        
        self.update_hyperparameters(theta)
        self.add_noise(1e-3)

        # check k(x,x)
        if self.x1.all != self.x2.all:
            raise Exception()
        
        g = [0.0]*6

        dKdh1 = 2*self.K1/self.h1
        dKdh2 = 2*self.K2/self.h2
        dKdh3 = 2*self.K3/self.h3
        
        dKdl1 = np.matrix(np.zeros((self.n,self.m)))
        dKdl2 = np.matrix(np.zeros((self.n,self.m)))
        dKdl3 = np.matrix(np.zeros((self.n,self.m)))
        for i in range(self.n):
            for j in range(self.m):
                dij = self.x1[0,i]-self.x2[0,j]
                dKdl1[i,j] = np.power(dij,2)*self.K1[i,j]/np.power(self.l1,3)
                dKdl1[j,i] = dKdl1[i,j]
                
                dKdl2[i,j] = np.power(2*np.sin(np.pi*dij/48),2)*self.K2[i,j]\
                             /np.power(self.l2,3)
                dKdl2[j,i] = dKdl2[i,j]

                dKdl3[i,j] = np.power(2*np.sin(np.pi*(dij)/336),2)*self.K3[i,j]\
                             /np.power(self.l3,3)
                dKdl3[j,i] = dKdl3[i,j]
        
        g[0] = (np.trace(self.inv(dKdh1))-\
                self.d.T*self.inv(dKdh1)*self.inv(self.d))[0,0]
        g[1] = (np.trace(self.inv(dKdl1))-\
                self.d.T*self.inv(dKdl1)*self.inv(self.d))[0,0]
        g[2] = (np.trace(self.inv(dKdh2))-\
                self.d.T*self.inv(dKdh2)*self.inv(self.d))[0,0]
        g[3] = (np.trace(self.inv(dKdl2))-\
                self.d.T*self.inv(dKdl2)*self.inv(self.d))[0,0]
        g[4] = (np.trace(self.inv(dKdh3))-\
                self.d.T*self.inv(dKdh3)*self.inv(self.d))[0,0]
        g[5] = (np.trace(self.inv(dKdl3))-\
                self.d.T*self.inv(dKdl3)*self.inv(self.d))[0,0]

        #print(g)                       
        return g

    def check_derivatives(self,theta):
        f0 = self.f(theta)
        g0 = self.g(theta)
        for i in range(len(theta)):
            theta[i] += 0.000001
            f = self.f(theta)
            theta[i] -= 0.000001
            print('Checking gradient '+str(i+1))
            print(g0[i])
            print((f-f0)/0.000001)
            
                
class CovMatrix2:
    def __init__(self,x1,x2,theta0):
        # storing the hyper-parameters
        self.h1 = theta0[0]
        self.l1 = theta0[1]
        self.l2 = theta0[2]

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
        self.K = np.matrix(np.zeros((self.n,self.m)))

        if self.square is True:
            for i in range(self.n):
                for j in range(self.n):
                    self.K[i,j] = se(self.x1[0,i],self.x2[0,j],self.h1,self.l1)*\
                                  p(self.x1[0,i],self.x2[0,j],1,self.l2,
                                     2*np.pi/48)

                    self.K[j,i] = self.K[i,j]
        else:
            for i in range(self.n):
                for j in range(self.m):
                    self.K[i,j] = se(self.x1[0,i],self.x2[0,j],self.h1,self.l1)*\
                                  p(self.x1[0,i],self.x2[0,j],1,self.l2,
                                     2*np.pi/48)

        self.foundInv = False
        self.foundChol = False

    def add_noise(self,sigma):

        if self.square == False:
            return ''

        else:
            self.K += sigma*np.eye(self.n)

    def update_hyperparameters(self,theta1):

        self.h1 = theta1[0]
        self.l1 = theta1[1]
        self.l2 = theta1[2]

        self.calc_matrix()       

    def inv(self,b=[],sigma=0):
        # check square
        if self.square == False:
            raise Exception()
        
        if len(b) == 0:
            if self.foundInv == False:
                self.iK = np.linalg.inv(self.K)
                self.foundInv = True
            return self.iK
            
        else:
            # cholesky decomposition to speed up inversion
            if self.foundChol == False:
                self.L = np.linalg.cholesky(self.K)
                self.iL = np.linalg.inv(self.L)
                self.iU = np.linalg.inv(self.L.H)
                self.foundChol = True
                
            if len(b) == 1:
                return self.iU*self.iL*b.T
            else:
                return self.iU*self.iL*b

    def det(self):
        return np.linalg.det(self.K)
    
    def set_training_pts(self,y):
        self.y = y

        d = []
        mean = 0
        for i in range(y.size):
            mean += y[0,i]/y.size
        for i in range(y.size):
            d.append(y[0,i]-mean)
        self.d = np.matrix(d).T

    def f(self,theta):

        self.update_hyperparameters(theta)
        self.add_noise(1e-5)

        f = np.log(self.det()) + self.d.T*self.inv(self.d)

        return f

    def g(self,theta):
        
        self.update_hyperparameters(theta)
        self.add_noise(1e-5)

        # check k(x,x)
        if self.x1.all != self.x2.all:
            raise Exception()
        
        g = [0.0]*3

        dKdh1 = 2*self.K/self.h1
        
        dKdl1 = np.matrix(np.zeros((self.n,self.m)))
        dKdl2 = np.matrix(np.zeros((self.n,self.m)))
        
        for i in range(self.n):
            for j in range(self.m):
                dij = self.x1[0,i]-self.x2[0,j]
                dKdl1[i,j] = np.power(dij,2)*self.K[i,j]/np.power(self.l1,3)
                dKdl1[j,i] = dKdl1[i,j]
                
                dKdl2[i,j] = np.power(2*np.sin(np.pi*dij/48),2)*self.K[i,j]\
                             /np.power(self.l2,3)
                dKdl2[j,i] = dKdl2[i,j]
        
        g[0] = (np.trace(self.inv(dKdh1))-\
                self.d.T*self.inv(dKdh1)*self.inv(self.d))[0,0]
        g[1] = (np.trace(self.inv(dKdl1))-\
                self.d.T*self.inv(dKdl1)*self.inv(self.d))[0,0]
        g[2] = (np.trace(self.inv(dKdl2))-\
                self.d.T*self.inv(dKdl2)*self.inv(self.d))[0,0]
                      
        return g

    def check_derivatives(self,theta):
        f0 = self.f(theta)
        g0 = self.g(theta)
        for i in range(len(theta)):
            theta[i] += 0.000001
            f = self.f(theta)
            theta[i] -= 0.000001
            print('Checking gradient '+str(i+1))
            print(g0[i])
            print((f-f0)/0.000001)
            
'''
            
                
class GaussianProcess:
    def __init__(self,CType):
        self.mean = 0.0
        self.theta = None
        self.x = None
        self.y = None
        self.CType = CType

    def learn_hyperparameters(self,x,y,theta0):
        # check length of x and y the same

        self.x = x
        self.y = y

        # set mean to average observed value
        self.mean = 0
        for i in range(y.size):
            self.mean += y[0,i]/y.size

        self.cov = self.CType(self.x,self.x,theta0)

        self.cov.add_noise(1e-5)
        self.cov.set_training_pts(y)

        self.cov.check_derivatives(theta0)
        self.theta = opt.fmin_tnc(self.cov.f,theta0,fprime=self.cov.g,
                                  bounds=[[0.01,200]]*len(theta0))[0]
 
        print(self.theta)
        self.cov.update_hyperparameters(self.theta)
        self.cov.add_noise(1e-5)

    def train(self,x,y,theta0=None):
        self.x = x
        self.y = y
        
        # set mean to average observed value
        self.mean = 0
        for i in range(y.size):
            self.mean += y[0,i]/y.size

        self.theta = theta0

        if self.theta is None:
            print('need to learn hyperparameters first')
        # set up covariance matrix of right size
        self.cov = self.CType(x,x,self.theta)

    def predict(self,x_):
        m = np.matrix([self.theta[0]]*x_.size).T
        d = self.y-np.matrix([self.theta[0]]*self.y.size)
        K2 = self.CType(x_,self.x,self.theta)
        m += K2.K*self.cov.inv(d)

        cov = self.CType(x_,x_,self.theta).K-K2.K*self.cov.inv(K2.K.T)
        var = np.diag(cov)
        
        m = np.squeeze(np.asarray(m))
        return [m,var]
