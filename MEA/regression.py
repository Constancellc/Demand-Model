import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

stem = '../../Documents/My_Electric_avenue_Technical_Data/training/'

# ok, trying something simpler - just a linear relationship

X = []
with open(stem+'X.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        p = []
        for i in range(len(row)):
            p.append(float(row[i]))
        X.append(p)
xPredicted = np.array([X[-1]])
X = np.array(X[:5000])


y = []
with open(stem+'y.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        p = []
        for i in range(len(row)):
            p.append(float(row[i]))
        y.append(p)
yTrue = np.array(y[-1])
y = np.array(y[:5000])


# scale units
X = normalize(X, axis=1, norm='max')
xPredicted = xPredicted / np.amax(xPredicted)

class Network():
    def __init__(self):
        self.inputSize = 48
        self.outputSize = 48
        self.W = np.random.randn(self.inputSize,self.outputSize)

    def sigmoid(self, s):
        # activation function
        return 1 / (1 + np.exp(-s))

    def sigmoidPrime(self, s):
        #derivative of sigmoid
        return s * (1 - s)
    
    def forward(self, X):
        self.z = np.dot(X,self.W)
        o = self.sigmoid(self.z)

        return o

    def backward(self, X, y, o):
        # backward propgate through the network
        self.o_error = y - o  # error in output
        self.o_delta = self.o_error*self.sigmoidPrime(o)  # applying derivative of sigmoid to error
        self.W += X.T.dot(self.o_delta)
        
    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    def saveWeights(self):
        np.savetxt("w.txt", self.W, fmt="%s")

    def predict(self):
        print("Predicted data based on trained weights: ")
        print("Input (scaled): \n" + str(xPredicted))
        print("Output: \n" + str(self.forward(xPredicted)))
 

NN = Network()
for i in range(10000):  # trains the NN 100,000 times
    if i in [0,999,9999]:
        print(" #" + str(i) + "\n")
        print("Loss: \n" + str(np.mean(
            np.square(y - NN.forward(X)))))  # mean sum squared loss
        print("\n")
    NN.train(X, y)

NN.saveWeights()
NN.predict()
