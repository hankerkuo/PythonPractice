import numpy as np
import matplotlib.pyplot
from sklearn.datasets.samples_generator import make_blobs
import argparse

def sigmoid_transition(x):
    return 1/(1+np.exp(-x))

(X, y) = make_blobs(n_samples = 10, n_features = 2, centers = 2, cluster_std = 2, random_state = 30)
#np.shape returns a array (a, b) that describe the element number in a numpyarray's first and second axis
#This method is to put a X0 in every sample
# X is a 10 x 3(by 2+1) matrix
X = np.c_[np.ones((np.shape(X)[0], 1)), X]
#generate a 1 x np.shape(X)[1] matrix , np.shape(X)[1] is the feature number of X
W = np.random.rand(1,np.shape(X)[1]) * 5
#regression line , it is a 10 x 1 matrix
H_OF_X = np.dot(X, W.T)
H_OF_X = sigmoid_transition(H_OF_X)
#Cost function of a logistic regression
Cost_Function = np.dot(y,np.log(H_OF_X)) + np.dot((1-y), np.log(1-H_OF_X))

a = 0.01
gradient =
print(y)
print(Cost_Function)


# 10 2 2 20 10 2
