# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:47:00 2020

@author: VASU
"""
import time
import numpy as np
import numpy.linalg as linalg
import scipy.optimize as sopt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from numpy import sqrt, sin, cos, exp
pi = 3.14159

N = 20 # number of iterations
# values is an array and stores the next points obtained using Cauchy method
values = [np.array([0, 0])] # Initial point

# Objective function to be minimized
def f(x):
    return (x[0]**2+x[1]-11)**2+(x[0]+x[1]**2-7)**2

# Gradient of the function
def df(X):
    x = X[0]
    y = X[1]
    h = 10**-6
    val1 = (f([x+h, y])-f([x, y]))/h
    val2 = (f([x, y+h])-f([x, y]))/h
    return np.array([val1, val2])

##########################################################################

# Visualize 3d mesh plot of funtion
# fig = plt.figure()
# ax = fig.gca(projection="3d")
xmesh, ymesh = np.mgrid[-5:5:50j,-5:5:50j]
fmesh = f(np.array([xmesh, ymesh]))
# ax.plot_surface(xmesh, ymesh, fmesh)

#--------- Do not run these two codes together-------------- #

# Visualize the contour plot of function
plt.axis("equal")
plt.contour(xmesh, ymesh, fmesh)

##########################################################################

t = time.time()


for i in range(N):
    x = values[-1] # Using the index -1 directly gives the last point of array
    dir_ = -df(x) # Get the steepest direction
    
    # This is the function along the steepest direction in terms of alpha
    def f_alpha(alpha):
        return f(x + alpha*dir_)
    
    # This command returns optimal value of alpha, using inbuilt golden section search
    alpha_opt = sopt.golden(f_alpha)
    next_ = x + alpha_opt * dir_ 
    
    # Append this value to the values array
    values.append(next_)

elapsed = t-time.time()

# Visualize the points obtained by algorithm
plt.axis("equal")
plt.contour(xmesh, ymesh, fmesh, 50)
it_array = np.array(values)
plt.plot(it_array.T[0], it_array.T[1], "x-")

plt.plot(values[0][0], values[0][1], "o", color='black')
plt.plot(values[-1][0], values[-1][1], "o", color='red')

plt.plot(values)



