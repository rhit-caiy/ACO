from random import randint
from tkinter import Tk,Canvas
# from time import sleep

window=Tk()
canvas=Canvas(window,bg="#FFFFFF",width=1440,height=810)
window.title("ACO")

n=100#vertex number
antnum=10#number of ants in one group, update pheromone every antnum ants
antgroupnum=100#total ant group number
initialPheromone=100#initial value should greater than 0 for random
rou=0.01#pheromone decrease every group
q=10000#amount of pheromone one ant have
#used for probability adjustment
alpha=4
beta=3

v=[]#vertices, first one would be the ant net


for i in range(n):
    while 1:
        x,y=(randint(50,1400),randint(50,750))
        num=0
        for vertex in v:
            if ((x-vertex[0])**2+(y-vertex[1])**2)**0.5<10:
                num=1#avoid two points too close
                break
        if num==0:
            break
    v.append((x,y))

e=[[i for i in range(n)] for j in range(n)]#edges
for i in range(n):
    for j in range(n):
        e[i][j]=((v[i][0]-v[j][0])**2+(v[i][1]-v[j][1])**2)**0.5

tau=[[initialPheromone for i in range(n)] for j in range(n)]#pheromone
eta=[[0 for i in range(n)] for j in range(n)]
for i in range(n):
    for j in range(n):
        if i!=j:
            eta[i][j]=1/e[i][j]#1/d

def nextmove(available,v0,vtau):
    l=list(available)
    weights=[(vtau[i]**alpha*eta[v0][i]**beta) for i in l]
    mul=100/min(weights)#let minimum weight to be 100
    weights=[i*mul for i in weights]
    r=randint(0,int(sum(weights)+1))
    i=0
    for weight in weights:
        r-=weight
        if r<=0:
            return l[i]
        i+=1
    else:
        return l[-1]





bestdistance=n*10000
bestpath=[]
for g in range(antgroupnum):
    tauupdate=[[0 for i in range(n)] for j in range(n)]#update at the end of ant group, track the total number
    groupbestdistance=n*10000
    groupbestpath=[]
    for k in range(antnum):
        d=0#record the ant distance
        path=[0]#record the path
        available=set([i for i in range(1,n)])#not travelled vertices from index 1 to n-1
        v0=0#current vertex
        for i in range(n-1):
            v1=nextmove(available,v0,tau[v0])#next vertex
            available.remove(v1)
            path.append(v1)
            d+=e[v0][v1]
            v0=v1
        path.append(0)
        d+=e[v0][0]
        for i in range(n):
            tauupdate[path[i]][path[i+1]]+=q/d
        if d<groupbestdistance:
            groupbestdistance=d
            groupbestpath=path
        
    #update pheromone
    for i in range(n):
        for j in range(n):
            if i>j:
                tau[i][j]=tau[j][i]=(1-rou)*tau[i][j]+tauupdate[i][j]+tauupdate[j][i]
    print("group",g," ",groupbestdistance)
    if groupbestdistance<bestdistance:
        bestdistance=groupbestdistance
        bestpath=groupbestpath
        

print(bestdistance,bestpath)

for vertex in v:
    canvas.create_oval(vertex[0]-2,vertex[1]-2,vertex[0]+2,vertex[1]+2,fill="#000000")
canvas.create_oval(v[0][0]-2,v[0][1]-2,v[0][0]+2,v[0][1]+2,fill="#FF0000")
for i in range(n):
    canvas.create_line(v[bestpath[i]][0],v[bestpath[i]][1],v[bestpath[i+1]][0],v[bestpath[i+1]][1])
    
canvas.pack()
window.mainloop()



