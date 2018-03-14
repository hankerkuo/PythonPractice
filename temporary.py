'''
A = ([[1, 2, 3], [2, 3, 4]])
print(numpy.dot(A[0], A[1]))

def test(*getin):
    return list(map(lambda x: x*2 ,getin))
print(test(1,2,3))

from random import gauss
from random import seed
from pandas import Series
from pandas.tools.plotting import autocorrelation_plot
from matplotlib import pyplot
# seed random number generator
seed(5)
# create white noise series
series = [gauss(0.0, 2.0) for i in range(1000)]
series = Series(series)
# summary stats
print(series.describe())
# line plot
series.plot()
pyplot.show()
# histogram plot
series.hist()
pyplot.show()
# autocorrelation
autocorrelation_plot(series)
pyplot.show()
'''
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
def sigmoid_changing(x):
    return 1/(1+np.exp(-x))
def double(x):
    return 2*x

X, y = make_blobs(n_samples=10, centers=3, n_features=2,
                  random_state=1)
X = np.c_[np.ones((X.shape[0])), X]
print(X)
W = np.random.uniform(size=(X.shape[1],))
print(np.dot(X, W))
h = double(X.dot(W))
print(h)
