from random import randint,shuffle
from time import time
#ACO4 for adjust details on code implement and further improvements

def distance(a,b):
    return sum([(a[i]-b[i])**2 for i in range(len(a))])**0.5

def pathdistance(path):
    d=0
    for i in range(len(path)-1):
        d+=e[path[i]][path[i+1]]
    return d

# def validpath(path):
#     if sorted(path)==[0]+[i for i in range(n)]:
#         print(True)
#     else:
#         print(False)

def weightedrandom(weights,num):
    if min(weights):
        mul=10000/min(weights)#let minimum weight to be 10000
    else:
        mul=1000000000000
    newweights=[i*mul for i in weights]
    result=[]
    total=int(sum(newweights))
    for i in range(num):
        r=randint(0,total)
        index=0
        for weight in newweights:
            r-=weight
            if r<=0:
                result.append(index)
                break
            index+=1
        else:
            result.append(len(weights)-1)
    return result
        
#input: number of vertex, range of dimensions in 2D array, minimum interval between any two vertices
def randomedge(n,ranges,interval):
    global v,e,availablelist
    v=[]#vertices, first one would be the ant net
    for i in range(n):
        while 1:
            coordinate=[]
            for i in range(len(ranges)):
                coordinate.append(randint(ranges[i][0],ranges[i][1]))
            num=0
            for vertex in v:
                if distance(coordinate,vertex)<interval:
                    num=1#avoid two points too close
                    break
            if num==0:
                break
        v.append(tuple(coordinate))
    #print(v)
    e=[[0 for i in range(n)] for j in range(n)]#edges
    for i in range(n):
        for j in range(n):
            e[i][j]=sum([(v[i][d]-v[j][d])**2 for d in range(len(ranges))])**0.5
    availablelist=[i for i in range(1,n)]

#returns: best path, corresponding distance, totaltime, time for each round, solution of each round
#O(n^2*antnum*generationnum)
def ACO(v,e,timelimit,antnum,generationnum,rou,q,initialPheromone,alpha,beta,antwiseopt,generationwiseopt):
    times=[]
    bestpath=[]
    maxdistance=sum((max(i) for i in e))
    bestdistance=maxdistance
    historydistance=[]
    tau=[[initialPheromone for i in range(n)] for j in range(n)]#pheromone
    eta=[[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j:
                eta[i][j]=1/e[i][j]#1/d
    tstart=time()
    for g in range(generationnum):
        tauupdate=[[0 for i in range(n)] for j in range(n)]#update at the end of ant generation, track the total number
        generationbestdistance=maxdistance
        generationbestpath=[]
        for k in range(antnum):
            d=0
            path=[0]
            available=availablelist.copy()
            v0=0
            for i in range(n-1):
                p=[(tau[v0][i]**alpha*eta[v0][i]**beta) for i in available]
                v1=available[weightedrandom(p,1)[0]]
                available.remove(v1)
                path.append(v1)
                d+=e[v0][v1]
                v0=v1
            path.append(0)
            d+=e[v0][0]
            if antwiseopt:
                path=moveonepoint(pathtwoopt(path))
                d=pathdistance(path)
            
            for i in range(n):
                tauupdate[path[i]][path[i+1]]+=q/d
            if d<generationbestdistance:
                generationbestdistance=d
                generationbestpath=path
        #update pheromone
        for i in range(n):
            for j in range(n):
                if i>j:
                    tau[i][j]=tau[j][i]=(1-rou)*tau[i][j]+tauupdate[i][j]+tauupdate[j][i]
            tau[i][i]=0
            tau[i][i]=sum(tau[i])/(n-1)#remove diagonal
        historydistance.append(generationbestdistance)
        if generationwiseopt:
            generationbestpath=moveonepoint(pathtwoopt(path))
            generationbestdistance=pathdistance(generationbestpath)
        if generationbestdistance<bestdistance:
            bestdistance=generationbestdistance
            bestpath=generationbestpath
        if (t:=time()-tstart)>timelimit:
            times.append(t)
            break
        times.append(t)
        
    
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance,g+1

def geneticalgorithm(v,e,timelimit,chromosomenum,generation,mutatenum,selection):
    chromosomes=[]
    lengths=[]
    for i in range(chromosomenum):
        chromosome=availablelist.copy()
        shuffle(chromosome)
        chromosome.append(0)
        chromosome.insert(0,0)
        chromosomes.append(chromosome)
        lengths.append(pathdistance(chromosome))
    bestdistance=min(lengths)
    bestpath=chromosomes[lengths.index(bestdistance)]
    times=[]
    historydistance=[]
    tstart=time()
    for g in range(generation):
        #selection, index 0 is reserved for best
        bestc=chromosomes[lengths.index(min(lengths))]
        #best has weight 1, others has their (length/best)**selection
        nextgenerationindex=weightedrandom([(bestdistance/i)**selection for i in lengths],chromosomenum-1)
        chromosomes=[bestc]+[chromosomes[i] for i in nextgenerationindex]
        #mutation, exchange 2 parts of chromosome
        for c in range(1,chromosomenum):
            for a in range(mutatenum):
                if randint(1,2)==1:
                    i,j,k=sorted((randint(1,n),randint(1,n),randint(1,n)))
                    chromosomes[c]=chromosomes[c][:i]+chromosomes[c][j:k]+chromosomes[c][i:j]+chromosomes[c][k:]
                else:
                    i,j=sorted((randint(1,n),randint(1,n)))
                    chromosomes[c]=chromosomes[c][:i]+chromosomes[c][i:j][::-1]+chromosomes[c][j:]
            
        lengths=[pathdistance(c) for c in chromosomes]
        if min(lengths)<bestdistance:
            bestdistance=min(lengths)
            bestpath=chromosomes[lengths.index(bestdistance)]
        historydistance.append(min(lengths))
        if (t:=time()-tstart)>timelimit:
            times.append(t)
            break
        times.append(t)
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance,g+1

#O(num*n^2)
def twoopt(v,e,timelimit,num,furtheropt):
    times=[]
    bestpath=[]
    bestdistance=sum((max(i) for i in e))
    historydistance=[]
    tstart=time()
    for g in range(num):
        path=availablelist.copy()
        shuffle(path)
        path.append(0)
        path.insert(0,0)
        d=pathdistance(path)
        reduced=1
        while reduced:
            reduced=0
            for i in range(n-2):
                for j in range(2,n):
                    if j-i>1:
                        d0=e[path[i]][path[i+1]]+e[path[j]][path[j+1]]
                        d1=e[path[i]][path[j]]+e[path[i+1]][path[j+1]]
                        if d1<d0:
                            path=path[:i+1]+path[i+1:j+1][::-1]+path[j+1:]
                            d=pathdistance(path)
                            reduced=1
                            
            if not reduced:
                break
        if furtheropt:
            path=moveonepoint(path)
            d=pathdistance(path)
        if d<bestdistance:
            bestdistance=d
            bestpath=path
        historydistance.append(d)
        if (t:=time()-tstart)>timelimit:
            times.append(t)
            break
        times.append(t)
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance,g+1

#O(num*n^3)
def threeopt(v,e,timelimit,num):
    times=[]
    bestpath=[]
    bestdistance=sum((max(i) for i in e))
    historydistance=[]
    tstart=time()
    for g in range(num):
        path=availablelist.copy()
        shuffle(path)
        path.append(0)
        path.insert(0,0)
        d=pathdistance(path)
        while 1:
            reduced=0
            for i in range(n-4):
                for j in range(2,n-2):
                    for k in range(4,n):
                        if j-i>1 and k-j>1:
                            d0=e[path[i]][path[i+1]]+e[path[j]][path[j+1]]+e[path[k]][path[k+1]]
                            d1=e[path[i]][path[j+1]]+e[path[j]][path[k+1]]+e[path[k]][path[i+1]]
                            d2=e[path[i]][path[k]]+e[path[i+1]][path[j+1]]+e[path[j]][path[k+1]]
                            if d1<d0:
                                path=path[:i+1]+path[j+1:k+1]+path[i+1:j+1]+path[k+1:]
                                d=pathdistance(path)
                                reduced=1
                            elif d2<d0:
                                path=path[:i+1]+path[j+1:k+1][::-1]+path[i+1:j+1]+path[k+1:]
                                d=pathdistance(path)
                                reduced=1
            if not reduced:
                break
        
        if d<bestdistance:
            bestdistance=d
            bestpath=path
        historydistance.append(d)
        if (t:=time()-tstart)>timelimit:
            times.append(t)
            break
        times.append(t)
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance,g+1

def pathtwoopt(oldpath):
    path=oldpath.copy()
    reduced=1
    while reduced:
        reduced=0
        for i in range(n-2):
            for j in range(2,n):
                if j-i>1:
                    d0=e[path[i]][path[i+1]]+e[path[j]][path[j+1]]
                    d1=e[path[i]][path[j]]+e[path[i+1]][path[j+1]]
                    if d1<d0:
                        path=path[:i+1]+path[i+1:j+1][::-1]+path[j+1:]
                        reduced=1
    return path

def moveonepoint(oldpath):
    path=oldpath.copy()
    reduced=1
    while reduced:
        reduced=0
        for i in range(1,n):
            di=e[path[i-1]][path[i+1]]-e[path[i-1]][path[i]]-e[path[i]][path[i+1]]
            for j in range(1,n):
                if i!=j:
                    dj=e[path[i]][path[j]]+e[path[i]][path[j+1]]-e[path[j]][path[j+1]]
                    if di+dj<0:
                        reduced=0
                        if i>j:
                            vertex=path.pop(i)
                            path.insert(j+1,vertex)
                        else:
                            vertex=path.pop(i)
                            path.insert(j,vertex)
                        break
    return path

n=4096#vertex number
antnum=int(10000/n)#number of ants in one generation, update pheromone every antnum ants
antnum=5
generationnum=int(n**0.5)#total ant generation number
rou=1/n#pheromone decrease every generation
q=n#amount of pheromone one ant have
initialPheromone=antnum*q/n/(n-1)#initial concertration on paths, should >0 for random
#pheromone attractivity
alpha=1
#distance attractivity
beta=7

randomedge(n,[[0,10000],[0,10000]],10)#randomedge(n,[[0,1000],[0,1000],[0,1000]],10) for 3 dimensions


# result=twoopt(v,e,5)#1 s n=512
# result=threeopt(v,e,1)#4 min n=512

infinity=10**10#arbitrary large number to hit time limit

functions=[twoopt]*2+[geneticalgorithm]+[ACO]*3
inputs=[[infinity,0],#0
        [infinity,1],#1
        [10,infinity,1,n],#2
        [antnum,infinity,rou,q,initialPheromone,alpha,beta,0,0],#3
        [antnum,infinity,rou,q,initialPheromone,alpha,beta,0,1],#4
        [antnum,infinity,rou,q,initialPheromone,alpha,beta,1,0]#5
        ]
names=["2-opt",
       "2-opt opt",
       "genetic algorithm",
       "ACO",
       "ACO generation-wise opt",
       "ACO ant-wise opt"]
colors=["r",
        "#FF8000",
        "g",
        "b",
        "#8000FF",
        "#FF00FF"]
run=[1,2,3,5]

# functions=[]
# inputs=[]
# names=[]
# run=[]


results=[]
timelimit=600

print(f"n = {n}, time limit = {timelimit}s")
print("{:<40}{:<20}{:<16}{:<10}".format("algorithm","distance","time/s","generation"))
for i in run:
    result=functions[i](v,e,timelimit,*inputs[i])
    print("{:<40}{:<20f}{:<16f}{:<10}".format(names[i],result[1],result[2],result[5]))
    results.append(result)

import matplotlib.pyplot as plt
for i in range(len(results)):
    plt.plot(results[i][3],results[i][4],colors[i])
