# -*- coding: utf-8 -*-
"""

Created on Sun Mar  8 16:51:30 2020
@author: VASU

"""

import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as linalg
import scipy.optimize as sopt
from mpl_toolkits.mplot3d import axes3d
import time

# Objective function to be minimized
def f(x):
    return (x[0]**2+x[1]-11)**2+(x[0]+x[1]**2-7)**2

# 20-20*exp(-0.2*sqrt(0.5*(x[0]*x[0]+x[1]*x[1])))+exp(0.5*(cos(2*pi*x[0]) + cos(2*pi*x[1])))
# (x[0]-2)**2 + (x[0]-2*x[1])**2
# -2*sin(x[0])+ 0.1*x[1]**2
# -(2*x[0]*x[1]+2*x[0]-x[0]**2-2*x[1]**2)
# (sin(3*pi*x[0]))**2 + ((x[0] - 1)**2)* (1 + sin(3*pi*x[1]))**2 + ((x[1]-1)**2)*(1 + sin(2*pi*x[1]))**2
#  (x[0]**2 - x[1])^2 + (1 - x[0])^2
# -0.26*(x[0]**2+x[1]**2)-0.48*x[0]*x[1]
    
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

"""

 n = Number of variables/dimension of problem
 gamma = expansion parameter
 beta = contraction parameter
 N = number of iterations
 epsilon = Termination parameter

"""

t = time.time()



# Parameters involved
gamma, beta, N, epsilon, n = 2, 0.5, 20, 0.001, 2

# Initial point
X = np.array([0, 0])

# values is an array and stores the next points obtained by Nelder Mead method step
values = [np.array([0, 0])] # Initial point already stored

# Creating initial simplex

"""
Initial simplex is created by first declaring an nXn Identity matrix.
Then a row of zeros is appended at the beginning.
Then each row is added by the initial point to get the simplex.
"""

X_simplex = np.append(np.zeros((1, n)), np.identity(n), axis=0)

# Initial simplex
X_sim = [X+X_simplex[i] for i in range(n+1)]

for iter in range(N):
    
    # Finding worst, best and second to worst points
    x_h = X_sim[0] # Stores worst point
    x_g = X_sim[0] # Stores best point

    first = second = x_g # second stores second worst point
    
    j, worstIndex= 0, 0
    
    # This loop finds best, worst and second to worst point
    for Xiter in X_sim:
        
        if(f(Xiter)>=f(x_h)): # calculates maximum
            x_h = Xiter
            worstIndex = j
        if(f(Xiter)<=f(x_g)): # calculates minimum
            x_g = Xiter
        
        # Logic obtained from geeksfromgeeks.com
        if(f(Xiter)>f(first)): # calculates second maximum
            second = first
            first = Xiter
        elif(f(Xiter)>f(second) and f(Xiter) != f(first)):
            second = Xiter
        j=j+1
        
    
    # Centroid of face not containing the worst point
    x_c = [0,0]
    for Xiter in X_sim:
        x_c = x_c + Xiter
    x_c = (x_c - x_h)/n
    
    # Calculate the reflected point
    x_r = 2*x_c-x_h
    x_new = x_r
    
    # Obtain the new point by performing expansion or contraction
    if(f(x_r)<f(x_g)): # Expansion
        x_new = (1+gamma)*x_c - gamma*x_h
    elif(f(x_r)>=f(x_h)): # Contraction
        x_new = (1-beta)*x_c + beta*x_h
    elif(f(second)<f(x_r)<f(x_h)): # Contraction
        x_new = (1+beta)*x_c - beta*x_h
    
    # Append this point to the value array
    values.append(x_new)    
    # Replace the worst point in simplex by the new point
    X_sim[worstIndex] = x_new
    
    # Find the error, as given in Kalyanmoy Deb's textbook.
    error = 0
    for Xiter in X_sim:
        error = error+(f(Xiter)-f(x_c))**2
    error = (error/(n+1))**0.5
    
    if error<epsilon:
        break

elapsed = time.time() - t

# Visualize the points obtained by algorithm
plt.axis("equal")
plt.contour(xmesh, ymesh, fmesh, 50)
it_array = np.array(values)
plt.plot(it_array.T[0], it_array.T[1], "x-")

plt.plot(values[0][0], values[0][1], "o", color='black')
plt.plot(values[-1][0], values[-1][1], "o", color='red')

plt.plot(values)
