import matplotlib.pyplot as plt
import numpy as np
import random


# Algorithmic illustration of Gallai's proof that \nu = \tau for an interval graph

## Method:
# We will store an interval as a list of 3 elements: [float left-end, float right-end, string color]
# all intervals will be inside a sole list and we will plot them with the plot_intervals function.

#adjustment variable:
space = 0.2     #space between intervals
n = 80       #number of intervals

def plot_intervals(L, title = ''):
    red = 0 #how much red intervals?
    for i in range(len(L)):
        interval = L[i]
        plt.plot([interval[0], interval[1]], [space*i, space*i], interval[2])
        if interval[2] != 'k':
            red +=1
    if title == '':
        plt.title(r'$\nu$' + '=' + str(red) + ' ; ' + str(len(L)) + " total sets")
    else:
        plt.title(title)
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
    dtype1 = [('left', float), ('right', float), ('color', 'U20')] #see: https://numpy.org/doc/stable/reference/generated/numpy.sort.html
    LNP = np.array(L, dtype = dtype1)
    L = np.sort(LNP, order = method)
    return L

def isin(a,b,x):
    '''
    return True iff a<x<b
    '''
    return a< x and x<b

def max_set(L, color = 'r'):
    '''
    find a maximal disjoint set using the algorithm described in Gallai's proof.
    It is equal to the hitting number.
    The disjoins intervals appear in red
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

colors16 = ['r', 'g', 'b', 'c', 'y', 'm', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red','tab:purple', 'tab:brown','tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def coloration(L, colors=colors16):
    '''
    L: list of intervals.
    colors: list of color names.
    Does the colloration following the second proof of Gallai.
    '''
    L = sort_intervals(L, 'left')
    col_used = 0 #number of color used
    for i in range(len(L)):
        #then we try to eliminate every color by checking if L[i] is intersecting with an other interval of a given color. it
        flagcolored = False # 'have we figured out a coloration  for L[i] with already an used color?'
        for col in range(col_used):
            flag = False # 'has this color been used in an intersecting interval?'
            for j in range(i):
                if L[j][2] == colors[col] and isin(L[j][0], L[j][1], L[i][0]):
                    flag = True
                    break
            if flag == False:
                #then we can use color to color L[i]
                L[i][2] = colors[col]
                flagcolored=True
                break
            # if flag == True we check with an other interval
        if flagcolored == False:
            col_used +=1
            L[i][2] = colors[col_used]
    return L
        

            
## Execution
plot_intervals(max_set(sort_intervals(generate_intervals(n))))

plot_intervals(coloration(generate_intervals(15)), title='coloration using Gallai\'s algorithm')