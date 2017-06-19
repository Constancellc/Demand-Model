from clustering import Cluster, ClusteringExercise
import random
import matplotlib.pyplot as plt

testData = []
for i in range(0,100):
    point = []
    for j in range(0,10):
        point.append(random.random())
    testData.append(point)

test = ClusteringExercise(testData)
test.k_means(4)
print test.labels
plt.figure(1)
plt.subplot(2,1,1)
for i in range(0,4):
    plt.plot(test.clusters[str(i)].mean)
    
test.reset_clusters()
test.k_means_si(4)
print test.labels
plt.subplot(2,1,2)
for i in range(0,4):
    plt.plot(test.clusters[str(i)].mean)

plt.show()

