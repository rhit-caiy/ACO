from random import randint
from tkinter import Tk,Canvas
from time import sleep,time

import matplotlib.pyplot as plt
#ACO2 for ACO animated display

window=Tk()
canvas=Canvas(window,bg="#FFFFFF",width=1440,height=810)
window.title("ACO")

n=1024#vertex number
antnum=int(10000/n)#number of ants in one generation, update pheromone every antnum ants
generationnum=int(n**0.5)#total ant generation number, would be n*2 if no ant path optimization
rou=1/n#pheromone decrease every generation
q=n#amount of pheromone one ant have
initialPheromone=antnum*q/n/(n-1)#initial concertration on paths, should >0 for random
#pheromone attractivity
alpha=1
#distance attractivity
beta=7

def pheromonecolor(v,maxvalue):
    value=int((1-v/maxvalue)*255)
    colorvalue=hex(value)[2:]
    if len(colorvalue)==1:
        colorvalue="0"+colorvalue
    return "#"+colorvalue*3

def updatetext(g,k,bestdistance):
    canvas.delete("text")
    canvas.create_text(400,20,text="generation "+str(g+1)+"/"+str(generationnum)+"    ant "+str(k+1)+"/"+str(antnum)+"    "+"min distance "+str(bestdistance),tag="text")
    canvas.update()
    return

def draw(v,tau,bestpath,bestdistance,g):
    maxpheromone=max([max(i) for i in tau])#max(200,max([max(i) for i in tau]))
    minpheromone=min([min(i) for i in tau])
    print("pheromone concertration range",round(maxpheromone,6),round(minpheromone,6))
    
    canvas.delete("all")
    if n<200:
        for i in range(n):
            for j in range(n):
                if i>j:
                    canvas.create_line(v[i][0],v[i][1],v[j][0],v[j][1],fill=pheromonecolor(tau[i][j],maxpheromone))
    for i in range(n):
        vertex=v[i]
        canvas.create_oval(vertex[0]-2,vertex[1]-2,vertex[0]+2,vertex[1]+2,fill="#000000")
        canvas.create_text(vertex[0],vertex[1]-10,text=str(i))
    canvas.create_oval(v[0][0]-4,v[0][1]-4,v[0][0]+4,v[0][1]+4,fill="#FF0000")
    canvas.update()
    updatetext(g,antnum-1,bestdistance)
    color="#FF0000"
    sleep(0.2)
    if g>-1:
        for i in range(n):
            canvas.create_line(v[bestpath[i]][0]-2,v[bestpath[i]][1]-2,v[bestpath[i+1]][0]-2,v[bestpath[i+1]][1]-2,fill=color)
    canvas.update()
    

def nextmove(available,v0,vtau,veta):
    l=list(available)
    weights=[(vtau[i]**alpha*veta[i]**beta) for i in l]
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
    
def pathdistance(path):
    d=0
    for i in range(len(path)-1):
        d+=e[path[i]][path[i+1]]
    return d

def pathtwoopt(oldpath):
    path=oldpath.copy()
    reduced=1
    #usually takes several iterations
    while reduced:
        reduced=0
        for i in range(n-2):
            for j in range(2,n):
                if j-i>1:
                    d0=e[path[i]][path[i+1]]+e[path[j]][path[j+1]]
                    d1=e[path[i]][path[j]]+e[path[i+1]][path[j+1]]
                    if d1<d0:
                        path=path[:i+1]+path[i+1:j+1][::-1]+path[j+1:]
                        reduced+=1
                        # print(reduced,"2-opt",c)
    return path

def moveonepoint(oldpath):
    path=oldpath.copy()
    #only iterate every combinations once
    for i in range(1,n):
        di=e[path[i-1]][path[i+1]]-e[path[i-1]][path[i]]-e[path[i]][path[i+1]]
        for j in range(1,n):
            if i-j<-1 or i-j>1:
                dj=e[path[i]][path[j]]+e[path[i]][path[j+1]]-e[path[j]][path[j+1]]
                if di+dj<0:
                    if i>j:
                        path.insert(j+1,path.pop(i))
                    else:
                        path.insert(j,path.pop(i))
                    break
    return path

def start():
    global v,e
    tstart=time()
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
    print(v)
    
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
    
    bestdistance=sum([max(i) for i in v])
    bestpath=[]
    generationbestdistances=[]
    bestdistances=[]
    draw(v,tau,bestpath,bestdistance,-1)
    for g in range(generationnum):
        t=time()
        tauupdate=[[0 for i in range(n)] for j in range(n)]#update at the end of ant generation, track the total number
        generationbestdistance=n*10000
        generationbestpath=[]
        for k in range(antnum):
            d=0#record the ant distance
            path=[0]#record the path
            available=set([i for i in range(1,n)])#not travelled vertices from index 1 to n-1
            v0=0#current vertex
            for i in range(n-1):
                v1=nextmove(available,v0,tau[v0],eta[v0])#next vertex
                available.remove(v1)
                path.append(v1)
                d+=e[v0][v1]
                v0=v1
            path.append(0)
            d+=e[v0][0]
            
            #afterward optimization for each ant
            path=moveonepoint(pathtwoopt(path))#
            d=pathdistance(path)#
            
            for i in range(n):
                tauupdate[path[i]][path[i+1]]+=q/d
            if d<generationbestdistance:
                generationbestdistance=d
                generationbestpath=path
            updatetext(g,k,bestdistance)
            
        #update pheromone
        for i in range(n):
            for j in range(n):
                if i>j:
                    tau[i][j]=tau[j][i]=(1-rou)*tau[i][j]+tauupdate[i][j]+tauupdate[j][i]
            tau[i][i]=0
            tau[i][i]=sum(tau[i])/(n-1)#remove diagonal
        print("generation",g," generation best",round(generationbestdistance,6),"time",round(time()-t,6),"s")
        generationbestdistances.append(generationbestdistance)
        if generationbestdistance<bestdistance:
            bestdistance=generationbestdistance
            bestpath=generationbestpath
        bestdistances.append(bestdistance)
        draw(v,tau,bestpath,bestdistance,g)
        
    print(bestdistance,bestpath)
    print("total time",round(time()-tstart,6),"s")
    plt.plot(generationbestdistances,"")
    plt.plot(bestdistances,"r")
    plt.ylabel("distance")
    plt.xlabel("generation")
    plt.grid()
    plt.show()

running=0
def click(coordinate):
    global running
    if not running:
        running=1
        start()
        running=0
    
canvas.bind("<Button-1>",click)
canvas.pack()
window.mainloop()
