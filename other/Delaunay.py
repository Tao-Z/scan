import math
import SortPoint

def center(t):
    x=((t[0][0]**2-t[1][0]**2+t[0][1]**2-t[1][1]**2)*(t[0][1]-t[2][1])-(t[0][0]**2-t[2][0]**2+
    t[0][1]**2-t[2][1]**2)*(t[0][1]-t[1][1]))/2/((t[0][1]-t[2][1])*(t[0][0]-t[1][0])-(t[0][1]-t[1][1])
    *(t[0][0]-t[2][0]))
    y=((t[0][0]**2-t[1][0]**2+t[0][1]**2-t[1][1]**2)*(t[0][0]-t[2][0])-(t[0][0]**2-t[2][0]**2+
    t[0][1]**2-t[2][1]**2)*(t[0][0]-t[1][0]))/2/((t[0][1]-t[1][1])*(t[0][0]-t[2][0])-(t[0][1]-t[2][1])
    *(t[0][0]-t[1][0]))
    return [x,y]

def radius(t):
    r=math.sqrt((t[0][0]-center(t)[0])**2+(t[0][1]-center(t)[1])**2)
    return r

def right_of_circle(Point, triangle):
    if Point[0]>center(triangle)[0]+radius(triangle):
        return 1
    else:
        return 0

def in_circle(Point, triangle):
    if math.sqrt((Point[0]-center(triangle)[0])**2+(Point[1]-center(triangle)[1])**2)<radius(triangle):
        return 1
    else:
        return 0
def delaunay(a):
    #get the max and min value of x and y
    Point=[]
    Point.extend(a)
    N=len(Point)
    for i in range(N):
        for j in range(2):
            Point[i][j]=Point[i][j]
            if i==0:
                max_x=Point[i][0]
                min_x=Point[i][0]
                max_y=Point[i][1]
                min_y=Point[i][1]
            else:
                if Point[i][0]>max_x:
                    max_x=Point[i][0]
                elif Point[i][0]<min_x:
                    min_x=Point[i][0]
                if Point[i][1]>max_y:
                    max_y=Point[i][1]
                elif Point[i][1]<min_y:
                    min_y=Point[i][1]

    #get the corner of rectangle area and original temp triangles
    Delta_x=(max_x-min_x)/2
    Delta_y=(max_y-min_y)/2
    corner=[[min_x-Delta_x, min_y-Delta_y], [max_x+Delta_x, min_y-Delta_y], [min_x-Delta_x, max_y+Delta_y], [max_x+Delta_x, max_y+Delta_y]]
    temp_triangles=[[corner[0], corner[1], corner[2]], [corner[1], corner[3], corner[2]]]

    #sort by x
    SortPoint.sort(Point,'x')

    triangles=[]  #definite Delaunay triangles

    #insert the points
    for i in range(N):
        #adjust the temp triangles
        edge_buffer=[]
        j=0
        while j<len(temp_triangles):
            m=0
            if right_of_circle(Point[i], temp_triangles[j]):
                m=1
                triangles.append(temp_triangles.pop(j))
            elif in_circle(Point[i], temp_triangles[j]):
                m=1
                edge_buffer.append([temp_triangles[j][0],temp_triangles[j][1]])
                edge_buffer.append([temp_triangles[j][1],temp_triangles[j][2]])
                edge_buffer.append([temp_triangles[j][2],temp_triangles[j][0]])
                temp_triangles.pop(j)
            if m==0:
                j=j+1

        #delete the same edges in edge_buffer, delete both!
        j=0
        while j<len(edge_buffer):
            m=0
            for k in range(j+1, len(edge_buffer)):
                if edge_buffer[j]==edge_buffer[k] or (edge_buffer[j][0]==edge_buffer[k][1] and edge_buffer[j][1]==edge_buffer[k][0]):
                    m=1
                    edge_buffer.pop(k)
                    edge_buffer.pop(j)
                    break
            if m==0:
                j=j+1

        #renew the temp triangles
        for j in range(len(edge_buffer)):
            temp_triangles.append([Point[i], edge_buffer[j][0], edge_buffer[j][1]])

    #add the temp triangles to triangles
    triangles.extend(temp_triangles)

    #delete the triangles related with corners
    i=0
    while i<len(triangles):
        m=0
        for j in range(len(triangles[i])):
            if triangles[i][j] in corner:
                m=1
                triangles.pop(i)
                break
        if m==0:
            i=i+1
    return triangles
