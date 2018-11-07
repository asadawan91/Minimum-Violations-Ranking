# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 13:51:32 2018

@author: rajar
"""

import numpy as np
import random
import math
import matplotlib.pyplot as plt
import copy
import time

# Plot the violations V(t) as a function of time (t) and a function of
# the probabilities [0,1] in steps of 0.1 keeping n = 50 fixed

# Count time
start_time = time.time()

runs = np.arange(1.0, 5.01, 1.0)

# Generating a random graph
n = 100
m = 100
p = 0.15
k = []
ad = np.zeros((n,m))
for i in range(0,n):
    for j in range(0,m):
        rand = random.uniform(0, 1)
        if (rand <= p):
            if (i != j):
                ad[i][j] = 1
    k.append(i)
        
adj = ad.tolist() 

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
#print(min_vio1)

# Calcualate the stopping time
stopping_time = int(nCr(n, 2))

# Initialize the data structures for storing the timesteps and the
# values of the minimum violation values
minimum_violations_lists_r = []
minimum_violations_timesteps_r = []
hist_timesteps_r = []

# Outer loop for number of runs
final_timesteps = []
final_violations = []

for run in runs:
    time_taken = 0
    min_vio_list_r = []
    r = copy.deepcopy(k)
    min_vio_timestep_r = []
    min_vio = min_vio1
    mvt = 0
    #while there are no drops in V for nC2 iterations
    while (time_taken != stopping_time):
        mvt += 1
        min_vio_timestep_r.append(mvt)
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
        min_vio_list_r.append(min_vio)
        
    # Update the lists for plotting
    minimum_violations_lists_r.append(copy.deepcopy(min_vio_list_r))
    minimum_violations_timesteps_r.append(copy.deepcopy(min_vio_timestep_r))
    hist_timesteps_r.append(len(min_vio_timestep_r))
    final_violations.append(min_vio)
    final_timesteps.append(mvt)
    
avg_fin_vio = sum(final_violations)/len(runs)
avg_fin_tim = sum(final_timesteps)/len(runs)

print("Initial number of violations :", min_vio1)
print("Average number of final violations :", avg_fin_vio)
print("Average number of total timesteps :", avg_fin_tim)

# Plotting V vs. t
#plt.plot(min_vio_timestep, min_vio_list, linestyle='-.', color='b',
#         linewidth=2)
#plt.xlabel('Number of timesteps t')
#plt.ylabel('Number of violations V')
#plt.show()  

# Plotting V vs. t for all runs
for list1, list2 in zip(minimum_violations_timesteps_r,
                        minimum_violations_lists_r):
    plt.plot(list1, list2, linestyle='-',linewidth=2)
plt.xlabel('Number of timesteps t')
plt.ylabel('Number of violations V(t)')
plt.savefig('V_versus_t_random-graph_nodes-100_p-0-15_runs-5', dpi = 300)
plt.show() 

## Plotting the histogram for the timesteps
#x = hist_timesteps_r
#plt.hist(x, normed=False, bins=30)
#plt.xlabel('Timestep values t')
#plt.ylabel('Number of occurences')
#plt.savefig('Histogram_random-graph_nodes-100_p-0-90_runs-50', dpi = 300)
#plt.show()

# Record elapsed time
elapsed_time = time.time() - start_time

print(elapsed_time, 'seconds' )
#print((elapsed_time/3600), 'hours' )   