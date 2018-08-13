import math
import numpy as np
import bisect

def distance(Point1, Point2):
    return math.sqrt((Point1[0] - Point2[0])**2 + (Point1[1] - Point2[1])**2 + (Point1[2] - Point2[2])**2)

def len_v(vector):
    return math.sqrt(sum((n**2) for n in vector))

def unify(vector):
    return np.array(vector) / len_v(vector)

def cos_v(vector1, vector2):
    return np.dot(vector1, vector2) / len_v(vector1) / len_v(vector2)

def angle_v(vector1, vector2):
    return math.acos(np.dot(vector1, vector2) / len_v(vector1) / len_v(vector2))

def thick(t, face1, face2, r_min, num):
    vertices = t['vertices']
    n = len(vertices)
    P1 = np.array([[0.,0,0] for i in range(n)])
    P2 = np.array([[0.,0,0] for i in range(n)])
    vector1 = np.array([[0.,0,0] for i in range(n)])
    vector2 = np.array([[0.,0,0] for i in range(n)])
    t['R2'] = [0 for i in range(n)]
    t['a2'] = [0 for i in range(n)]
    t['b2'] = [0 for i in range(n)]
    for i in range(n):
        r = r_min
        while t['a2'][i] < num or t['b2'][i] < num:
            P1[i] = [0.,0,0]
            vector1[i] = [0.,0,0]
            t['a2'][i] = 0
            p = bisect.bisect(face1, [vertices[i][0] - r, 0])
            q = bisect.bisect(face1, [vertices[i][0] + r, 0])
            for point in face1[p:q]:
                if point[1] < vertices[i][1] - r or point[1] > vertices[i][1] + r:
                    continue
                if distance([vertices[i][0], vertices[i][1], t['z'][i]], point) < r:
                    P1[i] = P1[i] + np.array(point[:3])
                    vector1[i] = vector1[i] + unify(point[3:])
                    t['a2'][i] = t['a2'][i] + 1

            P2[i] = [0.,0,0]
            vector2[i] = [0.,0,0]
            t['b2'][i] = 0
            p = bisect.bisect(face2, [vertices[i][0] - r, 0])
            q = bisect.bisect(face2, [vertices[i][0] + r, 0])
            for point in face2[p:q]:
                if point[1] < vertices[i][1] - r or point[1] > vertices[i][1] + r:
                    continue
                if distance([vertices[i][0], vertices[i][1], t['z'][i]], point) < r:
                    P2[i] = P2[i] + np.array(point[:3])
                    vector2[i] = vector2[i] + unify(point[3:])
                    t['b2'][i] = t['b2'][i] + 1
            r += 0.5
        t['R2'][i] = r - 0.5
        P1[i] = P1[i] / t['a2'][i]
        vector1[i] = unify(vector1[i] / t['a2'][i])
        P2[i] = P2[i] / t['b2'][i]
        vector2[i] = unify(vector2[i] / t['b2'][i])

    vector = vector2 - vector1
    t['thick2'] = []
    for i in range(n):
        t['thick2'].append(distance(P1[i], P2[i]) / cos_v(vector[i], vector2[i]) / cos_v(vector[i], vector2[i]))
    t['thick2'] = np.array(t['thick2'])
