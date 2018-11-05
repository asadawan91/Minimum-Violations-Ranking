# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 12:00:16 2018

@author: rajar
"""

import numpy as np
import networkx as nx

graph = nx.DiGraph()
graph.add_nodes_from(range(11,14))
graph.add_edges_from([(11,12),(12,13),(13,14)])
#nx.draw(graph)

pos = nx.spring_layout(graph)

adj = nx.adjacency_matrix(graph)
#print(adj)
A = adj.todense()
print(A)

A[:,[2,1]] = A[:,[1,2]]
print (A)

A[[2,1],:] = A[[1,2],:]
print(A)