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

    return diff

def distance(x,y):
    
    if len(x) != len(y):
        raise Exception('two input vectors are different lengths')

    diff = 0
    for i in range(0,len(x)):
        d = x[i]-y[i]
        diff += d*d

    return diff

    
    
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

    def DB_scan(self):

        db = clst.DBSCAN().fit(self.data)

        label = db.labels_
        n_clusters_ = len(set(label))

        print n_clusters_

        for i in range(0,len(label)):
            self.labels[i] = str(label[i])
            
            if str(label[i]) not in self.clusters:
                print label[i]
                self.clusters[str(label[i])] = Cluster(str(label[i]),
                                                       x0=self.data[i],
                                                       x0name=str(i))
            else:
                self.clusters[str(label[i])].add_point(self.data[i],str(i))

        for label in self.clusters:
            self.clusters[label].update_centroid()

    def k_means_si(self,k):

        # first initiate clusters
        rn = int(random.random()*len(self.data)/k)
        for i in range(0,k):
            self.clusters[str(i)] = Cluster(str(i),mean=self.data[i*rn])

        data_subset = []

        for i in range(0,len(self.data)):
            if random.random() < 1:#0.0005:
                data_subset.append(self.data[i])

        # assign all points to clusters
        for i in range(0,len(data_subset)):
            self.add_to_nearest(data_subset[i],str(i))

        # update the mean values of all clusters
        for i in range(0,k):
            self.clusters[str(i)].update_centroid()

        loop = True

        while loop is True:

            pointsMoving = 0

            # now i need to find the points which want to move cluster
            for i in range(0,len(data_subset)):
                moved = self.add_to_nearest(data_subset[i],str(i))

                if moved is True:
                    pointsMoving += 1

            if pointsMoving == 0:
                loop = False
            else:
                print pointsMoving,
                print 'points moved'

            # update the mean values of all clusters
            for i in range(0,k):
                self.clusters[str(i)].update_centroid()

        # once clusters chosen assign all points to a cluster
        for i in range(0,k):
            self.clusters[str(i)].remove_all()
        self.labels = ['']*len(self.data)

        for i in range(0,len(self.data)):
            self.add_to_nearest(self.data[i],str(i))
            
        
                
