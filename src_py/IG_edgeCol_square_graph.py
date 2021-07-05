# Idea: extract an edge coloring of G from a "super edge coloring" (ie vertex coloring of G^2)
# We know that if G is a tree or a IG, then it is easy to determine a delta(G) + 1 vertex coloration of G^2

import intersection_graph as I
import igraph
import numpy as np

import pandas as pd

# PARAMETERS
n = 15

def is_superC(graph, col, verbose = False):
    '''
    Determines if graph (igraph type) is a proper surperC
    col is the list of colorations.
    '''
    n = len(graph.degree()-1) #checking the last one is useless
    for i in range(n):
        nI = graph.neighborhood(i, 2)
        for j in nI:
            if i != j and col[i] == col[j]: #have to add i != j as neighborhood works weirdly.
                if verbose:
                    print("\nThe graph does not have a proper super coloration.\nIncriminated vertices: ", i, j)
                return False
    if verbose:
        print("\nThe graph has a proper supercoloration")
    return True

def is_proper_EC(M, verbose=False):
    '''
    determines if the edge coloration of a graph is proper by checking all the incident edges of every vertex.
    Namely, for all i, it doesnt exists j1 and j2 st M[i][j1] = M[i][j2] and conversly for collumns. 
    If we suppose M is symmetric (we do) only lines need to be checked/
    verbose param. prints additional informations when M is not proper.  
    '''
    for i in range(len(M)):
        for j1 in range(len(M)):
            col_ij1 = M[i][j1]
            for j2 in range(j1):
                if M[i][j2] == col_ij1:
                    if verbose:
                        print("edge coloration not proper; see couple", i, j1, " and ", i, j2)
                    return False
    return True
    



def extract_edge_coloration(M, supercolG, edgecolK, verbose = False):
    '''
    extract from supercolG a coloration of the edges og G using the values of edgecolK using the algorithm described in the latex.
    gives the result under a matricial form (modification of M, the adjacency matrixs)
    supercolG = list
    edgecolK : matrix
    '''
    n = len(M)
    for i in range(n):
        for j in range(i):
            ci, cj = supercolG[i], supercolG[j]
            if M[i][j] != 0:
                colK = edgecolK[ci][cj]
                M[i][j], M[j][i] = colK
    return M

def KnEdgeColoration(n, printM = False, verbose = False):
    '''
    Does the Kn edge coloration according to the Soifer description.
    Returns a matrix.
    if verbose, also plots the colored graph using igraph library.
    '''
    M = np.zeros((n, n)).tolist()

    # Extract (wikipédia): 
    # Soifer (2008) provides the following geometric construction of a coloring in this case: 
    # place n points at the vertices and center of a regular (n − 1)-sided polygon. 
    # For each color class, include one edge from the center to one of the polygon vertices, 
    # and all of the perpendicular edges connecting pairs of polygon vertices.

    for i in range(1, n):
        M[0][i]= int(i)
        M[i][0] = int(i)
    
    if n%2 ==1: #ie n is odd
        for col in range(n): 
            nEdgesTODO = int( (n-1)/2 )
            i = (col -1)%n
            j = (col+1)%n

            for whatever in range(nEdgesTODO):
                M[i][j] = col+1
                M[j][i] = col+1
                if verbose:
                    print(i, j, col+1, M)
                i = (i-1)%n
                j = (j+1)%n        


    if n%2 == 0: #ie n is even.         The algorithm is done color by color, ordered by the outer edges.
        for start_i in range(1, n):
            j = start_i +1
            i = start_i 
            if j == n:  # last edge to color case
                j=1

            tmp = (int(n/2)+i)%n
            if tmp != int(n/2)+i:        # The 0 creates some glitches
                tmp += 1
            col = M[0][tmp]

            nEdgesTODO =int( (n-2)/2 )
            if verbose:
                print("edgestocolor: ", nEdgesTODO)
                print("col chosed: ", col)
            for whatever in range(nEdgesTODO):
                if verbose: 
                    print(M,i,j)
                M[i][j] = col
                M[j][i] = col
                j+=1
                i+=-1
                if i%n == 0:
                    i = 1
                if j%n == 0:
                    j = 1

    if verbose:
        M = pd.DataFrame(M, dtype = int)
        print(M)
        m = M.values.tolist()
    
        L = []
        for X in m:
            L = L+X

        while L.count(0)>0:
            L.remove(0)
        print(L, end='\n')
    
    
        gKn = igraph.Graph.Adjacency((M.values>0).tolist(), mode='undirected')
        gKn.es["color_assigned"] = L
        color_dict = {"1": 'red', "2": 'blue', "3": 'green'}
    

    #for col_num in gKn.es["color_assigned"]:
     #   print(color_dict[str(int(col_num))])
    #print([color_dict[int(col_num)] for col_num in gKn.es["color_assigned"]])    

        igraph.plot(gKn, edge_color = [color_dict[str(int(col_num))] for col_num in gKn.es["color_assigned"]])
    if not(verbose) and printM:
        print(pd.DataFrame(M, dtype=int))
    return M


print(is_proper_EC(KnEdgeColoration(19, printM=True), True))






            

