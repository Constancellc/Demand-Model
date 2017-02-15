import numpy as np
import matplotlib.pyplot as plt
import random
import csv

from cvxopt import matrix, spdiag, solvers, sparse

n = 2
t = 4

A2 = matrix(0.0,(n,t*n))

for j in range(0,n):
    for i in range(0,t):
        A2[n*i+j*(t*n+1)] = 1.0
        if i < 2:
            continue


print A2
