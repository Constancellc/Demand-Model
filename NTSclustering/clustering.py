import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import sys
#import sklearn.cluster as clst

sys.path.append('/Users/constance/scikit-learn')
import sklearn.cluster as clst
   
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
                self.nFeatures = len(mean)
                
            if x0 is not None:
                self.nFeatures = len(x0)
                self.mean = x0
                
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

    def remove_point(self,xname):
        try:
            del self.points[xname]
            self.nPoints -= 1
        except:
            raise Exception('I cant find that point to be deleted')

    def remove_all(self):
        self.points = {}

    def update_centroid(self,centroid=None):
        
        if centroid != None:
            self.mean = centroid
            
        else:
            mean = [0.0]*self.nFeatures
            
            for i in self.points:
                for j in range(0,self.nFeatures):
                    mean[j] += self.points[i][j]/self.nPoints

    def update_centroid_si(self):

        mean = [0.0]*self.nFeatures
        x = 0

        for i in self.points:
            if x == 0:
                x = self.points[i]
                for j in range(0,self.nFeatures):
                    mean[j] += x[j]/self.nPoints 
            else:
                y = self.points[i]
            
                # first find shift with highest correlation
                highest = 0
                for j in range(0,self.nFeatures):
                    y2 = y[j:]+y[:j]
                        
                    c = 0
                    for k in range(0,len(x)):
                        c += y2[k]*x[k]

                    if c > highest:
                        highest = c
                        best_y = y2

                for j in range(0,self.nFeatures):
                    mean[j] += best_y[j]/self.nPoints           
            
class ClusteringExercise:

    def __init__(self,data):
        
        self.clusters = {}
        self.points = {}
        self.data = data
        self.labels = ['']*len(data)

    def reset_clusters(self):
        
        self.clusters = {}
        self.labels = ['']*len(self.data)

    def add_to_nearest(self,x,xname):

        current_cluster = self.labels[int(xname)]

        dist = 10000000
        for j in range(0,len(self.clusters)):
            d = distance(x,self.clusters[str(j)].mean)#distance_si(x,self.clusters[str(j)].mean)
            if d < dist:
                dist = d
                nearest = str(j)

        if nearest == self.labels[int(xname)]:
            return False

        else:
            self.clusters[nearest].add_point(x,xname)

            if current_cluster != '':
                self.clusters[current_cluster].remove_point(xname)
            self.labels[int(xname)] = nearest
            return True
        

    def k_means(self,k):

        centroid, label, inertia = clst.k_means(self.data,k)

        # first create the clusters
        for i in range(0,k):
            self.clusters[str(i)] = Cluster(str(i),mean=centroid[i])

        # then add the points to them
        for i in range(0,len(label)):
            self.clusters[str(label[i])].add_point(self.data[i],str(i))
            self.labels[i] = str(label[i])

