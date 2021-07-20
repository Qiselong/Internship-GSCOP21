# the problem: can an SU (square - unit) intersection graph with \omega = 2 (triangle-free) and maximal degree 3 be 4-edge colorable?
# To prove that it is possible, exposing an example is sufficient.
# I want to prove it is not possible as it is my belief. I want to expose an algorithm to 3-color graphs with the previous parameters.

# If my predictions are correct, when given such a graph, by removing vertex of degree 1 one by one, you should end up with cycles that have common edges only
# (you may have to add dummy vertices/edges). I want to test this prediction with the following file.

import igraph

import random
import matplotlib.pyplot as plt
import time
import numpy

import sys
import copy



# some parameters
nV = 50 
scale = 4
nG = 1
omega = 2
delta = 4


toolbar_width = nG


def intersection(eA, eB):
    '''
    determines if eA and eB are intersecting or not using the projections. 
    '''
    for i in range(len(eA[0])):
        al = eA[0][i] #right point
        ar = eA[1][i] #left point
        bl = eB[0][i]
        br = eB[1][i]
        #it does not work if the left most point of one is less than the right most point of the other
        if (ar<bl) or (br<al):
            return False
    return True

def fill_edges(elements, graph):
    '''
    fill graph (of type igraph) with the connections of elements, determined by the intersection method. 
    '''
    for a in range(len(elements)):
        for b in range(a):
            if intersection(elements[a],elements[b]):
                graph.add_edges([(a,b)])
                #print(a, b)
    return graph # i think it is unecessary.

def color_dictionary(n):
    '''
    generates a random dictionary of colors of size n. 
    '''
    col_dict = {}
    for i in range(n):
        col_random = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        col_dict[i] = str(col_random) #rq= this is a different version of a function with the same name as here the keys are integers.
    return col_dict

def plot2D(elements, mode = 'trans1'):
    '''
    special 2D plot for squares.
    Uses elements after the use of special_graph under 'elementsForPlot=True' argument.
    The colors used are randomised using an intern color dictionary. 

    Modes:
    trans1  is all edges + LR diagonal; default mode
    '''
    n = len(elements)
    
    col_dict = color_dictionary(n)

    if mode == 'trans1':
        for el in range(n):
            col = col_dict[el]
            LLx, LLy = elements[el][0][0], elements[el][0][1]
            plt.plot([LLx, LLx], [LLy, LLy+1], col)
            plt.plot([LLx+1, LLx+1], [LLy, LLy+1], col)
            plt.plot([LLx, LLx+1], [LLy+1, LLy+1], col)
            plt.plot([LLx, LLx+1], [LLy, LLy], col)
            plt.plot([LLx, LLx+1], [LLy, LLy+1], col)
    
    if mode == 'nat':
        for el in range(n):
            col = col_dict[el]
            LLx, LLy = elements[el][0][0], elements[el][0][1]
            plt.plot([LLx, LLx], [LLy, LLy+1], col)
            plt.plot([LLx+1, LLx+1], [LLy, LLy+1], col)
            plt.plot([LLx, LLx+1], [LLy+1, LLy+1], col)
            plt.plot([LLx, LLx+1], [LLy, LLy], col)   
    
    
    plt.show()




def special_graph(n, om=10, delta = 10, gtype='none', elementsForPlot= False):
    '''
    creates a graph with n vertices and the special properties. 
    '''
    ts = time.clock_gettime_ns(time.CLOCK_BOOTTIME)

    graph = igraph.Graph(n+1)
    graph_copy = igraph.Graph(n+1) # the copy checks at every steps that the specs are still true.

    # one may add somtheing on the gtype parameter some day here
    elements = [] # list of our elements

    #first element
    LLx, LLy = numpy.random.normal(scale = scale, size= 2)
    elements.append([[LLx, LLy], [LLx+1, LLy+1]])
    elements_copy = elements.copy() #copy

    

    nel = 0
    while nel < n:
        # generate a new square
        LLx, LLy = numpy.random.normal(scale = 2, size= 2)
        elements_copy.append([[LLx, LLy], [LLx+1, LLy+1]])
        graph_copy = fill_edges(elements_copy, graph_copy)
        
        omega = graph_copy.clique_number()
        maxd = graph_copy.maxdegree()
        lastdeg = graph_copy.degree(nel+1)
        #print(omega, maxd, lastdeg, nel)
        #print(omega <= om and maxd<=delta and lastdeg != 0)
        

        if omega <= om and maxd<=delta and lastdeg != 0:
            #then act the addition of the element to elements list
            elements.append([[LLx, LLy], [LLx+1, LLy+1]])
            nel+=1
        elements_copy = elements.copy()
        graph_copy = igraph.Graph(n+1) # wipe the graph

    graph = fill_edges(elements, graph)
    #print("\nExecution time (ms): ",(time.clock_gettime_ns(time.CLOCK_BOOTTIME)-ts)/1000000)
    if elementsForPlot:
        return graph, elements
    return graph

#g = special_graph(nV, 2, 3)
#igraph.plot(g)

#next section is stolen code from stackoverflow
def testplot(graph, name):
    graph.vs['label'] = graph.vs['name']
    out = igraph.plot(graph, vertex_size=[a/5 for a in graph.betweenness()],
                      layout = graph.layout('grid'))
    out.save(name + '_allyBetweenness.png')


# if an epurated SU graph is 3-col, then the natural graph is 3-col.
# the epurated graph is obtained by removing all the vertices of degree 1.
# the proposition is true as: if a vertex is of degree one, is only
# neighbour is at most of a degree 3 as \delta = 3. if the edges of it's 
# neighbour are colored in 1 and 2, then chose 3 for this particular node.

def epuration(graph):
    '''
    epurates the graph by removing one by one the vertices of degree one.
    '''

    #deleted = 0
    #i=0

    nod1 = False
    nVertex = len(graph.degree())
 
    L = graph.degree()
    while L.count(1) !=0:
        to_del=[]
        for i in range(len(L)):
            if L[i] == 1:
                to_del.append(i)
        graph.delete_vertices(to_del)
        L = graph.degree()
    return graph





def rid_neighboors2(graph):
    nv = len(graph.degree())
    nT = nv #total number of vertices at start
    flag = True #set to false when a full travel with to_del == []
    n1 = 0 # number of vertices deleted because of degree 1
    n22 = 0 # number of time we deleted  because of degree 2 and a neighboor aswell
    n0 = 0 # number of vertices deleted because of deg 0
    while flag:
        nv = len(graph.degree())
        to_del = []
        for i in range(nv):
            if graph.degree(i) == 0:
                to_del.append(i)
                n0+=1
            if graph.degree(i)==1:
                to_del.append(i)
                n1 +=1
            if graph.degree(i) == 2:
                K = graph.neighborhood([i])
                for j in range(len(K)):
                    if graph.degree(j)==2 and j !=i:
                        n22 +=1
                        to_del.append(i)
                        to_del.append(j)

        graph.delete_vertices(to_del)
        if to_del == []:
            flag = False    
    
    return graph

#better visual style to visualize vertices and their degrees        
color_dict = {2: '#FF0000', 3: '#0000FF', 1:'#000000', 4: '#00FF00' }

def are_neighbours(M, i1, i2, j1, j2):
    '''
    determines if i and j are adjacent in M.
    i1, j1, .. are vertices of the graph.
    '''
    return (i1 == j1 or i1 == j2 or i2 == j1 or i2 == j2) and (M[i1][i2]!=0) and (M[j1][j2]!=0) 

def base_convert(i, b):
    result = []
    while i > 0:
            result.insert(0, i % b)
            i = i // b
    return result

def hard_edge_col(graph):
    '''
    starts by coloring all the edges with three colors, then checks 
    if the coloring is proper (ie two edges with same color share 
    no common end point)
    '''
    #maximum number of colorations to be tested is 3**n; n being the number
    # of edges. Given the problem you can assume n ~ 3 nV.
    Mpure = graph.get_adjacency() #adjacency matrix

    n = 0
    for mi in Mpure:
        n+=sum(mi)
    n//2 # number of edges

    case = 0
    
    for i in range(3**n -1):
        #case selection
        case = base_convert(i, 3)
        
        #coloration
        Mcopy = copy.copy(Mpure)
        xtmp = 0 #number of edges colored
        for i in range(len(Mpure)):
            for j in range(i):
                if Mpure[i][j]!=0:
                    Mcopy[i][j] = case[xtmp]
                    xtmp+=1   
    
        #proper coloration verification
        for i in range(len(Mpure)):
            for j in range(i):
                #TODO: here it is not over
                return 0
                
    

# setup toolbar
def toolbar():
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['


## MAIN

#toolbar()

for i in range(nG):
    #print('graph n°'+str(i)+': ', end = "")
    g, elements = special_graph(nV, omega, delta, elementsForPlot=True)
    plot2D(elements, mode = 'nat')
    igraph.plot(g, "images/SU_om2_ksip4/natgraph_"+str(i)+'.png')
    #g = epuration(g)
    #degs = g.degree()
    #igraph.plot(g, "images/SU_om2_ksip4/puregraph_"+str(i)+'.png',vertex_color = [color_dict[v] for v in degs])
    
    #g = rid_neighboors2(g)
    #degs = g.degree()
    #igraph.plot(g, "images/SU_om2_ksip4/graph_minus2_"+str(i)+'.png',vertex_color = [color_dict[v] for v in degs])

    #sys.stdout.write("-")
    #sys.stdout.flush()