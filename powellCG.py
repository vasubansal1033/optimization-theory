# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 13:58:27 2020

@author: VASU
"""

import numpy as np
import numpy.linalg as linalg
import scipy.optimize as sopt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from numpy import sqrt, sin, cos, exp
pi = 3.14159
# Objective function to be minimized
def f(x):
    return 20-20*exp(-0.2*sqrt(0.5*(x[0]*x[0]+x[1]*x[1])))+exp(0.5*(cos(2*pi*x[0]) + cos(2*pi*x[1])))

##########################################################################

# Visualize 3d mesh plot of funtion
# fig = plt.figure()
# ax = fig.gca(projection="3d")
xmesh, ymesh = np.mgrid[-5:8:50j,-5:8:50j]
fmesh = f(np.array([xmesh, ymesh]))
# ax.plot_surface(xmesh, ymesh, fmesh)

# #--------- Do not run these two codes together-------------- #

# # Visualize the contour plot of function
# plt.axis("equal")
# plt.contour(xmesh, ymesh, fmesh)

##########################################################################

N = 7 # Number of iterations
n = 2 # number of dimensions of objective function
epsilon1 = 10**-6

# values is an array and stores the next points
values = [np.array([2, 2])] # Already stores Initial point

directions = np.array([[1., 0.], [0., 1.]])
# directions = [[1,0,0], [0,1,0],[0,0,1]]

for i in range(N):
    # Using the index -1 directly gives the last point of array
    x = values[-1]
    
    # Minimize along N unidirectional search directions 
    for direction in directions:
        
        def f_alpha(alpha):
            return f(x + alpha*direction)
    
        alpha_opt = sopt.golden(f_alpha)
        x = x + alpha_opt*direction
        values.append(x)
    
    # Minimize once more along first direction
    def f_alpha(alpha):
        return f(x + alpha*direction[0])
    
    alpha_opt = sopt.golden(f_alpha)
    x = x + alpha_opt*direction[0]
    values.append(x)
    
    # Form new conjugate direction using parallel subspace property
    new_dir = values[-1]-values[-1-n]
    
    # Normalize the direction
    new_dir = new_dir/linalg.norm(new_dir)
    
    
    # Rearrange the directions and add the new direction
    j=n-1    
    while(j>0):
        directions[j]=directions[j-1]
        j=j-1
    directions[j] = new_dir
        
    
# Visualize the points obtained by algorithmplt.axis("equal")
plt.contour(xmesh, ymesh, fmesh, 50)
it_array = np.array(values)

plt.plot(it_array.T[0], it_array.T[1], "x-")
plt.plot(values[0][0], values[0][1], "o", color='black')
plt.plot(values[-1][0], values[-1][1], "o", color='red')

plt.plot(values)



