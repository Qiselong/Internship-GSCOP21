import matplotlib.pyplot as plt
import numpy
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


from random import randint
## Problem: 
# 5 students go to the library (separatly). They arrive at a certain time, take a break for lunch at some time, come back later, then leave. 
# We know that every pair of student met at some point. Prove that there is a time where they were three of them in the library.

## Method:
# We will generate every possible graph representing the situation and will look for a 3-loop.
# The graph has 10 nodes. We denote them as A, a, B, b, ...
# capital letter = first shift; regular letter = second shift.
# we want a connection between every couple (A, a); (B, b), ...
# 
# there is 10 couples: AB AC AD AE BC BD BE CD CE DE, so we need 10 connections.
# we will store a choice for a connection in a 10 digit number in quaternal (3333333333 in base 4 is 1048575 in base 10),  for instnace:
# for the AB connection, 0 means AB, 1 means Ab, 2 means ab, 3 means aB. 


#stolen code for the internet: 
def base_convert(i, b):
    result = []
    while i > 0:
            result.insert(0, i % b)
            i = i // b
    return result

def fill(i,j,k):
    # i'm 200% too lazy to explain how i come up with this and i will 300% regret it later
    if k == 0:
        return i,j
    if k == 1:
        return i, j+5
    if k == 2:
        return i+5, j+5
    return i+5, j

def case_observation(case, verbose = False):
    '''
    take a list (case) and convert it in a matrix. Then upgrades to the power 3 and checks if there is a number =! 0 on the main diagonal.
    '''
    M = numpy.zeros((10,10))
     
    indexes = [(0, 1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

    for i in range(len(case)):
        ip, jp = indexes[i]
        i,j = fill( ip, jp , case[i])
        M[i,j] = 1
    M = numpy.maximum(M, M.transpose()) #symmetrize the matrix
    T3 = numpy.linalg.matrix_power(M, 3)    #3-cycle detection
    T5 = numpy.linalg.matrix_power(M,5)     #5-cycle detection

    if verbose:
        print(M, T3, T5)

    if numpy.trace(T3) != 0 or numpy.trace(T5 !=0): #ie there exists an odd-loop in the graph associated to M
        return True
    
# some tests
#r = randint(0, 1048575)
#rbase = base_convert(r, 4)
#print(r, rbase)
#while len(rbase) != 10:
 #   rbase = rbase + [0]
#case_observation(rbase)



## Next section is about plotting / was used to check what was missing in the automatic checking. Was useful to show that i forgot to check 4-cycles.
def case_study(case):
    #next section is identical to case_observation
    M = numpy.zeros((10,10))
     
    indexes = [(0, 1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

    for i in range(len(case)):
        ip, jp = indexes[i]
        i,j = fill( ip, jp , case[i])
        M[i,j] = 1

    coordinates= [[0 ,3 ,-3 ] ,[3 ,0 ,-3 ] ,[ 2,-3 ,-3 ] ,[-2 , -3, -3] ,[-3 ,0 ,-3 ],[0 ,3 ,3 ] ,[3 ,0 ,3] ,[ 2,-3 ,3 ] ,[-2 , -3, 3] ,[-3 ,0 ,3 ]  ]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for i in range(10):
        for j in range(10):
            if M[i,j] != 0:
                x = [coordinates[i][0], coordinates[j][0]]
                y = [coordinates[i][1], coordinates[j][1]]
                z = [coordinates[i][2], coordinates[j][2]]

                plt.plot(x,y,z, 'b')
    plt.show()

def cycle4(case):
    '''
    checks the existence of 4-cycles.
    '''
    #next section is identical to case_observation
    M = numpy.zeros((10,10))
     
    indexes = [(0, 1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

    for i in range(len(case)):
        ip, jp = indexes[i]
        i,j = fill( ip, jp , case[i])
        M[i,j] = 1

    ## TODO
    for index_start in range(10):
        MP = 4  #moves remaining
        visited = [index_start] #nodes visited
        current = index_start
        availables = []
        for i in range(10):
            if M[current, i] == 1 and not(M[current, i] in visited):
                availables.append(i) 
    return None



# Actual algorithm
anomalies=0
for i in range(1048575):
    case = base_convert(i, 4)
  # if the list in not long enough we add 0 on the left
    while len(case)!=10:
        case = [0] + case

    #now we look for odd-cycles
    if not case_observation(case, verbose=False): # at this point we are sure there is no
       #print("\nAnomaly: \n", case)
       #case_study(case) 
       anomalies +=1
print(anomalies)
