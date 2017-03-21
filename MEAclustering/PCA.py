import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def PCA(csvfile,per,skipHeader=False):
    
    X = []
    names = []

#with open('scaledAverages.csv','rU') as csvfile:
    with open(csvfile,'rU') as csvfile:
        reader = csv.reader(csvfile)
        if skipHeader == True:
            reader.next()
        for row in reader:
            names.append(row[0])
            point = []
            for i in range(1,len(row)):
                point.append(float(row[i]))
            X.append(point)

    X = np.array(X)

    cov = np.matmul(X.transpose(),X)
    [U,S,V] = np.linalg.svd(cov)

    print S

    s = 0
    i = 0
    while s/sum(S) < per:
        s += S[i]
        i += 1
    print i 
    Z = np.matmul(U[:,:i].T,X.T)

    return Z, X, names

#print Z

#Z = PCA('chargeRLPs.csv',0.99)
#fig = plt.figure(1)
#ax = fig.add_subplot(111)#, projection='3d')
#ax.scatter(Z[0],Z[1])#,Z[2])
#plt.show()
