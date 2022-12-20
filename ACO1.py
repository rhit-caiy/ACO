from random import randint
from tkinter import Tk,Canvas
from time import sleep

window=Tk()
canvas=Canvas(window,bg="#FFFFFF",width=1440,height=810)
window.title("ACO")

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
    
def draw(points,paths,ant):
    canvas.delete("all")
    # maxinformation=max([max(i) for i in paths])
    canvas.create_line(0,10,ant,10)
    canvas.create_line(antnum,0,antnum,20)
    for i in range(n):
        # maxv=max(paths[i])
        for j in range(n):
            if i>j:
                maxinformation=max(max(paths[i]),max(paths[j]))
                canvas.create_line(points[i][0],points[i][1],points[j][0],points[j][1],fill=densitycolor(paths[i][j],maxinformation))
            # if paths[i][j]==maxv:
            #     canvas.create_line(points[i][0],points[i][1],points[j][0],points[j][1],fill="#000000")
    for point in points:
        if point==points[0]:
            canvas.create_oval(point[0]-4,point[1]-4,point[0]+4,point[1]+4,fill="#FF0000")
        else:
            canvas.create_oval(point[0]-4,point[1]-4,point[0]+4,point[1]+4,fill="#000000")
    canvas.update()

def start():
    global n
    points=[]
    for i in range(n):
        #avoid too close
        
        x,y=(randint(100,1400),randint(50,700))
        
        points.append((x,y))
    
    n=len(points)
    distances=[[0 for i in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            distances[i][j]=((points[i][0]-points[j][0])**2+(points[i][1]-points[j][1])**2)**0.5
    #print(distances)
    
    paths=[[0 for i in range(n)] for i in range(n)]
    
    for ant in range(antnum):
        availablepoints=[i for i in range(1,n)]
        currentpoint=0
        #print(currentpoint,end="")
        while availablepoints:
            i=getrandomindex(availablepoints,paths[currentpoint])
            #print("returnvalue",i)
            nextpoint=i
            availablepoints.remove(i)
            paths[currentpoint][nextpoint]+=(100/distances[currentpoint][nextpoint])#add information
            currentpoint=nextpoint
            #print(" ->",currentpoint,end="")
        else:
            paths[currentpoint][0]+=100/distances[currentpoint][0]
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
        if ant%10==0:
            draw(points,paths,ant)
            print(ant,max([max(i) for i in paths]))
            sleep(0.01)
def click(coordinate):
    start()
canvas.bind("<Button-1>",click)
canvas.pack()
window.mainloop()

