import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from cvxopt import matrix, spdiag, solvers, sparse

t = 3
t0 = 1
m = 3

A1 = matrix(0.0,(m,(t-t0)*m))
A2 = matrix(0.0,(m,(t-t0)*m))
b = matrix(0.0,(2*m,1))

for j in range(0,m):
    b[j] = 1.0 
    for i in range(0,t-t0):
        A1[m*((t-t0)*j+i)+j] = 2.0
        if i > (3-t0) or i == (t-t0-1):
            A2[m*((t-t0)*j+i)+j] = 1.0


print A2
print A1
        
