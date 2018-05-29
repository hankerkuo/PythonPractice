import pylab
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5,5,100) # 100 linearly spaced numbers
# y = numpy.sin(x)/x # computing the values of sin(x)/x
z = 1.7159 * np.tanh((2 / 3) * x)

# compose plot
# pylab.plot(x, y)  # sin(x)/x
# pylab.plot(x, y, 'co')  # same function with cyan dots
# pylab.plot(x, 2 * y, x, 3 * y)  # 2*sin(x)/x and 3*sin(x)/x

pylab.plot(x, z)
plt.xticks(np.arange(min(x), max(x)+1, 1.0))
pylab.show() # show the plot