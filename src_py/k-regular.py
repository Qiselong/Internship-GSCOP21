#objective: generations through igraph of k-regular graphs for observation & counterexample research.

#parameters:
planar = False
nV = 8 #note that nV must be even if k is odd
k = 3
name = 'images/k-regular/'+ '3_6' +'.png'
limit = 10000
mode = 'count'

#importations
import random
import igraph
import numpy as np

#comments: 
# about k=3

    #   I d=identified 


def main():
    if mode == 'generation':
        g = None
        while g == None:
            g = k_reg_generation(nV, k)
        igraph.plot(g, name)
    if mode == 'count':
        nCase = int(2**(nV*(nV-1)/2-1))
        s = 0
        for i in range(nCase):
            s+= case_study(case_generation(i, nV), k, nV)
        print(s)

## SECTION 1

def k_reg_generation(nV_tmp, k):
    '''
    generates and returns a k regular graphs according to the parameters.
    nV_tmp : number of vertices
    k: k
    note: if k is odd and so is nV, then nV is put at nV+1
    '''

    nV = nV_tmp
    if k%2 ==1 and nV_tmp%2 !=0:
        nV = nV_tmp +1
    
    g = igraph.Graph(nV)
    nE = nV*k/2

    #the choice thing is done with a list: say k is 3 and nV is 4; the list is [0,0,0, 1,1,1, 2,2,2,3,3,3]
    #every time we put an edge we remove two numbers from the list if the corresponding edge does not exists

    Choice = []
    for i in range(nV):
        Choice = Choice + [i]*k

    print(Choice)
    EdgesPicked = 0
    iteration = 0
    while Choice != [] :
        iteration +=1
        a = random.choice(Choice)
        b = random.choice(Choice)
        #print(Choice, a, b)
        if a != b and not(a in g.neighborhood(b,1)):
            Choice.remove(a)
            Choice.remove(b)
            g.add_edge(a,b)
        if iteration > limit:
            return None

    return g

#SECTION 2

#goal of this section is to write a script to count how much
# k-regular graphs of size nV are acceptable. 

#the idea is to represent a graph as an upper triangle matrix of size
# nV, nV. A case is a number in binary of size 2^(nV-1)
# a function verifies that the case is conform:
# enough edges on each line, etc.

#TODO Let A be the adjacency matrix of a graph. Then the graph is regular if and only if j = ( 1 , … , 1 ) {\displaystyle {\textbf {j}}=(1,\dots ,1)} {\textbf {j}}=(1,\dots ,1) is an eigenvector of A.

def case_study(M, k, nV):
    '''
    verifies that M correspond to a valid case of a k-regular graph.
    '''
    for i in range(nV):
        count = 0
        for j in range(i):
            count += M[i,j]
        if count != k:
            return False

    for j in range(nV):
        count = 0
        for i in range(j):
            count += M[i,j]
        if count != k:
            return False
    
    return True

#stolen code for the internet: 
def base_convert(i, b):
    result = []
    lmin = int(nV*(nV-1)/2)
    while i > 0:
            result.insert(0, i % b)
            i = i // b
    return [0]*(lmin - len(result)) + result

def case_generation(case, nV):
    '''
    return an array corresponding to the case.
    '''
    caseB = base_convert(case, 2)
   
    M = np.zeros((nV, nV))
    for i in range(nV):
        for j in range(i):
            #print(i, j, int(j*(j-1)/2 +i))
            M[i,j] = caseB[int(j*(j-1)/2 +i)] #for more details about this formula: subscribe to my religious newsletter

    return M + M.transpose()

# EXECUTION
main()