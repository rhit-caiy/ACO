from random import randint,shuffle
from time import time

n=100#vertex number
antnum=n#number of ants in one generation, update pheromone every antnum ants
generationnum=n*2#total ant generation number
rou=1/n#pheromone decrease every generation
q=n#amount of pheromone one ant have
initialPheromone=antnum*q/n/(n-1)#initial concertration on paths, should >0 for random
#pheromone attractivity
alpha=1
#distance attractivity
beta=7

def distance(a,b):
    return sum([(a[i]-b[i])**2 for i in range(len(a))])**0.5

def pathdistance(path):
    d=0
    for i in range(len(path)-1):
        d+=e[path[i]][path[i+1]]
    return d

def validpath(path):
    if sorted(path)==[0]+[i for i in range(n)]:
        print(True)
    else:
        print(False)

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
        

#input: number of vertex, range in those dimension as 2D array, minimum interval
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
    print(v)
    e=[[0 for i in range(n)] for j in range(n)]#edges
    for i in range(n):
        for j in range(n):
            e[i][j]=((v[i][0]-v[j][0])**2+(v[i][1]-v[j][1])**2)**0.5
    availablelist=[i for i in range(1,n)]
randomedge(n,[[0,1000],[0,1000]],10)

#returns: best path, corresponding distance, totaltime, time for each round, solution of each round
#O(n^2*antnum*generationnum)
def ACO(v,e,antnum,generationnum,rou,q,initialPheromone,alpha,beta):
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
        t=time()
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
        if generationbestdistance<bestdistance:
            bestdistance=generationbestdistance
            bestpath=generationbestpath
        times.append(time()-t)
        # if g%100==0:
        #     print(g,bestdistance)
    
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance

#can be treated as brute force
#O(num*n)
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

#O(num*n^2)
def twoopt(v,e,num):
    times=[]
    bestpath=[]
    bestdistance=sum((max(i) for i in e))
    historydistance=[]
    tstart=time()
    for g in range(num):
        t0=time()
        path=availablelist.copy()
        shuffle(path)
        path.append(0)
        path.insert(0,0)
        d=pathdistance(path)
        while 1:
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
                            break
                if reduced:
                    break
                            
            if not reduced:
                break
        
        if d<bestdistance:
            bestdistance=d
            bestpath=path
        historydistance.append(d)
        # print(d)
        
        t1=time()
        times.append(t1-t0)
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance

#O(num*n^3)
def threeopt(v,e,num):
    times=[]
    bestpath=[]
    bestdistance=sum((max(i) for i in e))
    historydistance=[]
    tstart=time()
    for g in range(num):
        t0=time()
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
                                break
                            elif d2<d0:
                                path=path[:i+1]+path[j+1:k+1][::-1]+path[i+1:j+1]+path[k+1:]
                                d=pathdistance(path)
                                reduced=1
                                break
                            
                    if reduced:
                        break
                if reduced:
                    break
                            
            if not reduced:
                break
        
        if d<bestdistance:
            bestdistance=d
            bestpath=path
        historydistance.append(d)
        # print(g,d)
        
        t1=time()
        times.append(t1-t0)
    totaltime=time()-tstart
    return bestpath,bestdistance,totaltime,times,historydistance


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

#genetic algorithm, unable to cross chromosomes, just mutation and selection
#O(n*generationnum*chromosomenum)
def geneticalgorithm(v,e,chromosomenum,generation,mutatenum,selection):
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
        #selection
        #index 0 is reserved for best
        bestc=chromosomes[lengths.index(min(lengths))]
        nextgenerationindex=weightedrandom([(bestdistance/i)**selection for i in lengths],chromosomenum-1)
        chromosomes=[bestc]+[chromosomes[i] for i in nextgenerationindex]
        #mutation, change 2 edge currently
        for c in range(1,chromosomenum):
            for a in range(mutatenum):
                i,j,k=sorted((randint(1,n),randint(1,n),randint(1,n)))
                chromosomes[c]=chromosomes[c][:i]+chromosomes[c][j:k]+chromosomes[c][i:j]+chromosomes[c][k:]       
            
        lengths=[pathdistance(c) for c in chromosomes]
        if min(lengths)<bestdistance:
            bestdistance=min(lengths)
            bestpath=chromosomes[lengths.index(bestdistance)]
        # print(min(lengths))
        historydistance.append(min(lengths))
        # print(chromosomes)
        # if g%100==0:
        #     print(g,bestdistance)
        
    totaltime=time()-tstart
    # print(bestdistance,lengths)
    return bestpath,bestdistance,totaltime,times,historydistance

'''
# print(random(v,e,10000)[1])
print(twoopt(v,e,10)[1])
print(threeopt(v,e,2)[1])
# print(greedy(v,e)[1])
# print(Prim(v,e)[1])
# print(Kruskal(v,e)[1])
# print(geneticalgorithm(v,e,1000,1000,1,64)[1])
# print()
print(ACO(v,e,antnum,100,rou,q,initialPheromone,alpha,beta)[1])
'''


# print("brute force")
# print(random(v,e,int(1000000/n))[1])
# print("greedy")
# print(greedy(v,e)[1])
# print("Prim")
# print(Prim(v,e)[1])
# print("Kruskal")
# print(Kruskal(v,e)[1])

# print("2-opt")
# print(twoopt(v,e,int(10000/n))[1])
# print("3-opt")
# print(threeopt(v,e,int(500/n))[1])
# print("GA")
# print(geneticalgorithm(v,e,int(100000/n),n*10,1,64)[1])


# print("ACO")
# acoresults=[[0 for i in range(10)] for i in range(10)]
# for i in range(2):
#     for alpha in range(1,4):
#         for beta in range(1,8):
#             ACOresult=ACO(v,e,n,generationnum,rou,q,initialPheromone,alpha,beta)
#             print(i,alpha,beta,ACOresult[1])
#             acoresults[alpha][beta]+=ACOresult[1]
# for b in range(1,8):
#     for a in range(1,4):
#         print("{:<8d}".format(int(acoresults[a][b])),end="")
#     print()
    
'''
t1=time()
n=100
print(n)
randomedge(n,2,[[0,1000],[0,1000]],10)
ACO(v,e,10,10,0.1,10,1,1,1)
t2=time()
n=200
print(n)
randomedge(n,2,[[0,1000],[0,1000]],10)
ACO(v,e,10,10,0.1,10,1,1,1)
t3=time()
n=400
print(n)
randomedge(n,2,[[0,1000],[0,1000]],10)
ACO(v,e,10,10,0.1,10,1,1,1)
t4=time()
print(t2-t1,t3-t2,t4-t3)

'''
results=[]
strings=["brute force", "greedy", "Prim", "Kruskal", "2-opt", "3-opt", "Genetic algorithm", "ACO"]
print(strings[0])
results.append(random(v,e,600000))
print(results[0][1],results[0][2],"s")
print(strings[1])
results.append(greedy(v,e))
print(results[1][1],results[1][2],"s")
print(strings[2])
results.append(Prim(v,e))
print(results[2][1],results[2][2],"s")
print(strings[3])
results.append(Kruskal(v,e))
print(results[3][1],results[3][2],"s")
print(strings[4])
results.append(twoopt(v,e,int(12000/n)))
print(results[4][1],results[4][2],"s")
print(strings[5])
results.append(threeopt(v,e,int(20000/n**2)))
print(results[5][1],results[5][2],"s")
print(strings[6])
results.append(geneticalgorithm(v,e,1000,500,1,64))
print(results[6][1],results[6][2],"s")
print(strings[7])
results.append(ACO(v,e,int(5000/n),200,rou,q,initialPheromone,alpha,beta))
print(results[7][1],results[7][2],"s")


import matplotlib.pyplot as plt
import numpy as np
#brute force, greedy, Prim, Kruskal, 2-opt, 3-opt, Genetic algorithm, ACO
fig, axs = plt.subplots(nrows=3, ncols=3, constrained_layout=True)
for i in range(3):
    for j in range(3):
        plt.subplot(3,3,3*i+j+1)
        plt.scatter(np.array([vx[0] for vx in v]),np.array([vy[1] for vy in v]),s=2,c='#000000')
        if i==2 and j==2:
            break
        plt.plot(np.array([v[vx][0] for vx in results[3*i+j][0]]),np.array([v[vy][1] for vy in results[3*i+j][0]]))
        plt.title(strings[3*i+j])
        plt.text(0,1050,str(round(results[3*i+j][1],6)))
