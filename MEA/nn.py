import numpy as np
import csv
from sklearn.preprocessing import normalize

stem = '../../Documents/My_Electric_avenue_Technical_Data/training/'

X = []
with open(stem+'X.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        p = []
        for i in range(len(row)):
            p.append(float(row[i]))
        X.append(p)
xPredicted = np.array([X[-1]])
X = np.array(X[:10])


y = []
with open(stem+'y.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        p = []
        for i in range(len(row)):
            p.append(float(row[i]))
        y.append(p)
y = np.array(y[:10])
print(X)

'''
X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)

y = np.array(([92], [100], [89]), dtype=float)

xPredicted = np.array(([4, 8]), dtype=float)
'''

# scale units
X = normalize(X, axis=0, norm='max')
'''
X = X / np.amax(X, axis=0)  # maximum of X array
print(np.amax(X, axis=1))
xPredicted = xPredicted / np.amax(
    xPredicted)#axis=0)  # maximum of xPredicted (our input data for the prediction)
#y = y / 100  # max test score is 100
'''
print(X)
class Neural_Network(object):
    def __init__(self):
        #parameters
        self.inputSize = 48
        self.outputSize = 48
        self.hiddenSize = 3

        #weights
        self.W1 = np.random.randn(
            self.inputSize,
            self.hiddenSize)  # (3x2) weight matrix from input to hidden layer
        self.W2 = np.random.randn(
            self.hiddenSize,
            self.outputSize)  # (3x1) weight matrix from hidden to output layer

    def forward(self, X):
        #forward propagation through our network
        self.z = np.dot(
            X,
            self.W1)  # dot product of X (input) and first set of 3x2 weights
        self.z2 = self.sigmoid(self.z)  # activation function
        self.z3 = np.dot(
            self.z2, self.W2
        )  # dot product of hidden layer (z2) and second set of 3x1 weights
        o = self.sigmoid(self.z3)  # final activation function
        return o

    def sigmoid(self, s):
        # activation function
        return 1 / (1 + np.exp(-s))

    def sigmoidPrime(self, s):
        #derivative of sigmoid
        return s * (1 - s)

    def backward(self, X, y, o):
        # backward propgate through the network
        self.o_error = y - o  # error in output
        self.o_delta = self.o_error * self.sigmoidPrime(
            o)  # applying derivative of sigmoid to error

        self.z2_error = self.o_delta.dot(
            self.W2.T
        )  # z2 error: how much our hidden layer weights contributed to output error
        self.z2_delta = self.z2_error * self.sigmoidPrime(
            self.z2)  # applying derivative of sigmoid to z2 error

        self.W1 += X.T.dot(
            self.z2_delta)  # adjusting first set (input --> hidden) weights
        self.W2 += self.z2.T.dot(
            self.o_delta)  # adjusting second set (hidden --> output) weights

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    def saveWeights(self):
        np.savetxt("w1.txt", self.W1, fmt="%s")
        np.savetxt("w2.txt", self.W2, fmt="%s")

    def predict(self):
        print("Predicted data based on trained weights: ")
        print("Input (scaled): \n" + str(xPredicted))
        print("Output: \n" + str(self.forward(xPredicted)))


NN = Neural_Network()
for i in range(10000):  # trains the NN 1,000 times
    '''
    print(" #" + str(i) + "\n")
    print("Input (scaled): \n" + str(X))
    print("Actual Output: \n" + str(y))
    print("Predicted Output: \n" + str(NN.forward(X)))
    print("Loss: \n" + str(np.mean(
        np.square(y - NN.forward(X)))))  # mean sum squared loss
    print("\n")
    '''
    NN.train(X, y)

NN.saveWeights()
NN.predict()
