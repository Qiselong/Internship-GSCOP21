import matplotlib.pyplot as plt
import numpy as np
import random


# Algorithmic illustration of Gallai's proof that \nu = \tau for an interval graph

## Method:
# We will store an interval as a list of 3 elements: [float left-end, float right-end, string color]
# all intervals will be inside a sole list and we will plot them with the plot_intervals function.

#adjustment variable:
space = 0.2     #space between intervals
n = 40       #number of intervals

def plot_intervals(L):
    red = 0 #how much red intervals?
    for i in range(len(L)):
        interval = L[i]
        plt.plot([interval[0], interval[1]], [space*i, space*i], interval[2])
        if interval[2] != 'k':
            red +=1
    plt.title("Transversal set with " + str(red)+" points")
    plt.show()
    
def generate_intervals(n):
    '''
    generate n intervals of the format explained before. All intervals are 'black'.
    '''
    L = []
    for i in range(n):
        L.append([0,0,0])
        a = random.random()
        b = random.random()
        L[i] = (min(a,b), max(a,b), 'k')
    return L

def sort_intervals(L, method='right'):
    '''
    sort the intervals by the method end point
    '''
    dtype1 = [('left', float), ('right', float), ('color', 'U5')] #see: https://numpy.org/doc/stable/reference/generated/numpy.sort.html
    LNP = np.array(L, dtype = dtype1)
    L = np.sort(LNP, order = method)
    return L

def isin(a,b,x):
    '''
    return True iff a<x<b
    '''
    return a< x and x<b

def coloration(L, color = 'r'):
    '''
    coloration using the algorithm described in Gallai's proof.
    The disjoins intervals appear in 
    '''
    X=[]
    for i in range(len(L)):
        flag=False      #detection: is a xi in the i-th interval?
        for xi in X:
            if isin(L[i][0], L[i][1], xi):
                flag = True
        if flag == False: #then we have to add something to X
            X.append(L[i][1])
            L[i][2] = color
    return L

## Execution
plot_intervals(coloration(sort_intervals(generate_intervals(n))))
