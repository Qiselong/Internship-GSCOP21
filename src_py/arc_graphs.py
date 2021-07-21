# Idead: create some random arc-graph in order to get ideas.

# imports

import matplotlib.pyplot as plt
import igraph
import random
import numpy as np
import sys

#some parameters

nG = 10
nV = 200
scale= 1
modeG = 'full'
size = 5 #relative parameter for custom plot 
accuracy = 200 #accuracy for custom plot


def main():
    mode_intersection = modeG
    g= intersection(arc_elements(nV), mode =modeG)


def arc_elements(n, scale = 1):
    '''
    generates n arc-like elements and returns them as a list.
    each element is a list [h, t] consisting of head and tail point.
    to prevent the element of getting too big, we use a normal law of scale 'scale'. 
    We first pick the head value in [0, 2.\pi[ then t:= abs(N(0, scale)) + h
    small scale (<=1) is advised.
    '''

    elements = []
    for i in range(n):
        h = random.random()*2*np.pi
        t = h + abs(random.normalvariate(0,sigma=scale))
        elements.append([h, t])
    
    return elements

def is_intersecting(ei, ej):
    '''
    ei, ej: two elements under arc_elements format: [hi, ti] & [hj, tj]
    returns a boolean depending if the arcs are intersecting or not.
    method: first compute if point 2\pi belongs to them:
    if 2: return True
    if 0: treat them as default intervals (see previous works)
    if 1: split the one including 2\pi in two default intervals. return an OR
    '''

    
    dec = (ei[1]>np.pi) + (ej[1]>np.pi)
    if dec == 2:
        return True
    ih = ei[0] #head
    it = ei[1] #tail
    jh = ej[0]
    jt = ej[1]

    if dec == 0:
        if (jh>it) or (ih>jt):
            return False
        return True

    else:
        if jt > 2*np.pi:
            ih, it, jh, jt = jh, jt, ih, it
        #now the i interval is the one including 2pi
    it1 = np.pi
    ih1 = ih
    ih2 = np.pi 
    it2 = it
    if (jh>it1) or (ih1>jt):
        flag1 = False
    else: 
        return True
    if (jh>it2) or (ih2>jt):
        return False
    return True 

def intersection(elements, mode='graph', path= "default"):
    '''
    computes the intersection of elements depending on the mode.
    'default' mode: returns igraph graph.
    'igraph' mode: returns a graph & save an igraph picture under some name.
    'plt.plot' mode: custom matplotlib plot
    'plt.save' mode: custom matplotlib save
    'full' mode: custom matplotlib save & igraph save
    '''
    n = len(elements)
    g = igraph.Graph(n)
    for ei in range(n):
        for ej in range(ei):
            if is_intersecting(elements[ei], elements[ej]):
                g.add_edge(ei, ej)
    
    if mode == 'igraph':
        igraph.plot(g,"images/arc-graphs/"+path+".png")
        return g

    if mode == 'default':
        return g

    if mode=='plt.plot' or mode == 'plt.save' or mode=='full':
        custom_plot(elements, mode)
        if mode == 'full':
            igraph.plot(g,"images/arc-graphs/"+path+".png")
        return g

def color_dictionary(n):
    '''
    generates a random dictionary of colors of size n. 
    '''
    col_dict = {}
    for i in range(n):
        col_random = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        col_dict[i] = str(col_random) #rq= this is a different version of a function with the same name as here the keys are integers.
    return col_dict

def custom_plot(elements, mode):
    '''
    custom matplotlib.pyplot plot.
    3 mode admissible:
    'plt.plot' mode: custom matplotlib plot
    'plt.save' mode: custom matplotlib save
    'full' mode: custom matplotlib save 
    '''


    #quick sort by size in order to have visually satisfaying result
    #dtype1 = [('left', float), ('right', float), ('diff', float)] #see: https://numpy.org/doc/stable/reference/generated/numpy.sort.html
    #LNP = np.array(elements, dtype = dtype1)
    #print(LNP[0])
    #for i in range(len(LNP)):
     #   LNP[i,2] = LNP[i,1]-LNP[i,0]
    #L = np.sort(LNP, order = 'diff')
    L = np.array(elements)

    #dictionary for randomized colors
    col_dict = color_dictionary(len(L))

    n =len(elements)
    step = size/n
    t = np.linspace(0, 1, accuracy, endpoint=False )
    for i in range(len(L)):
        theta = t*(L[i, 1]-L[i,0])+ L[i, 0]
        R_i = 1 + step*i
        X = R_i*np.cos(theta)
        Y = R_i*np.sin(theta)
        plt.plot(X, Y, col_dict[i])

    if mode == 'plt.plot' or mode == 'full':
        plt.show() 








main()