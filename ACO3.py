from random import randint,shuffle
# from tkinter import Tk,Canvas
from time import sleep,time

n=64#vertex number
antnum=n#number of ants in one generation, update pheromone every antnum ants
generationnum=n*2#total ant generation number
rou=1/n#pheromone decrease every generation
q=n#amount of pheromone one ant have
initialPheromone=antnum*q/n/(n-1)#initial concertration on paths, should >0 for random
#pheromone attractivity
alpha=1
#distance attractivity
beta=5

def distance(a,b):
    return sum([(a[i]-b[i])**2 for i in range(len(a))])**0.5

def pathdistance(path):
    d=0
    for i in range(len(path)-1):
        d+=e[path[i]][path[i+1]]
    return d

def weightedrandom(weights,num):
    mul=10000/min(weights)#let minimum weight to be 10000
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
        

#input: number of vertex, dimension, range in those dimension as 2D array, minimum interval
def randomedge(n,dimension,ranges,interval):
    global v,e
    v=[]#vertices, first one would be the ant net
    for i in range(n):
        while 1:
            coordinate=[]
            for i in range(dimension):
                coordinate.append(randint(ranges[i][0],ranges[i][1]))
            num=0
            for vertex in v:
                if distance(coordinate,vertex)<interval:
                    num=1#avoid two points too close
                    break
            if num==0:
                break
        v.append(tuple(coordinate))
    # v=[(267, 364), (78, 521), (428, 206), (1399, 118), (204, 689), (1322, 488), (396, 349), (1154, 609)]
    print(v)
    e=[[0 for i in range(n)] for j in range(n)]#edges
    for i in range(n):
        for j in range(n):
            e[i][j]=((v[i][0]-v[j][0])**2+(v[i][1]-v[j][1])**2)**0.5

randomedge(n,2,[[50,1400],[50,750]],10)



availablelist=[i for i in range(1,n)]
#returns: best path, corresponding distance, totaltime, time for each round, solution of each round

def ACO(v,e,antnum,generationnum,rou,q,initialPheromone,alpha,beta):
    times=[]
    bestpath=[]
    bestdistance=0
    return bestpath,bestdistance,times

#can be treated as brute force
def random(v,e,num):
    times=[]
    bestpath=[]
    bestdistance=sum((max(i) for i in e))
    historydistance=[]
    tstart=time()
    for i in range(num):
        t0=time()
        path=availablelist.copy()
        shuffle(path)
        path.append(0)
        path.insert(0,0)
        d=pathdistance(path)
        if d<bestdistance:
            bestdistance=d
            bestpath=path
        historydistance.append(d)
        
        t1=time()
        times.append(t1-t0)
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance

def twoopt(v,e,num):
    return

def threeopt(v,e):
    return


def greedy(v,e):
    maxedge=max((max(i) for i in e))*2
    ecopy=[i.copy() for i in e]
    for i in range(n):
        ecopy[i][i]=ecopy[i][0]=maxedge
    v0=v1=0
    path=[0]
    d=0
    tstart=time()
    for i in range(n-1):
        v1=ecopy[v0].index(min(ecopy[v0]))
        for j in range(n):
            ecopy[j][v1]=maxedge
        
        path.append(v1)
        d+=e[v0][v1]
        v0=v1
    d+=e[v1][0]
    path.append(0)
    totaltime=time()-tstart
    return path,d,totaltime,[totaltime],[d]

#only allow two end
def Prim(v,e):
    maxedge=max((max(i) for i in e))*2
    ecopy=[i.copy() for i in e]
    for i in range(n):
        ecopy[i][i]=maxedge
    available=set(availablelist)
    path=[0]*(n+1)
    v1=ecopy[0].index(min(ecopy[0]))
    ecopy[0][v1]=maxedge
    v2=ecopy[0].index(min(ecopy[0]))
    p1=1
    p2=n-1
    path[1]=v1
    path[n-1]=v2
    available.remove(v1)
    available.remove(v2)
    for i in range(n):
        ecopy[i][0]=ecopy[i][v1]=ecopy[i][v2]=maxedge
    ecopy[v1][0]=ecopy[v2][0]=maxedge
    
    tstart=time()
    for i in range(n-4):
        v1min=min(ecopy[v1])
        v2min=min(ecopy[v2])
        if v1min<v2min:
            v1new=ecopy[v1].index(v1min)
            v1=v1new
            for j in range(n):
                ecopy[j][v1]=maxedge
            available.remove(v1)
            p1+=1
            path[p1]=v1
        else:
            v2new=ecopy[v2].index(v2min)
            v2=v2new
            for j in range(n):
                ecopy[j][v2]=maxedge
            available.remove(v2)
            p2-=1
            path[p2]=v2
    path[p1+1]=available.pop()
    d=pathdistance(path)
    totaltime=time()-tstart
    return path,d,totaltime,[totaltime],[d]

#only allow connect while have <2 edge and acyclist until end
def Kruskal(v,e):
    maxedge=max((max(i) for i in e))*2
    ecopy=[i.copy() for i in e]
    for i in range(n):
        ecopy[i][i]=maxedge
    connection=[[] for i in range(n)]
    forests=[]
    tstart=time()
    for i in range(n):
        valid=0
        while not valid:
            minedge=maxedge
            v0=-1
            v1=-1
            for j in range(n):
                if min(ecopy[j])<minedge:
                    v0=j
                    v1=ecopy[j].index(min(ecopy[j]))
                    minedge=min(ecopy[j])
            ecopy[v0][v1]=maxedge
            ecopy[v1][v0]=maxedge
            valid=1
            for trees in forests:
                if (v0 in trees and v1 in trees) and i!=n-1:
                    valid=0
                    break
        modified=0
        i1=0
        
        for i in range(len(forests)):
            trees=forests[i]
            if (v0 in trees or v1 in trees) and modified:
                forests[i1]=forests[i1]|forests[i]
                forests.pop(i)
                break
            if v0 in trees or v1 in trees:
                trees.update((v0,v1))
                modified=1
                i1=i
        if not modified:
            forests.append(set((v0,v1)))
        connection[v0].append(v1)
        connection[v1].append(v0)
        if len(connection[v0])==2:
            for j in range(n):
                ecopy[j][v0]=maxedge
                ecopy[v0][j]=maxedge
        if len(connection[v1])==2:
            for j in range(n):
                ecopy[j][v1]=maxedge
                ecopy[v1][j]=maxedge
    path=[0]
    v0=v1=v2=0
    for i in range(n):
        if connection[v1][0]!=v0:
            v2=connection[v1][0]
        else:
            v2=connection[v1][1]
        path.append(v2)
        v0,v1=v1,v2
    d=pathdistance(path)
    totaltime=time()-tstart
    return path,d,totaltime,[totaltime],[d]

def astar(v,e):
    return

#genetic algorithm, unable to cross chromosomes, just mutation and selection
def geneticalgorithm(v,e,chromosomenum,generation,mutaterate):
    chromosomes=[]
    lengths=[]
    mutatenum=int(mutaterate*n)
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
        #selection
        # print("generation",g)
        if g%100==0:
            print(g,bestdistance)
        nextgenerationindex=weightedrandom([(bestdistance/i)**64 for i in lengths],chromosomenum)
        chromosomes=[chromosomes[i] for i in nextgenerationindex]
        #mutation, change 2 edge currently
        for c in range(chromosomenum):
            #for a in range(mutatenum):
            i,j,k=sorted((randint(1,n),randint(1,n),randint(1,n)))
            #chromosomes[c][i],chromosomes[c][j]=chromosomes[c][j],chromosomes[c][i]
            chromosomes[c]=chromosomes[c][:i]+chromosomes[c][j:k]+chromosomes[c][i:j]+chromosomes[c][k:]       
            
        lengths=[pathdistance(c) for c in chromosomes]
        if min(lengths)<bestdistance:
            bestdistance=min(lengths)
            bestpath=chromosomes[lengths.index(bestdistance)]
        # print(min(lengths))
        historydistance.append(min(lengths))
        # print(chromosomes)
        
    totaltime=time()-tstart
    # print(bestdistance,lengths)
    return bestpath,bestdistance,totaltime,times,historydistance

# greedyresult=greedy(v,e)
# print(greedyresult[1],pathdistance(greedyresult[0]))
# print(random(v,e,1000000)[1])

print(random(v,e,10000)[1])
print(greedy(v,e)[1])
print(Prim(v,e)[1])
print(Kruskal(v,e)[1])
print(geneticalgorithm(v,e,1000,1000,0.1)[1])
