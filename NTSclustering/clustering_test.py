from clustering import Cluster, ClusteringExercise
import random

testData = []
for i in range(0,100):
    point = []
    for j in range(0,10):
        point.append(random.random())
    testData.append(point)

test = ClusteringExercise(testData)
test.k_means(4)


