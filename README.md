# Minimum-Violations-Ranking
Implementation of the Minimum Violations Ranking algorithm to rank the nodes or vertices in a network. The first graph is a a directed chain of n = 50 vertices such that A(i;i+1) = 1 for i = 1,2,3,...,49. The second graph is an Erdos-Renyi random graph in which n = 50 and p = 0.15. 

Two dimensional plots of the Number of violations V(t) have been shown as a function of the time-steps required to complete the algorithm, along with a histogram showing the distribution of the number of time-steps.

In the second part of the problem, we generate random directed (Erdos Renyi) graph in which thre exist no 'correct' or gold standard rankings. We then execute our MVR algorithm on it with the hope that is assigns some ranking to it with the same stoppping conditions as before. A study was conducted with the probability of connection spanning the entire range for 50 - 100 nodes in the graph.

Three-dimensional plots of four quantities were plotted as a function of the probability of connection p and the number of nodes n in the graph. The quantities of interest are: 
(1) Initial number of Violations,
(2) Average Final number of Violations,
(3) Average Decrease in number of Violations,
(4) Average Final number of time-steps.

