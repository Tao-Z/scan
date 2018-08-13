import numpy as np
import math
import bisect
import Linkedlist as Ll
import Transform as Tf
import sympy
import copy

def P2P(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#get the distance of point to vector, begin is the begin point of vector, end is the end point of vector
#value larger than 0 means the point is at the clockwise of vector, value smaller than 0 means the point is at the anticlockwise of vector
def P2V(point, begin, end):
    vec1 = np.array([point[0], point[1]]) - np.array(begin)
    vec2 = np.array(end) - np.array(begin)
    lenth2 = math.sqrt(np.sum(np.square(vec2)))
    d = (vec1[0] * vec2[1] - vec1[1] * vec2[0]) / lenth2
    return d

def len_v(vector):
    return math.sqrt(sum((n**2) for n in vector))

def unify(vector):
    return np.array(vector) / len_v(vector)

def plane_face(points):
    k = 1
    if len(points) > 1000:
        k = len(points) // 1000
    mid_point = [0, 0, 0]
    vec = [0, 0, 0]
    n = 0
    for point in points[::k]:
        mid_point += np.array(point[0:3])
        vec += unify(point[3:6])
        n += 1
    mid_point = mid_point / n
    vec = unify(vec)
    return mid_point, vec

def plane(points_couple, p_name):
    if p_name == 'W':
        mid_point0, vec0 = plane_face(points_couple[0])
        mid_point1, vec1 = plane_face(points_couple[1])
        mid_point = (mid_point0 + mid_point1) / 2
        vec = unify((vec0 - vec1) / 2)
        keypoint = np.append(mid_point, vec)
    else:
        mid_point0, vec0 = plane_face(points_couple[0])
        keypoint = np.append(mid_point0, vec0)
    return keypoint

def intersect_of_plate(plate1, plate2):
    kp_1 = copy.deepcopy(plate1.keypoint)
    kp_2 = copy.deepcopy(plate2.keypoint)
    Tf.step_s(kp_1, plate2.step)
    Tf.step_s(kp_2, plate2.step)
    x,y,z = sympy.symbols('x y z')
    func_1 = kp_1[3] * (kp_1[0] - x) + kp_1[4] * (kp_1[1] - y) + kp_1[5] * (kp_1[2] - z)
    line = func_1.subs(z, kp_2[2])
    segment = end(line, plate2.boundary)
    for point in segment:
        point.append(kp_2[2])
    r_step = Tf.reverse(plate2.step)
    Tf.bystep(segment, r_step)
    return segment

def end(line, boundary):
    ver = boundary['vertices']
    end = []
    for seg in boundary['segments']:
        line_cur = getline_2D(ver[seg[0]], ver[seg[1]])
        c = intersect_of_line(line, line_cur)
        if (c[0]-ver[seg[0]][0])*(c[0]-ver[seg[1]][0])<=0 and (c[1]-ver[seg[0]][1])*(c[1]-ver[seg[1]][1])<=0 and c not in end:
            end.append(c)
    return end

def getline_2D(point1, point2):
    x, y = sympy.symbols('x y')
    line = (x - point2[0])*(point1[1] - point2[1]) - (y - point2[1])*(point1[0] - point2[0])
    return line

def intersect_of_line(line1, line2):
    x, y = sympy.symbols('x y')
    result = sympy.solve([line1, line2], [x, y])
    return [result[x], result[y]]

#add points into link to complete boundary
def add(link, Points, error, cur):
    next = cur.next
    x = [min(cur.data[0], next.data[0]), max(cur.data[0], next.data[0])]
    y = [min(cur.data[1], next.data[1]), max(cur.data[1], next.data[1])]
    p = bisect.bisect(Points, [x[0], 0])
    q = bisect.bisect(Points, [x[1], 0])
    temp = None
    dist = 0
    for point in Points[p:q]:
        if point[1] < y[0] or point[1] > y[1]:
            continue
        p2v = P2V(point, cur.data, next.data)
        if p2v > error and p2v > dist:
            temp = point
            dist = p2v

    if temp == None:
        if cur == link.tail:
            return
        cur = cur.next
        add(link, Points, error, cur)
    else:
        link.insert([temp[0], temp[1]], cur)
        add(link, Points, error, cur)
    return

def boundary(points_couple, keypoint, error): #get the boundary based on face1

    #rotate plate into X_Y plane
    points = copy.deepcopy(points_couple[0])
    kp = copy.deepcopy(keypoint)
    step = Tf.new_z(points, kp)

    #get eight corner on boundary with anticlockwise
    corner=[[points[0][0], points[0][1]] for i in range(4)]
    for point in points[1:]:
        if point[0] < corner[0][0]:
            corner[0][0] = point[0]
            corner[0][1] = point[1]

        if point[1] < corner[1][1]:
            corner[1][0] = point[0]
            corner[1][1] = point[1]

        if point[0] > corner[2][0]:
            corner[2][0] = point[0]
            corner[2][1] = point[1]

        if point[1] > corner[3][1]:
            corner[3][0] = point[0]
            corner[3][1] = point[1]

    link = Ll.Linkedlist()
    link.append(corner[0])
    for point in corner[1:]:
        if P2P(point, link.tail.data) > error:
            link.append(point)

    points.sort()
    cur = link.head
    add(link, points, error, cur)

    vertices = []
    cur = link.head
    for i in range(link.length):
        vertices.append(cur.data)
        cur = cur.next

    segments = [[i, i+1] for i in range(link.length-1)]
    segments.append([link.length - 1, 0])

    boundary = dict(vertices = vertices, segments = segments)
    return boundary, step

def sub_segment(segment, n):
    dx = (segment[1][0] - segment[0][0]) / n
    dy = (segment[1][1] - segment[0][1]) / n
    dz = (segment[1][2] - segment[0][2]) / n
    for i in range(1, n):
        point = [segment[0][0] + i*dx, segment[0][1] + i*dy, segment[0][2] + i*dz]
        segment.insert(i, point)

def between(P1, P2, P3):
    return (P1[0] - P2[0]) * (P1[0] - P3[0]) <= 0 and (P1[1] - P2[1]) * (P1[1] - P3[1]) <= 0

def add_segment(boundary, new_seg):
    vertices = [boundary['vertices'][i] for i in range(len(boundary['vertices']))]
    segments = [boundary['segments'][i] for i in range(len(boundary['segments']))]
    n = len(vertices)
    vertices.extend(new_seg)
    for i in range(len(new_seg)):
        j = 0
        while j < len(segments):
            p2v = P2V(new_seg[i], vertices[segments[j][0]], vertices[segments[j][1]])
            if p2v > -0.3:
                if [n+i, segments[j][0]] not in segments:
                    segments.insert(j, [segments[j][0], n+i])
                    j += 1
                else:
                    segments.remove([n+i, segments[j][0]])
                    j -= 1
                if [segments[j][1], n+i] not in segments:
                    segments.insert(j, [n+i, segments[j][1]])
                    j += 1
                else:
                    segments.remove([segments[j][1], n+i])
                    j -= 1
                segments.pop(j)
            else:
                j += 1
    if [n, n+len(new_seg)-1] in segments:
        segments.remove([n, n+len(new_seg)-1])
    if [n+len(new_seg)-1, n] in segments:
        segments.remove([n+len(new_seg)-1, n])
    for i in range(len(new_seg) - 1):
        if [n+i, n+i+1] not in segments and [n+i+1, n+i] not in segments:
            segments.append([n+i, n+i+1])

    i = 0
    while i < len(vertices):
        if any(i in segment for segment in segments):
            i += 1
        else:
            vertices.pop(i)
            for segment in segments:
                for j in range(2):
                    if segment[j] > i:
                        segment[j] = segment[j] - 1

    boundary['vertices'] = vertices
    boundary['segments'] = segments


if __name__ == '__main__':
    import ReadData as RD
    import matplotlib.pyplot as plt
    import Locate as Lc
    import time

    Point = RD.vertices('data/input/sh_0411.obj')
    P = Lc.locate(Point)
    face1 = [point for point in P['DTF1']]
    face2 = [point for point in P['UTF']]

    start = time.time()
    boundary = boundary(face1, face2, 5, 'flange')
    end = time.time()
    print('Time = ', end - start)

    fig1 = plt.figure()
    ax = fig1.add_subplot(111, aspect = 'equal')
    for point in face1[::10]:
        ax.scatter(point[0], point[1], color = 'black', marker = '.')
    v = boundary['vertices']
    s = boundary['segments']
    print(len(v))
    print(len(s))
    for i in range(len(s)):
        ax.scatter(v[i][0], v[i][1], color = 'red', marker = '.')
        ax.plot([v[s[i][0]][0], v[s[i][1]][0]], [v[s[i][0]][1], v[s[i][1]][1]], 'k-')

    plt.show()
