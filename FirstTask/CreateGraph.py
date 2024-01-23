import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time
from Methods import *

# create a copy of the list of Paulistrings
# Paulistrings is a list of Strings, which contain 'X', 'Z', 'Y' and '1'

# list of Paulistrings
# PauliStrings = ['X1ZY', 'X1XX', 'XYYZ', 'ZZZZ', '1111', 'XXXX', 'YYYY']

# example for all possible two qubit pauli strings (16):
# PauliStrings = ['XX', 'YY', 'ZZ', '11', 'X1', 'XY', 'XZ', 'Y1', 'YX', 'YZ', 'Z1', 'ZX', 'ZY', '1X', '1Y', '1Z']
 
# example from paper 
PauliStrings = ['ZZ11', '111Z', '11Z1', '1Z11', 'Z111', 'Z1Z1', '1ZZ1', 'Z11Z', '1Z1Z', '11ZZ', 'XXYY', 'YXXY', 'XYYX', 'YYXX']



def Main():

    check = check_Paulistring(PauliStrings)

    if not check:
        return False 


    Graph_QWC = create_Graph_QWC(PauliStrings)
    Graph_GC, edge_colors_GC = create_Graph_GC(PauliStrings)


    # to keep track of time, to compare runtimes for different algorithms to each other, first calculate number of families for GC
    start = time.time()
    result_GC = find_max_clique(Graph_GC, [])
    end = time.time()
    time_GC_ms = np.round(1000*(end-start), 3)

    # then, calculate number of families for QWC
    start = time.time()
    result_QWC = find_max_clique(Graph_QWC, [])
    end = time.time()
    time_QWC_ms = np.round(1000*(end-start), 3)


    draw_Graph(Graph_GC, 'General Commutation', edge_colors_GC)
    draw_Graph(Graph_QWC, 'Cubit Wise Commutation', [])

    draw_new_Graph(result_GC, 'GC, #families: ' + str(len(result_GC)) + ', #naive: ' + str(len(PauliStrings)) + ', time: ' + str(time_GC_ms) + 'ms')
    draw_new_Graph(result_QWC, 'QWC, #families: ' + str(len(result_QWC)) + ', #naive: ' + str(len(PauliStrings)) + ', time: ' + str(time_QWC_ms) + 'ms')


Main()

'''
Further ideas: 

comparing sets of Pauli strings of different lengths to each other, depending on the element the Hamiltonian stems from. 
The number of Pauli strings will increase with the complexity of the molecule. 

And the computation time will increase as well. 

The idea is, comparing the computation time of estimating the ground state energy for the three methods: Naive, QWC and GC.

Also, one could compare the times it takes to partition the Paulistrings into commuting families with the two different methods, GC and QWC. 
'''
