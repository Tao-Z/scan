import math
import numpy as np
import sympy
import copy

#move single point by vector
def move_s(point, vector):
    point[0] += vector[0]
    point[1] += vector[1]
    point[2] += vector[2]

#move Points by vector
def move(Points, vector):
    for point in Points:
        move_s(point, vector)

#rotate single point around axis-X by theta
def rotate_x_s(point, theta):
    y = point[1] * math.cos(theta) - point[2] * math.sin(theta)
    z = point[1] * math.sin(theta) + point[2] * math.cos(theta)
    point[1] = y
    point[2] = z
    if len(point) == 6:
        vy = point[4] * math.cos(theta) - point[5] * math.sin(theta)
        vz = point[4] * math.sin(theta) + point[5] * math.cos(theta)
        point[4] = vy
        point[5] = vz

#rotate Points around axis-X by theta
def rotate_x(Points, theta):
    for point in Points:
        rotate_x_s(point, theta)

#rotate single point around axis-Y by theta
def rotate_y_s(point, theta):
    z = point[2] * math.cos(theta) - point[0] * math.sin(theta)
    x = point[2] * math.sin(theta) + point[0] * math.cos(theta)
    point[2] = z
    point[0] = x
    if len(point) == 6:
        vz = point[5] * math.cos(theta) - point[3] * math.sin(theta)
        vx = point[5] * math.sin(theta) + point[3] * math.cos(theta)
        point[5] = vz
        point[3] = vx

#rotate Points around axis-Y by theta
def rotate_y(Points, theta):
    for point in Points:
        rotate_y_s(point, theta)

#rotate single point around axis-Z by theta
def rotate_z_s(point, theta):
    x = point[0] * math.cos(theta) - point[1] * math.sin(theta)
    y = point[0] * math.sin(theta) + point[1] * math.cos(theta)
    point[0] = x
    point[1] = y
    if len(point) == 6:
        vx = point[3] * math.cos(theta) - point[4] * math.sin(theta)
        vy = point[3] * math.sin(theta) + point[4] * math.cos(theta)
        point[3] = vx
        point[4] = vy

#rotate Points around axis-Z by theta
def rotate_z(Points, theta):
    for point in Points:
        rotate_z_s(point, theta)

#move and rotate Points with vector by picked points
def newcoord(Points, pick):
    P = [[coord for coord in point] for point in pick]
    #Step 1: A[xa,ya,za] -> A[0,0,0]
    vector = np.array([0,0,0]) - np.array(P[0])
    move(Points, vector)
    move(P, vector)
    #Step 2: B[xb,yb,zb] -> B[xb',0,0] xb'>0
    #Step 2.1: rotate around axis-Z, yb -> 0
    theta = - math.atan2(P[1][1],P[1][0])
    rotate_z(Points, theta)
    rotate_z(P, theta)
    #Step 2.2: rotate around axis-Y, zb -> 0
    theta = math.pi / 2 - math.atan2(P[1][0], P[1][2])
    rotate_y(Points, theta)
    rotate_y(P, theta)
    #Step 3: C[xc,yc,zc] -> C[xc',0,zc'] zc'>0
    #rotate around axis-X, yc -> 0
    theta = math.pi / 2 - math.atan2(P[2][2], P[2][1])
    rotate_x(Points, theta)
    rotate_x(P, theta)

#move and rotate Points with vector by picked new axis-Z
def new_z(Points, keypoint):
    p = keypoint[0:3]
    new_z = keypoint[3:6]
    step = [] #record the steps

    #move Points to make p to [0,0,0]
    vec = np.array([0, 0, 0]) - p
    move(Points, vec)
    move([p], vec)
    step.append(['m',vec])

    #rotate around axis-X and axis-Y, new_z(x, y, z) -> (0, 0, z')
    #step 1: rotate around axis-X, new_z(y) -> 0
    theta = math.pi / 2 - math.atan2(new_z[2], new_z[1])
    rotate_x(Points, theta)
    rotate_x([new_z], theta)
    step.append(['rx', theta])

    #step 2: rotate around axis-Y, new_z(x) -> 0
    theta = - math.atan2(new_z[0], new_z[2])
    rotate_y(Points, theta)
    rotate_y([new_z], theta)
    step.append(['ry', theta])

    return step

def reverse(step):
    r_step = []
    for i in step[::-1]:
        r_step.append([i[0], - i[1]])
    return r_step

def step_s(point, steps):
    for step in steps:
        if step[0] == 'm':
            move_s(point, step[1])
        elif step[0] == 'rx':
            rotate_x_s(point, step[1])
        elif step[0] == 'ry':
            rotate_y_s(point, step[1])
        elif step[0] == 'rz':
            rotate_z_s(point, step[1])

def bystep(Points, steps):
    for step in steps:
        if step[0] == 'm':
            move(Points, step[1])
        elif step[0] == 'rx':
            rotate_x(Points, step[1])
        elif step[0] == 'ry':
            rotate_y(Points, step[1])
        elif step[0] == 'rz':
            rotate_z(Points, step[1])

def bystep_line(line, steps):
    x0, y0, z0 = sympy.symbols('x0 y0 z0')
    x, y, z = sympy.symbols('x y z')
    line_temp = copy.deepcopy(line)
    for step in steps:       
        if step[0] == 'm':
            point = [x, y, z]
            move_s(point, -step[1])
            line_temp = line_temp.subs([(x, point[0]), (y, point[1]), (z, point[2])])
        if step[0] == 'rx':
            point = [x0, y0, z0]
            rotate_x_s(point, -step[1])
            print(point)
            line_temp = line_temp.subs([(x, point[0]), (y, point[1]), (z, point[2])])
            line_temp = line_temp.subs([(x0, x), (y0, y), (z0, z)])
        if step[0] == 'ry':
            point = [x0, y0, z0]
            rotate_y_s(point, -step[1])
            line_temp = line_temp.subs([(x, point[0]), (y, point[1]), (z, point[2])])
            line_temp = line_temp.subs([(x0, x), (y0, y), (z0, z)])
        if step[0] == 'rz':
            point = [x0, y0, z0]
            rotate_z_s(point, -step[1])
            line_temp = line_temp.subs([(x, point[0]), (y, point[1]), (z, point[2])])
            line_temp = line_temp.subs([(x0, x), (y0, y), (z0, z)])
    return line_temp
                   
    
def tri_step(t, step):
    Points = [[t['vertices'][i][0], t['vertices'][i][1], t['z'][i]] for i in range(len(t['vertices']))]
    bystep(Points, step)
    for i in range(len(Points)):
        t['vertices'][i][0] = Points[i][0]
        t['vertices'][i][1] = Points[i][1]
        t['z'][i] = Points[i][2]

if __name__ == '__main__':
    import ReadData as RD
    import time
    start = time.time()
    Points = RD.vertices('data/input/sh_0411.obj')
    #get coordinates of three picked points
    pick = [[145, -196, -104], [145, -199, 82], [-158, -196, -104]]
    newcoord(Points, pick)
    for i in range(10):
        print(Points[i])
    end = time.time()
    print('Time=', end - start, 's')
