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

    def get_centroid_median(self):
        # find the point nearest to the centroid

        nearest = 10000000
        median = None
        
        for i in self.points:
            dist = np.linalg.norm(np.array(self.points[i])-\
                                     np.array(self.mean))
            if dist < nearest:
                median = self.points[i]

        return median
            

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
                    
    def get_cluster_bounds(self,conf=0.95):

        per = (1.0-conf)/2
        upper = []
        lower = []

        N = len(self.points)
        u_lim = int(N*(1.0-per))
        l_lim = int(N*per)

        for j in range(0,48):
            p = []
            
            for i in self.points:
                p.append(self.points[i][j])

            p = sorted(p)

            upper.append(p[u_lim])
            lower.append(p[l_lim])

        return upper, lower

    def get_av_distance(self,maxScale,nDays):

        totalDist = 0.0
        nVehicles = len(self.points)

        for i in self.points:
            totalDist += sum(np.array(self.points[i]))/nDays

        return int(totalDist*maxScale/nVehicles)

    def get_sum_of_squares(self):

        total = 0.0

        for i in self.points:
            for p in range(len(self.mean)):
                d = self.mean[p]-self.points[i][p]
                total += d*d

        return total
        
            
            
class ClusteringExercise:

    def __init__(self,data):
        
        self.clusters = {}
        self.points = {}
        self.data = data
        self.labels = ['']*len(data)

    def get_overall_mean(self):
        mean = [0.0]*len(self.data[0])

        for i in range(len(self.data)):
            for j in range(len(mean)):
                mean[j] += self.data[i][j]/len(self.data)

        return mean

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

    def find_nearest(self,x):

        dist = 1000000
        for j in range(0,len(self.clusters)):
            d = 0
            for i in range(len(x)):
                d += np.power(x[i]-self.clusters[str(j)].mean[i],2)
            if d < dist:
                dist = d
                nearest = str(j)

        return nearest

    def k_means(self,k):

        centroid, label, inertia = clst.k_means(self.data,k)

        # first create the clusters
        for i in range(0,k):
            self.clusters[str(i)] = Cluster(str(i),mean=centroid[i])

        # then add the points to them
        for i in range(0,len(label)):
            self.clusters[str(label[i])].add_point(self.data[i],str(i))
            self.labels[i] = str(label[i])

    def get_cluster_median(self):
        medians = {}
        for cluster in self.clusters:
            medians[cluster] = self.clusters[cluster].get_centroid_median()

        return medians

    def get_sum_of_squares(self):
        n = 0
        total = 0.0
        for cluster in self.clusters:
            total += self.clusters[cluster].get_sum_of_squares()
            n += 1

        return total/n

    def get_per_explained_var(self):
        exp = 0

        mean = self.get_overall_mean()

        for cluster in self.clusters:
            centroid = self.clusters[cluster].mean
            for i in range(len(mean)):
                d = centroid[i]-mean[i]
                exp += d*d*self.clusters[cluster].nPoints

        exp = exp#/(len(self.clusters)-1)

        unexp = 0

        for cluster in self.clusters:
            unexp += self.clusters[cluster].get_sum_of_squares()

        unexp = unexp#/(len(self.data)-len(self.clusters))

        return exp/unexp

    def get_dist_closest_centroids(self):

        closest = 1

        for i in self.clusters:
            for j in self.clusters:
                if i == j:
                    continue
                d = 0
                for p in range(len(self.data[0])):
                    d += np.power(self.clusters[i].mean[p]-\
                                  self.clusters[j].mean[p],2)
                if d < closest:
                    closest = d

        return closest
        
            

