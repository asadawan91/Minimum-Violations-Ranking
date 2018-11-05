# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 00:13:37 2018

@author: rajar
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import operator as op
import math
import numpy as np
import copy

# Create a directed graph of n = 50 vertices such that A(i,i+1) = 1
# for i = 1,2,3,...,49
adj = [] # Adjacency matrix for the graph
k = [] # Actual ranking of the vertices
for i in range(50):
    rows = [0] * 50
    if (i != 49):
        rows[i + 1] = 1
    adj.append(rows)
    k.append(i)

# Define the factorial function for determining the stopping timr
# of the algorithm
def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

# Define a function which shuffles the adjacency matrix based on the 
# list of random (initially) or swapped ranks
def generate_matrix(r,a):
    s = (len(r), len(r))
    new_adj = np.zeros(s)
    #print(type(new_adj))
    xi = 0
    for i in r:
        xj = 0
        for j in r:
            #print(a[di[i]][di[j]])
            new_adj[xi][xj] = a[i][j]
            xj += 1
        xi += 1
    return new_adj

# Define a function which calculates the number of violations in the
# adjacency matrix by computing the number of non-zero entries below
# the diagonal
def violations(a):
    lowertriangle = np.tril(a)
    viol = np.sum(lowertriangle)
    return (int(viol))



min_vio1 = 0
# Shuffle the rankings
random.shuffle(k)

# Generate the initial number of violations
min_vio1 = violations(generate_matrix(k,adj))
print(min_vio1)



# Calcualate the stopping time
stopping_time = int(nCr(50, 2))

# Initialize the data structures for storing the timesteps and the
# values of the minimum violation values
minimum_violations_lists = []
minimum_violations_timesteps = []
hist_timesteps = []

# Outer loop for number of runs
for runs in range(0,100):
    time_taken = 0
    min_vio_list = []
    r = copy.deepcopy(k)
    min_vio_timestep = []
    min_vio = min_vio1
    mvt = 0
    #while there are no drops in V for nC2 iterations
    while (time_taken != stopping_time):
        mvt += 1
        min_vio_timestep.append(mvt)
        rand1 = 0
        rand2 = 0  
        # Randomly pick any two different nodes
        while (rand1 == rand2):
            rand1 = random.randint(0, len(r)-1)
            rand2 = random.randint(0, len(r)-1)
        # Swap the two nodes in the rankings list r
        r[rand1],r[rand2] = r[rand2],r[rand1]
        # Get the adjacency matrix after swapping the two nodes
        shuffledmatrix = generate_matrix(r, adj)
        # Get the number of violations for the shuffled matrix 
        vio = violations(shuffledmatrix)
        # If the number of violations ddcreases or stays the same
        if (vio <= min_vio):
            if (vio < min_vio):
                time_taken = 0
            else:
                time_taken += 1
            min_vio = vio
        else:
            r[rand1],r[rand2] = r[rand2],r[rand1]
            time_taken += 1
        min_vio_list.append(min_vio)
        
    
    # Update the lists for plotting
    minimum_violations_lists.append(copy.deepcopy(min_vio_list))
    minimum_violations_timesteps.append(copy.deepcopy(min_vio_timestep))
    hist_timesteps.append(len(min_vio_timestep))

# Plotting V vs. t
#plt.plot(min_vio_timestep, min_vio_list, linestyle='-.', color='b',
#         linewidth=2)
#plt.xlabel('Number of timesteps t')
#plt.ylabel('Number of violations V')
#plt.show()  

# Plotting V vs. t for all runs
for list1, list2 in zip(minimum_violations_timesteps,
                        minimum_violations_lists):
    plt.plot(list1, list2, linestyle='-',linewidth=2)
plt.xlabel('Number of timesteps t')
plt.ylabel('Number of violations V')
plt.show() 

# Plotting the histogram for the timesteps
x = hist_timesteps
plt.hist(x, normed=True, bins=50)
plt.xlabel('Number of occurences')
plt.ylabel('Timesteps')
plt.show()
   
