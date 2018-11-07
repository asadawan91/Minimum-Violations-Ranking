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
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

# Plot the violations V(t) as a function of time (t) and a function of
# the probabilities [0,1] in steps of 0.1 keeping n = 50 fixed

# Count time
start_time = time.time()

number_of_nodes = np.arange(50.0, 100.01, 5.0)
probabilities = np.arange(0.0, 1.001, 0.1)
runs = np.arange(1.0, 10.01, 1.0)

# Generating a random graph
def random_graph_generator(n, m, p):    
    
    k = []
    n1 = int(n)
    m1 = int(m)
    ad = np.zeros((n1,m1))
    for i in range(0,n1):
        for j in range(0,m1):
            rand = random.uniform(0, 1)
            if (rand <= p):
                if (i != j):
                    ad[i][j] = 1
        k.append(i)
            
    adj = ad.tolist() 
    
    return (k, adj)

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

#min_vio1 = 0
# Shuffle the rankings
#random.shuffle(k)

# Generate the initial number of violations
#min_vio1 = violations(generate_matrix(k,adj))
#print(min_vio1)

# Calcualate the stopping time
#stopping_time = int(nCr(n, 2))

#--------------------------------------------------------------------------------

array_probability = []
array_nodenumber = []
array_initial_violations = []
array_final_violations = []
array_decrease_in_violations = []
array_final_timesteps = []


for node_num in number_of_nodes:

    for pr in probabilities:

        k, adj = random_graph_generator(node_num, node_num, pr)
        random.shuffle(k)
        min_vio1 = 0
        min_vio1 = violations(generate_matrix(k,adj))
        stopping_time = int(nCr(node_num, 2))

        # Initialize the data structures for storing the timesteps and the
        # values of the minimum violation values
        #minimum_violations_lists_r = []
        #minimum_violations_timesteps_r = []
        #hist_timesteps_r = []

        # Outer loop for number of runs
        #final_timesteps = []
        #final_violations = []

        total_final_violations = 0
        total_final_timesteps = 0

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
            #minimum_violations_lists_r.append(copy.deepcopy(min_vio_list_r))
            #minimum_violations_timesteps_r.append(copy.deepcopy(min_vio_timestep_r))
            #hist_timesteps_r.append(len(min_vio_timestep_r))
            #final_violations.append(min_vio)
            #final_timesteps.append(mvt)

            total_final_violations += min_vio
            total_final_timesteps += mvt

        array_probability.append(pr)
        array_nodenumber.append(node_num)

        array_initial_violations.append(min_vio1)
        array_final_violations.append(total_final_violations/len(runs))
        array_decrease_in_violations.append(min_vio1 - (total_final_violations/len(runs)))
        array_final_timesteps.append(total_final_timesteps/len(runs))

#avg_fin_vio = sum(final_violations)/len(runs)
#avg_fin_tim = sum(final_timesteps)/len(runs)

#print("Initial number of violations :", min_vio1)
#print("Average number of final violations :", avg_fin_vio)
#print("Average number of total timesteps :", avg_fin_tim)

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_nodenumber, array_probability, array_initial_violations)
ax.set_xlabel('Number of nodes n')
ax.set_ylabel('Probability of drawing an edge p')
ax.set_zlabel('Initial Number of Violations')
ax.legend()
plt.savefig('Initial-Number-of-Violations_vs_Number-of-Nodes_vs_Probability', dpi = 300)
plt.show()

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_probability, array_nodenumber,  array_initial_violations)
ax.set_xlabel('Probability of drawing an edge p')
ax.set_ylabel('Number of nodes n')
ax.set_zlabel('Initial Number of Violations')
ax.legend()
plt.savefig('Initial-Number-of-Violations_vs_Probability_vs_Number-of-Nodes', dpi = 300)
plt.show()

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_nodenumber, array_probability, array_final_violations)
ax.set_xlabel('Number of nodes n')
ax.set_ylabel('Probability of drawing an edge p')
ax.set_zlabel('Final (Average) Number of Violations')
ax.legend()
plt.savefig('Final-Avg-Number-of-Violations_vs_Number-of-Nodes_vs_Probability', dpi = 300)
plt.show()

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_probability, array_nodenumber, array_final_violations)
ax.set_xlabel('Probability of drawing an edge p')
ax.set_ylabel('Number of nodes n')
ax.set_zlabel('Final (Average) Number of Violations')
ax.legend()
plt.savefig('Final-Avg-Number-of-Violations_vs_Probability_vs_Number-of-Nodes', dpi = 300)
plt.show()

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_nodenumber, array_probability, array_decrease_in_violations)
ax.set_xlabel('Number of nodes n')
ax.set_ylabel('Probability of drawing an edge p')
ax.set_zlabel('Decrease in (Average) Number of Violations from Initial Number')
ax.legend()
plt.savefig('Decrease-in-Violations_vs_Number-of-Nodes_vs_Probability', dpi = 300)
plt.show()

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_probability, array_nodenumber, array_decrease_in_violations)
ax.set_xlabel('Probability of drawing an edge p')
ax.set_ylabel('Number of nodes n')
ax.set_zlabel('Decrease in (Average) Number of Violations from Initial Number')
ax.legend()
plt.savefig('Decrease-in-Violations_vs_Probability_vs_Number-of-Nodes', dpi = 300)
plt.show()

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_nodenumber, array_probability, array_final_timesteps)
ax.set_xlabel('Number of nodes n')
ax.set_ylabel('Probability of drawing an edge p')
ax.set_zlabel('Final (Average) Number of Timesteps')
ax.legend()
plt.savefig('Final-Avg-Number-of-Timesteps_vs_Number-of-Nodes_vs_Probability', dpi = 300)
plt.show()

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(array_probability, array_nodenumber, array_final_timesteps)
ax.set_xlabel('Probability of drawing an edge p')
ax.set_ylabel('Number of nodes n')
ax.set_zlabel('Final (Average) Number of Timesteps-2')
ax.legend()
plt.savefig('Final-Avg-Number-of-Timesteps_vs_Probability_vs_Number-of-Nodes', dpi = 300)
plt.show()

# Record elapsed time
elapsed_time = time.time() - start_time

print(elapsed_time, 'seconds' )
print((elapsed_time/3600), 'hours' )   