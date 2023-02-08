from random import randint
from tkinter import Tk,Canvas
from time import sleep
from itertools import permutations

window=Tk()
canvas=Canvas(window,bg="#FFFFFF",width=1440,height=810)
window.title("ACO1")

n=64
antnum=1000

def getrandomindex(availablepoints,information):
    weights=[]
    for i in availablepoints:
        weights.append(information[i]+n)#base probability
    total=sum(weights)
    r=randint(0,int(total+1))
    i=0
    for weight in weights:
        r=r-weight
        if r<=0:
            return availablepoints[i]
        i+=1
    else:
        return availablepoints[-1]

def densitycolor(v,maxvalue):
    value=int((1-v/maxvalue)*255)#color
    colorvalue=hex(value)[2:]
    if len(colorvalue)==1:
        colorvalue="0"+colorvalue
    color="#"+colorvalue*3
    return color
    
def draw(points,paths,ant,minp):
    canvas.delete("all")
    # maxinformation=max([max(i) for i in paths])
    canvas.create_line(0,10,ant/10,10)
    canvas.create_line(antnum/10,0,antnum/10,20)
    for i in range(n):
        # maxv=max(paths[i])
        for j in range(n):
            if i>j:
                maxinformation=max(max(paths[i]),max(paths[j]),1)
                canvas.create_line(points[i][0],points[i][1],points[j][0],points[j][1],fill=densitycolor(paths[i][j],maxinformation))
            # if paths[i][j]==maxv:
            #     canvas.create_line(points[i][0],points[i][1],points[j][0],points[j][1],fill="#000000")
    for point in points:
        if point==points[0]:
            canvas.create_oval(point[0]-4,point[1]-4,point[0]+4,point[1]+4,fill="#FF0000")
        else:
            canvas.create_oval(point[0]-4,point[1]-4,point[0]+4,point[1]+4,fill="#000000")
    x,y=points[0]
    for pointn in minp:
        point=points[pointn]
        x1,y1=point
        canvas.create_line(x,y,x1,y1,fill="#FF0000")
        x,y=x1,y1
    canvas.update()

def pathlength(path,distances):
    total=0
    for i in range(len(path)-1):
        total+=distances[path[i]][path[i+1]]
    return total

def start():
    print()
    permutationnum=4
    
    
    
    mind=n*1000
    minp=[]
    points=[]
    for i in range(n):
        #avoid too close
        while 1:
            x,y=(randint(50,1400),randint(50,750))
            num=0
            for p in points:
                if ((x-p[0])**2+(y-p[1])**2)**0.5<1000/n:
                    num+=1
            if num==0:
                break
        points.append((x,y))
    
    #n=len(points)
    distances=[[0 for i in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            distances[i][j]=((points[i][0]-points[j][0])**2+(points[i][1]-points[j][1])**2)**0.5
    #print(distances)
    paths=[[0 for i in range(n)] for i in range(n)]
    
    
    #use local optimize
    minp=[i for i in range(n)]+[0]
    mind=pathlength(minp,distances)
    while 1:
        newlen=mind
        newminp=[]
        for i in range(1,n):
            for j in range(1,n):
                if i<j:
                    newp=minp.copy()
                    newp[i:j+1]=newp[i:j+1][::-1]
                    if (l:=pathlength(newp,distances))<newlen:
                        newlen=l
                        newminp=newp.copy()
        for i in range(1,n):
            for j in range(1,n):
                if i<j:
                    newp=minp.copy()
                    newp[i],newp[j]=newp[j],newp[i]
                    if (l:=pathlength(newp,distances))<newlen:
                        newlen=l
                        newminp=newp.copy()
        for i in range(1,n-permutationnum):
            newp=minp.copy()
            for p in permutations(newp[i:i+permutationnum]):
                newp=newp[:i]+list(p)+newp[i+permutationnum:]
                if (l:=pathlength(newp,distances))<newlen:
                    newlen=l
                    newminp=newp.copy()
        for i in range(1,n):
            newp=minp.copy()
            pointvalue=newp[i]
            newp.remove(pointvalue)
            for j in range(1,n-1):
                newp.insert(j,pointvalue)
                if (l:=pathlength(newp,distances))<newlen:
                    newlen=l
                    newminp=newp.copy()
                newp.remove(pointvalue)
        if newlen<mind:
            minp=newminp.copy()
            mind=newlen
            #print(newminp,newlen)
        elif newlen==mind:
            print("end")
            break
        draw(points,paths,antnum,minp)
        canvas.create_text(1300,50,text=str(mind))
        canvas.update()
    print("minimum length",mind)
    sleep(1)
    
    mind=n*1000
    minp=[]
    #ACO
    for ant in range(antnum):
        d=0
        p=[0]
        availablepoints=[i for i in range(1,n)]
        currentpoint=0
        #print(currentpoint,end="")
        while availablepoints:
            i=getrandomindex(availablepoints,paths[currentpoint])
            #print("returnvalue",i)
            nextpoint=i
            availablepoints.remove(i)
            paths[currentpoint][nextpoint]+=(100*n/distances[currentpoint][nextpoint])#add information
            d+=distances[currentpoint][nextpoint]
            p.append(nextpoint)
            currentpoint=nextpoint
            #print(" ->",currentpoint,end="")
        else:
            paths[currentpoint][0]+=100*n/distances[currentpoint][0]
            d+=distances[currentpoint][0]
            p.append(0)
            #print("-> 0")
        for i in range(n):
            for j in range(n):
                if i>j:
                    paths[i][j]=paths[j][i]=(paths[i][j]+paths[j][i])*0.999/2
        # newpaths=[[0 for i in range(n)] for i in range(n)]
        # for i in range(n):
        #     s=sum(paths[i])
        #     for j in range(n):
        #         newpaths[i][j]=paths[i][j]*100/s#reduce
        # paths=newpaths
        # print(maxinformation)
        if d<mind:
            mind=d
            minp=p
        if ant%10==0:
            draw(points,paths,ant,minp)
            canvas.create_text(1300,50,text=str(mind))
            canvas.update()
            #print(ant,mind,max([max(i) for i in paths]))
            #sleep(0.01)
    print("ACO minimum result",mind)
    
    sleep(1)
    #ACO then local optimize
    mind=pathlength(minp,distances)
    while 1:
        newlen=mind
        newminp=[]
        for i in range(1,n):
            for j in range(1,n):
                if i<j:
                    newp=minp.copy()
                    newp[i:j+1]=newp[i:j+1][::-1]
                    if (l:=pathlength(newp,distances))<newlen:
                        newlen=l
                        newminp=newp.copy()
        for i in range(1,n):
            for j in range(1,n):
                if i<j:
                    newp=minp.copy()
                    newp[i],newp[j]=newp[j],newp[i]
                    if (l:=pathlength(newp,distances))<newlen:
                        newlen=l
                        newminp=newp.copy()
        for i in range(1,n-permutationnum):
            newp=minp.copy()
            for p in permutations(newp[i:i+permutationnum]):
                newp=newp[:i]+list(p)+newp[i+permutationnum:]
                if (l:=pathlength(newp,distances))<newlen:
                    newlen=l
                    newminp=newp.copy()
        for i in range(1,n):
            newp=minp.copy()
            pointvalue=newp[i]
            newp.remove(pointvalue)
            for j in range(1,n-1):
                newp.insert(j,pointvalue)
                if (l:=pathlength(newp,distances))<newlen:
                    newlen=l
                    newminp=newp.copy()
                newp.remove(pointvalue)
        if newlen<mind:
            minp=newminp.copy()
            mind=newlen
            #print(newminp,newlen)
        elif newlen==mind:
            print("end")
            break
        draw(points,paths,antnum,minp)
        canvas.create_text(1300,50,text=str(mind))
        canvas.update()
    print("mix minimum result",mind)
        
def click(coordinate):
    start()
canvas.bind("<Button-1>",click)
canvas.pack()
window.mainloop()

