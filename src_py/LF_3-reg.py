#objective: look for all 3-regular graphs of size 8.

import numpy as np
from collections import Counter
from itertools import permutations
import igraph

# how does the loop works?
# I have a list called Astack; each element is a list of two things:
# 1st is a matrix; second a integer
# integer: -1 means it's no use to keep working on the matrix as it can't work (not enough room for 1s for instnace)
#           1 means it is a correct case of application
#           0 means we can't tell yet
# 
# a while loop is running as long as we have some 0s inside. 
# 
# TREATMENT:
# will do as:
# while flag = true:
# flag = false
# flag_i, A, Message= (treatment fctn)
# A = Sym(A)
# error_dect = check_col, check_liin(A)
# if error_dect : 
#   flag = true
#      


def main():
    A,message = init()
    print(message)
    Astack = [[A, 0]]
    worktodoB, index = worktodo(Astack)
    while worktodoB:
        print("wokr: ", worktodoB)
        Bstack = treatment(Astack[index][0])
        statestack = [Astack[i][1] for i in range(len(Astack))]
        if Bstack[0][1] == 0:
            
            Astack = Astack + Bstack
        else:
            Astack[index] = Bstack[0]
        worktodoB, index = worktodo(Astack)
    #print(Astack)
    print(Astack)
    c=0
    goodStack = []
    for AX in Astack:
        A = AX[0]

        if np.count_nonzero(A==1) == 24:
            c+=1
            goodStack.append(post_treatment(A))
    
    print(" a total of " + str(c) + " matrixes shoud be observed.")
    
    for i in range(len(goodStack)):
        path = "Internship-GSCOP21/images/k-reg-all-3-8/"+str(i+1)+".png"
        print(path)
        if i == 9: 
            print(goodStack[i])
        #graph = igraph.Graph.Adjacency( np.ndarray.tolist((goodStack[i] > 0)), mode='undirected')
        #out = igraph.plot(graph, path)


    
def post_treatment(A):
    '''
    returns A post-treated; ie all the -1 are 0 now.
    output format: A.
    '''
    for i in range(8):
        for j in range(8):
            if A[i,j]==-1:
                A[i,j]=0
    return A
    
    

def worktodo(Astack):
    ''' 
    determines if the stack requires more work to do or not. 
    return bool, index
    if bool = True, index is a matrix where there is work to be done.    
    '''
    for i in range(len(Astack)):
        
        if Astack[i][1] == 0:
            return True, i
    return False, -1
    
    
def treatment(A):
    '''
    treat the matrix A as much as possible using availables functions.
    returns [[A, int]]. 
    int = -1 : the matrix is no use. 
    int = 1: the matrix is done
    int = 0: is a list of elements. ( a stack) as we had to make a choice. 
    '''
    flag = True

    while flag == True:
        flag = False

        flag1, flag2, A, message = forbid(A)
        A, flag11 = sym(A)
        print(message)
        
        #A, flag2 , message = fill_lin(A)
        #A = sym(A)
        #print(message)
        
        A, flag3 , message = fill_col(A)
        
        A, flag12 = sym(A)
        print(message)

        flag = flag2 or flag3

        flag_col, message = check_col(A)
        print(message)

        if flag_col == False or flag12 == False or flag11 == False or flag1 == False:
            return([[A, -1]])

    if np.count_nonzero(A == 1) == 24: #in that case the matrix has enough 1s; and not too much has it passed the flag_cols/lins test
        return([[A, 1]])

    else:
        for i in range(8):
            if np.count_nonzero(A[i]==0)>0:
                print("Choice made on col "+ str(i))
                Astack = choice(A, i)
                out = []
                for x in range(len(Astack)):
                    out.append([Astack[x], 0])
                return out





def sym(A):
    '''
    Symetrize the matrix A.
    Returns A, bool
    '''
    for i in range(8):
        for j in range(8):
            if A[i,j]*A[j,i] <0 : #ie they have been assigned to different signs (not 0) which is a failure
                return A, False
            else:
                d = A[i,j]+A[j,i]
                A[i,j], A[j,i] = int(d/max(1, abs(d))), int(d/max(1, abs(d)))
    return A, True

def check_col(A):
    '''
    check if all the cols of A are valid; ie no more than 5 -1 and no more than 3 1.
    '''
    
    for i in range(8):
        counter = Counter(np.ndarray.tolist(A[i]))
        m1, p1 = counter[-1], counter[1]
        
        if m1 > 5 or p1 > 3:
            return False, "Col. error: "+ str(i) + "."
    return True, "Col check: ok."

def check_lin(A):
    '''
    check if all the lines of A are valid; ie no more than 5 -1 and no more than 3 1.
    '''
    
    for i in range(8):
        counter = Counter(np.ndarray.tolist(A[i]))
        m1, p1 = counter[-1], counter[1]
        if m1 > 5 or p1 > 3:
            return False, "Lin. error: " + str(i) + "."
    return True, "Lin. check: ok."

def init():
    '''
    return a matrix of size 8 corresponding to the correct size, with correct initial settings.
    format output: A, message
    '''
    A = np.zeros((8,8))
    A[0, 1] = 1
    A[0,2] = 1
    A[0,3] = 1
    A[1, 4]= 1
    A[1,5] = 1
    for i in range(8):
        A[i,i] = -1
    A, flag = sym(A)

    return A, "Matrix initialiazed."

def forbid(A):
    '''
    on every line, then every col, every time there is two 1s, check the associated numbers are not together (to prevent triangles) and put "-1" where needed.
    returns: bool, bool, A, message. If an error is detected (ie there should be a -1 but there is a 1 immediatly return a False, A, str)
    1st bool is error detection; second is modification
    '''
    c0 = np.count_nonzero(A == 0)
    if c0 == 0:
        return False, False, A, "no modification made by forbid as A is already complete."

    for i in range(8):
        L = []
        flag2 = False
        for j in range(8):
            if A[i,j]==1:
                L.append(j)

        if len(L)==2:
            a=L[0]
            b=L[1]

            if A[a,b] == 1 or A[b,a] == 1:
                return False, False, A, "Forbid error: "+ str(a)+", "+str(b)+'.'
            else:
                A[a,b] = -1
                A[b,a] = -1
                flag2 = True
                index = i

        elif len(L) == 3:
            a,b,c = L[0], L[1], L[2]

            if A[a,b] == 1 or A[b,a] == 1 or A[a,c] == 1 or A[c,a] == 1 or A[b,c] == 1 or A[c,b] == 1:
                return False,False, A, "Forbid error: "+ str(a)+", "+str(b)+ ', '+ str(c)+'.'
            else:
                A[a,b]= -1
                A[b,a]= -1
                A[a,c]= -1
                A[c,a]= -1
                A[b,c]= -1
                A[c,b]= -1
                flag2 = True
                index = i
    if flag2:
        message ="Forbid did modify A at index " + str(index)
    else:
        message = 'Forbid did no modification.'
    return True, flag2, A, message

def mod(A,i,j, val=1):
    '''
    Set i,j at val. val shall be 1 or -1.
    '''
    A[i,j] = val
    return A

def fill_col(A):
    '''
    If possible, will fill a col.
    flag: bool to modelize a modification was made.
    '''
    flag = False
    message = 'filled cols: '
    for i in range(8):
        counter = Counter(np.ndarray.tolist(A[i]))
        m1, p1 = counter[-1], counter[1]
        if m1 == 5 and p1 != 3:
            flag = True
            message += str(i) + ' '
            for j in range(8):
                if A[i,j] == 0:
                    mod(A, i,j)
        elif p1 == 3 and m1 !=5:
            flag = True
            message += str(i) + ' '
            for j in range(8):
                if A[i,j] == 0:
                    mod(A, i,j, -1)
    if flag:
        return A, flag, message
    return A, flag, 'no modification by fill_col. (flag value: ' + str(flag) + ')'

def fill_lin(A):
    '''
    If possible, will fill a lin.
    flag: bool to modelize a modification was made.
    '''
    flag = False
    message = 'filled lins: '
    for j in range(8):
        m1 = 0
        p1 = 0
        for i in range(8):
            m1 += -1&A[i,j]
        if m1 == 5:
            flag = True
            message += str(i) + ' '
            for i in range(8):
                if A[i,j] == 0:
                    mod(A, i,j)
        if p1 == 3:
            flag = True
            message += str(i) + ' '
            for i in range(8):
                if A[i,j] == 0:
                    mod(A, i,j, -1)
        
    if flag:
        return A, flag, message
    return A, flag, 'no modification by fill_lin.'

def choice(A, i):
    '''
    makes a choice for the i-th line. 
    return a list a matrix. The i-th line must have at least an ambiguity, for instance 4 -1 and 2 1. 
    The ambiguity is not checked in this function. 
    '''
    L= []
    m1 = 0
    p1 = 0


    L = np.ndarray.tolist(A[i])
    counter= Counter(L)

    perm_list = [1]*(3-counter[1]) + [-1]*(5-counter[-1])
    p = [list(p) for p in permutations(perm_list)]

    # remove duplicates
    new_p = []
    for elem in p:
        if elem not in new_p:
            new_p.append(elem)
    p = new_p
   


    out_lists = []
    for x in range(len(p)):
        out_lists.append([int(i) if i!=0 else p[x].pop() for i in L])
    n = len(out_lists)
    #return(out_lists)

    Astack=[]
    for x in range(n):
        A[i] = np.array(out_lists[x])
        Astack.append(np.array(A, copy=True))
    
    return Astack

main()