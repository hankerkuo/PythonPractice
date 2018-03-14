import numpy as np
import matplotlib.pyplot
from sklearn.datasets.samples_generator import make_blobs
import argparse

def sigmoid_transition(x):
    return 1/(1+np.exp(-x))
def error_rate(error_times, sample_number):
    return error_times / sample_number * 100

error = 0
(X, y) = make_blobs(n_samples = 1000, n_features = 2, centers = 2, cluster_std = 1.3, random_state = 20)
'''
This make_blobs will produce a matrix X like this:
 [X1.feature(1) X1.feature(2)
      ...           ...
  Xm.feature(1) Xm.feature(2)]
  
 And also produce a matrix y like this:
 [y1
  ..
  ym]
  where y is made for every sample 1~m, y has value of either 1 or 0 
'''
m = np.shape(X)[0]
n = np.shape(X)[1]
#np.shape returns a array (a, b) that describe the element number in a numpyarray's first and second axis

X = np.c_[np.ones((m, 1)), X]
#This method is to put a X0 in every sample, X is a m * (n+1) matrix

W = np.random.rand(1, n+1) * 5
#generate a 1 * (n+1) matrix , n is the feature number of X
Cost_Function = np.zeros((m, 1))


for i in range(1000):
    H_OF_X = np.dot(X, W.T)
    H_OF_X = sigmoid_transition(H_OF_X)
    # regression line , it is a 10 x 1 matrix

    a = 0.5
    gradient = (1 / m) * np.dot((H_OF_X.T - y), X)
    W = W - a * gradient
    Cost_Function_previous = Cost_Function
    Cost_Function = np.dot(y, np.log(H_OF_X)) + np.dot((1 - y), np.log(1 - H_OF_X))
    # Cost function of a logistic regression , which is used to see the cost changing condition during learning

    Cost_ChangingRate = (Cost_Function_previous - Cost_Function)/Cost_Function.sum()
    print("For logistic regression",i ,"times, Costfuction redced to",Cost_Function)
    '''
    if Cost_ChangingRate.sum() < 0.00001 and Cost_ChangingRate.sum() > -0.00001:
        break
    '''

(L, k) = make_blobs(n_samples = 1000, n_features = 2, centers = 2, cluster_std = 1.3, random_state = 20)
m = np.shape(L)[0]
n = np.shape(L)[1]
#np.shape returns a array (a, b) that describe the element number in a numpyarray's first and second axis

L = np.c_[np.ones((m, 1)), L]
#This method is to put a L0 in every sample, L is a m * (n+1) matrix

print("New data has been produced, Start to predict:")
for j in range(m):
    H_OF_L = np.dot(W, L.T[:,j])
    H_OF_L = sigmoid_transition(H_OF_L)
    if H_OF_L >= 0.5:
        Predicting_Result = 1
    else:
        Predicting_Result = 0
    if Predicting_Result != k[j]:
        error += 1
    print("Sample no.",j,"Predicted output:",Predicting_Result,"real output:",k[j])
#For predicting the sample output, first produce a same sample list as X

print("accurate rate goes to:",100-error_rate(error, m),"%")
print("error rate goes to:",error_rate(error, m),"%")
#print out the rate of accuracy

