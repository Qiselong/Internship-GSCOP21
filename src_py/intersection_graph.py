# objective: have box like elements of R^d and plot the intersection graph.
# library used for plotting the graph: igraph
# in case i don't remember how to install it as i'm very bad at managing version/libraries: see https://igraph.org/python/#startpy
# all the elements are stored in an array called "elements"
# let a be an element of R^d. a consists in a list of size 2, each being a point. 
# a point itself if a list of size d. Example with d = 3, an element can be eA = [[0,0,0],[1,1,0.5]]. We always take eA[0][i] < eA[1][i] for all i.
import igraph

import random
import matplotlib.pyplot as plt

### BASIC IGRAH MANIPULATIONS (it was my first time using it)
#print(igraph.__version__)
#g = igraph.Graph()
#g.add_vertices(3)
#g.add_edges([(0,1), (0,2)])
#g2 = igraph.Graph.Tree(127,3)

#print(g2) hard to read that one
#igraph.plot(g2) "good" plot with basic options.

### PARAMETERS
d = 5 # dimension
n = 16 # number of elements
colorsX11 = ['#FF0000', '#00FFFF', '#000000', '#0000FF', '#8A2BE2', '#A52A2A', '#7FFF00', '#FF7F50', '#DC143C', '#B8860B', '#FF00FF', '#228B22', '#BEBEBE', '#00FF00','#CD5C5C', '#800000']

elements = [] # list of our elements

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
    return graph # i think it is unecessary.


def random_elements(n, d):
    '''
    create n random box_like elements of dimension d and return it as a list of the elements format.
    '''
    elements = []
    for i in range(n):
        e = [[],[]]
        for j in range(d):
            a = random.random()
            b = random.random()
            e[0].append(min(a,b))
            e[1].append(max(a,b))
        elements.append(e)
    return elements

def plot1D(elements):
    '''
    does the plot in the special case of 1D elements.
    '''
    for ei in range(len(elements)):
        e = elements[ei]
        plt.plot([e[0], e[1]],[ei*0.2, ei*0.2], color = 'b')
    plt.show()

def plotDD(elements, colors):
    '''
    does the plot in any dimension using the projection trick.
    '''
    fig, axs = plt.subplots(len(elements[0][0]))
    for di in range(len(elements[0][0])):
        for ei in range(len(elements)):
            e = elements[ei]
            axs[di].plot([e[0][di], e[1][di]],[ei*0.2, ei*0.2], color = colors[ei])
    plt.show()

elements = random_elements(n,d)
graph = igraph.Graph(n)

fill_edges(elements, graph)

## Some properties of the graph
print("\nClique number: ", graph.clique_number())
print("Maximal independent set: ", graph.independence_number())

## Some plots
plotDD(elements, colorsX11)
igraph.plot(graph, vertex_color = colorsX11)