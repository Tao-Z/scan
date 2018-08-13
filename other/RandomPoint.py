import random
def point(N=0,M=1):
    a=[[0 for i in range(2)] for i in range(N)]
    for i in range(0,N):
        a[i][0]=round(M*random.random(),3)
        a[i][1]=round(M*random.random(),3)
    return a
