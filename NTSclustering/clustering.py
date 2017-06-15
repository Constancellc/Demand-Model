import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import sklearn.cluster as clst

def distance_si(x,y):
    if len(x) != len(y):
        raise Exception('two input vectors are different lengths')

    highest = 0
    # first find shift with highest correlation
    for i in range(0,len(x)):
        y2 = y[i:]+y[:i]
        c = 0
        for j in range(0,len(x)):
            c += y2[j]*x[j]

        if c > highest:
            highest = c
            best_y = y2

    diff = 0
    for i in range(0,len(x)):
        d = best_y[i]-x[i]
        diff += d*d
    
class Cluster:

    def __init__(self,cName,mean=None,x0=None,x0name=None):
        
        if mean is None and x0 is None:
            raise Exception('please define either a mean or initial point')
        
        else:
            self.nPoints = 0
            self.points = {}
            self.nFeatures = None # number of features
            
            if mean is not None:
                self.mean = mean
                
            if x0 is not None:
                self.nFeatures = len(x0)
                
                if x0name == None:
                    raise Exception('please name the initial point')
                
                self.nPoints += 1
                self.points[x0name] = x0

    def add_point(self,x,xname):
        
        if self.nFeatures == None:
            self.nFeatures = len(x)
            
        else:
            if len(x) != self.nFeatures:
                raise Exception('new point is the wrong length')
            
        self.points[xname] = x
        self.nPoints += 1

    def update_centroid(self,centroid=None):
        
        if centroid != None:
            self.mean = centroid
            
        else:
            mean = [0.0]*self.nFeatures
            
            for i in self.points:
                for j in range(0,nFeatures):
                    mean[j] += self.points[i][j]/self.nPoints        
            
class ClusteringExercise:

    def __init__(self,data):
        
        self.clusters = {}
        self.points = {}
        self.data = data
        self.labels = ['']*len(data)

    def reset_clusters(self):
        
        self.clusters = {}
        self.labels = ['']*len(self.data)

    def k_means(self,k):

        centroid, label, inertia = clst.k_means(self.data,k)

        # first create the clusters
        for i in range(0,k):
            self.clusters[str(i)] = Cluster(str(i),mean=centroid[i])

        # then add the points to them
        for i in range(0,len(label)):
            self.clusters[str(label[i])].add_point(self.data[i],str(i))
            self.labels[i] = str(label[i])
        
