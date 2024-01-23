import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time

'''
This file contains all the functions that are needed in order to determine different commutation graphs given Pauli strings and their minimal amount of commuting families. 
'''

# firstly, check the Paulistrings. Which means that it will be ensured that the Pauli strings stem from the Jordan Wigner transformation. 
# In the Hamiltonian, we have either 2 - or 4 creation and annihilation operators, which will be transformed. 
# The transformation introduces a term like (X+Y) ZZ ... ZZ
# A couple of constraints can be inferred by this on the Pauli strings. A paulistring can never have either X or Y on the fifth position in the string.
# In the first four indices, if there is an X or a Y followed by a Z, the Pauli string is not valid. 

def check_Paulistring(paulistrings):
    '''
    return false if paulistring not created by Jordan Wigner
    '''
    for j in range(len(paulistrings)):
        paulistring = paulistrings[j]
        for i in range(len(paulistring)):
            if i > 3 and paulistring[i] in ['X', 'Y']:
                print('The ' + str(j) + 'th Paulistring is not valid given the Jordan Wigner transformation.')
                return False
            elif i in range(1,4) and paulistring[i] in ['X', 'Y'] and paulistring[i-1] == 'Z':
                print('The ' + str(j) + 'th Paulistring is not valid given the Jordan Wigner transformation.')
                return False
    return True


'''
Commutation functions

- we want to know if two pauli strings commute under a certain rule - GC and QWC. 
For this, first establish commuatation rules in function allgemein_commutes
Then define functions for GC and QWC
'''

# Need a function to determine if two variables commute. X and Y or X and Z etc. do not commute. 
# Every operator commutes with the Identity.
# And every operator commutes with itself. 

# accepts two operators, which are firstly only strings 
def allgemein_commutes(a, b):
    if a == b: 
        return True
    elif a == '1' or b == '1': 
        return True
    else: 
        return False

# takes two pauli strings as input and returns true if they QWC commute 
def QWC_commutes(str1, str2): 

    # the pauli strings have to be from the same hamiltonian, thus of same size 
    if len(str1) != len(str2):
        print('strings are not the same size, sizes are ' + str(len(str1)) + ' and ' + str(len(str2)))
        return False

    # if any of the elements in the Pauli strings do not commute, the strings do not QWC commute 
    for i in range(len(str1)):
        if not allgemein_commutes(str1[i], str2[i]):
            return False
    return True

def GC_commutes(str1, str2, without_QWC): 

    # if they are not the same size -> error
    if len(str1) != len(str2):
        return False

    # non_commuting_count is a variable that counts how many of the elements in the two Pauli strings do not commute 
    non_commuting_count = 0
    
    # if it does not commute, increase the count of not commuting elements by one 
    for i in range(len(str1)):
        if not allgemein_commutes(str1[i], str2[i]):
            non_commuting_count += 1

    # for GC but not QWC, choose also that non_commuting_count should not be zero 
    if without_QWC and non_commuting_count == 0:
        return False


    # if this number is even, the strings GC commute 
    if non_commuting_count%2 == 0:
        return True
    else:
        return False


'''
Create Graphs
'''

# create the Graph given all the different Pauli strings
def create_Graph_QWC(paulistrings):
    '''
    returns Graph, gets List of Paulistrings as input
    '''
    # Copy of this Paulistring list 
    paulistrings_updatet = paulistrings.copy()

    # create Graph
    Pauli_Graph = nx.Graph()

    for string in paulistrings:

        # add every Pauli string as a node to the graph
        Pauli_Graph.add_node(string)
        for other_string in paulistrings_updatet:

            # Paulistring always commutes with itself. 
            if other_string == string: 
                continue

            # If two of the paulistrings commute, connect them
            if QWC_commutes(string, other_string):
                Pauli_Graph.add_edge(string, other_string)

        # To avoid double counting
        paulistrings_updatet.remove(string)    # (Wenn wir fuer einen string alle possibilities durchhaben, muessen wir den fuer die weiteren connections nicht beachten)


    return Pauli_Graph


def create_Graph_GC(paulistrings, without_QWC = False):
    '''
    returns Graph, gets List of Paulistrings as input
    '''
    # Copy of this Paulistring list 
    paulistrings_updatet = paulistrings.copy()

    # create Graph
    Pauli_Graph = nx.Graph()

    # To color the different edges differently, dep on the commutation type
    edge_colors = []

    for string in paulistrings:
        Pauli_Graph.add_node(string)
        for other_string in paulistrings_updatet:
            if other_string == string: 
                continue
            elif GC_commutes(string, other_string, without_QWC):
                Pauli_Graph.add_edge(string, other_string)

                # If QWC, paint the edge green
                if QWC_commutes(string, other_string):
                    edge_colors.append('blue')
                # If only GC, paint the edge red 
                elif not QWC_commutes(string, other_string):
                    edge_colors.append('red')
                    
        paulistrings_updatet.remove(string)    # (Wenn wir fuer einen string alle possibilities durchhaben, muessen wir den fuer die weiteren connections nicht beachten)

    return Pauli_Graph, edge_colors


'''
Draw Graph
'''

def draw_Graph(graph, title, edge_colors):
    '''
    Simply displays Graph with title using Matplotlib 
    '''
    fig, ax = plt.subplots(figsize=(8,6))

    draw_options = {
        'node_color': 'lightblue',
        'node_size': 900,
        'width': 1, 
        'edgecolors': 'black'
    }

    # If the two types of commutation are displayed in one graph, we want to differentiate between them using color 
    if edge_colors != []:
        nx.draw_shell(graph, with_labels = True, **draw_options, edge_color = edge_colors)
    else: 
        nx.draw_shell(graph, with_labels = True, **draw_options)

    plt.title(title)
    plt.show()



'''
Find max clique
'''

def find_max_clique(Graph, clique_list):
    '''
    To be used iteratively, gets as Input a graph and a list with all the maximum cliques so far 
    Adds the maximum clique of the current graph to the list and stops when theres only one clique left. 
    '''

    # copy graph, we dont want to manipulate the original Graph
    graph = Graph.copy()
    

    all_cliques_list = list(nx.find_cliques(graph))
    print('all list: ',all_cliques_list)
    print('max element: ', all_cliques_list[0])
    clique_list.append(all_cliques_list[0])

    if len(all_cliques_list) != 1:
        [graph.remove_node(nd) for nd in all_cliques_list[0]]
        find_max_clique(graph, clique_list)

    n = nx.number_of_nodes(graph)

    return clique_list


def find_max_clique_alt(Graph, clique_list):
    '''
    Uses method max_clique()
    '''
    graph = Graph.copy()

    max_clique_temp = nx.max_clique(graph)




'''
Draw new graph
'''

def draw_new_Graph(resulting_families, title):
    '''
    Draws the resulting families 
    '''
    # create a new graph to draw 
    new_Graph = nx.Graph()
    for i in range(len(resulting_families)):
        temp_list = resulting_families[i]
        for j in range(len(temp_list)):
            if j == len(temp_list)-1:
                new_Graph.add_edge(temp_list[j], temp_list[0])
            else:
                new_Graph.add_edge(temp_list[j], temp_list[j+1])
            

    draw_Graph(new_Graph, title, [])


