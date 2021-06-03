import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


tmp4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
tmp3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def toMatrix(case):
    #next section is identical to case_observation
    M = numpy.zeros((10,10), dtype = int)
     
    indexes = [(0, 1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

    for i in range(len(case)):
        ip, jp = indexes[i]
        i,j = fill( ip, jp , case[i])
        M[i,j] = 1
    M = numpy.maximum(M, M.transpose()) #symmetrize the matrix

    return M


def fill(i,j,k):
    # i'm 200% too lazy to explain how i come up with this and i will 300% regret it later
    if k == 0:
        return i,j
    if k == 1:
        return i, j+5
    if k == 2:
        return i+5, j+5
    return i+5, j

def Cycle4(depth, visited, current, M):
    '''
    M: adjacency matrix
    current: integer, index of where we currently are
    depth: integer. ends at 0
    visited: list of where we can't go
    '''

    if depth == 0:
        if visited[0]==visited[-1]:
            return True
        return False
    # if does not work we must create a list available of node we can travel to (we can't go to a node we already visited; so if the list turn out to be empty: retrun false)
    available = []
    for i in range(10):
        
        if M[current, i]==1 and not(i in visited) or (i==visited[0] and depth ==1): #complicated way to say it but "it just works!"
            
            available.append(i)

    #print("visited: ", visited, "\navailables: ", available, "\ndepth:", depth)
    if len(available) == 0:
        return False
    flag = False
    for destination in available:
        
        flag = flag or Cycle4(depth-1, visited+[destination], destination, M)
    return flag




M4 = toMatrix(tmp4)
print(M4)

for startpoint in range(10):
    print("\nStart Point: ", startpoint)
#startpoint = 2
    print(Cycle4(4, [startpoint], startpoint, M4))









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

case_study(tmp4)