# Idead: create some random arc-graph in order to get ideas.

# imports

import matplotlib.pyplot as plt
import igraph
import random
import numpy as np
import sys

#some parameters

nG = 10
nV = 30
scale= 1
modeG = 'igraph'


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
        out = igraph.plot(g)
        out.save( "images/arc-graphs/"+path+".png")
        return g

    if mode == 'default':
        return g




main()