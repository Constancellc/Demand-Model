import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from cvxopt import matrix, spdiag, solvers, sparse

for i in range(1,2):
    f = open('openDSSprofiles/load_profile_'+str(i)+'.txt')
    data = f.read()
    print data

    results = []
    newDigit = ''
    
    for j in range(0,len(data)):
        if data[j] == '':
            continue
        if data[j-1] == '':
            results.append(newDigit)
            newDigit = ''
        #print data[j]
        newDigit += data[j]

    print results
