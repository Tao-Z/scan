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
    lenth2 = len_v(vec2)
    d = (vec1[0] * vec2[1] - vec1[1] * vec2[0]) / lenth2
    return d

def len_v(vector):
    vector = np.array(vector)
    return np.sqrt(vector.dot(vector))

def unify(vector):
    return np.array(vector) / len_v(vector)

def angle(P1, P2, P3):
    vec1 = np.array(P1) - np.array(P2)
    vec2 = np.array(P3) - np.array(P2)
    if len_v(vec1) == 0 or len_v(vec2) == 0:
        return 0
    m = vec1.dot(vec2) / len_v(vec1) / len_v(vec2)
    m = round(m, 5)
    return np.arccos(m)

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
    x, y, z = sympy.symbols('x y z')
    func_1 = kp_1[3] * (kp_1[0] - x) + kp_1[4] * (kp_1[1] - y) + kp_1[5] * (kp_1[2] - z)
    line2 = func_1.subs(z, kp_2[2])
    r_step = Tf.reverse(plate2.step)
    plane_temp = Tf.bystep_plane(line2, r_step)
    plane_temp = Tf.bystep_plane(plane_temp, plate1.step)
    line1 = plane_temp.subs(z, 0)
    plate1.line.append(line1)
    plate2.line.append(line2)
    segment = getends(line2, plate2.boundary)
    for point in segment:
        point.append(kp_2[2])
    Tf.bystep(segment, r_step)
    return segment

def getends(line, boundary):
    ver = boundary['vertices']
    ends = []
    for seg in boundary['original_segments']:
        line_cur = getline_2D(ver[seg[0]], ver[seg[1]])
        c = intersect_of_line(line, line_cur)
        if (c[0]-ver[seg[0]][0])*(c[0]-ver[seg[1]][0])<=0 and (c[1]-ver[seg[0]][1])*(c[1]-ver[seg[1]][1])<=0 and c not in ends:
            ends.append(c)
    return ends

def getline_2D(point1, point2):
    x, y = sympy.symbols('x y')
    line = (x - point2[0])*(point1[1] - point2[1]) - (y - point2[1])*(point1[0] - point2[0])
    return line

def intersect_of_line(line1, line2):
    x, y = sympy.symbols('x y')
    result = sympy.solve([line1, line2], [x, y])
    return [float(result[x]), float(result[y])]

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
        if point != link.tail.data:
            link.append(point)

    points.sort()
    cur = link.head
    add(link, points, error, cur)
    
    cur = link.head
    while True:
        if (angle(cur.pre.data, cur.data, cur.next.data) > 3/4 * math.pi and P2V(cur.data, cur.pre.data, cur.next.data) < error):
            cur = cur.next
            link.delete(cur.pre)
        else:
            cur = cur.next
            if cur == link.head:
                break
    
    vertices = []
    cur = link.head
    for i in range(link.length):
        vertices.append(cur.data)
        cur = cur.next   
        
    segments = [[i, i+1] for i in range(link.length-1)]
    segments.append([link.length - 1, 0])
    original_vertices = copy.deepcopy(vertices)
    original_segments = copy.deepcopy(segments)
    boundary = dict(vertices = vertices, segments = segments, original_vertices = original_vertices, original_segments = original_segments)
    return boundary, step

def sub_segment(segment, n):
    dx = (segment[1][0] - segment[0][0]) / n
    dy = (segment[1][1] - segment[0][1]) / n
    dz = (segment[1][2] - segment[0][2]) / n
    for i in range(1, n):
        point = [segment[0][0] + i*dx, segment[0][1] + i*dy, segment[0][2] + i*dz]
        segment.insert(i, point)

def add_segment(boundary, new_seg):
    vertices = boundary['vertices']
    segments = boundary['segments']
    n = len(vertices)
    vertices.extend(new_seg)
    for i in range(len(new_seg)):
        j = 0
        while j < len(segments):
            p2v = P2V(new_seg[i], vertices[segments[j][0]], vertices[segments[j][1]])
            theta_1 = angle(new_seg[i], vertices[segments[j][0]], vertices[segments[j][1]])
            theta_2 = angle(new_seg[i], vertices[segments[j][1]], vertices[segments[j][0]])
            if p2v > -0.001 and theta_1 < 11/12 * math.pi and theta_2 < 11/12 * math.pi:
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

    for i in range(len(new_seg) - 1):
        if [n+i, n+i+1] not in segments and [n+i+1, n+i] not in segments:
            segments.append([n+i, n+i+1])
    
    for seg in boundary['original_segments']:
        if seg not in segments:
            if all(angle(p, vertices[seg[0]], vertices[seg[1]]) > 1/180 * math.pi for p in new_seg):
                segments.append(seg)


if __name__ == '__main__':
    import ReadData as RD
    import matplotlib.pyplot as plt
    import Locate as Lc
    import time

    vertices = RD.obj_vertices('data/input/sh_0411.obj')
    normals = RD.obj_normals('data/input/sh_0411.obj')
    Points = [vertices[i] + normals[i] for i in range(len(vertices))]
    P = Lc.locate(Points)
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
