import bisect
import math
import numpy as np
import sympy

def distance(Point1, Point2):
    return math.sqrt((Point1[0] - Point2[0])**2 + (Point1[1] - Point2[1])**2)

def len_v(vector):
    return math.sqrt(sum((n**2) for n in vector))

#unify the length of vector to 1
def unify(vector):
    return np.array(vector) / len_v(vector)

def thick(m_point, face1, face2, r_min, num):
    r = r_min
    a = 0
    b = 0
    while a < num or b < num:
        z1 = 0
        vector1 = np.array([0.,0,0])
        a = 0
        p = bisect.bisect(face1, [m_point[0] - r, 0])
        q = bisect.bisect(face1, [m_point[0] + r, 0])
        for point in face1[p:q]:
            if point[1] < m_point[1] - r or point[1] > m_point[1] + r:
                continue
            if distance(m_point, point) < r:
                z1 += point[2]
                vector1 = vector1 + unify(point[3:])
                a += 1

        z2 = 0
        vector2 = np.array([0.,0,0])
        b = 0
        p = bisect.bisect(face2, [m_point[0] - r, 0])
        q = bisect.bisect(face2, [m_point[0] + r, 0])
        for point in face2[p:q]:
            if point[1] < m_point[1] - r or point[1] > m_point[1] + r:
                continue
            if distance(m_point, point) < r:
                z2 += point[2]
                vector2 = vector2 + unify(point[3:])
                b += 1
        r += 0.5
    z1 = z1 / a
    vector1 = unify(vector1 / a)
    z2 = z2 / b
    vector2 = unify(vector2 / b)

    thick0 = abs(z1 - z2)
    vector = unify(vector2 - vector1)
    thick = thick0 * abs(vector[2])
    return thick

def getz(t, face1, face2, r_min, num, p_name, lines):
    vertices = t['vertices']
    n = len(vertices)
    z1 = [0.0 for i in range(n)]
    z2 = [0.0 for i in range(n)]
    t['z'] = [0 for i in range(n)]
    vector1 = np.array([[0., 0, 0] for i in range(n)])
    vector2 = np.array([[0., 0, 0] for i in range(n)])
    t['R1'] = [0 for i in range(n)]
    t['a1'] = [0 for i in range(n)]
    t['b1'] = [0 for i in range(n)]

    for i in range(n):
        r = r_min - 0.5
        while t['a1'][i] < num or t['b1'][i] < num:
            r += 0.5
            z1[i] = 0
            vector1[i] = [0.0, 0, 0]
            t['a1'][i] = 0
            p = bisect.bisect(face1, [vertices[i][0] - r, 0])
            q = bisect.bisect(face1, [vertices[i][0] + r, 0])
            for point in face1[p:q]:
                if point[1] < vertices[i][1] - r or point[1] > vertices[i][1] + r:
                    continue
                if distance(vertices[i], point) < r:
                    z1[i] += point[2]
                    vector1[i] = vector1[i] + unify(point[3:])
                    t['a1'][i] += 1

            z2[i] = 0
            vector2[i] = [0.0, 0, 0]
            t['b1'][i] = 0
            p = bisect.bisect(face2, [vertices[i][0] - r, 0])
            q = bisect.bisect(face2, [vertices[i][0] + r, 0])
            for point in face2[p:q]:
                if point[1] < vertices[i][1] - r or point[1] > vertices[i][1] + r:
                    continue
                if distance(vertices[i], point) < r:
                    z2[i] += point[2]
                    vector2[i] = vector2[i] + unify(point[3:])
                    t['b1'][i] += 1
        t['R1'][i] = r
        z1[i] = z1[i] / t['a1'][i]
        vector1[i] = unify(vector1[i] / t['a1'][i])
        z2[i] = z2[i] / t['b1'][i]
        vector2[i] = unify(vector2[i] / t['b1'][i])

        #get z
        x, y = sympy.symbols('x y')
        if any(abs(line.subs([(x, vertices[i][0]), (y, vertices[i][1])])) < 1 for line in lines):
            t['z'][i] = 0
        else:
            if p_name == 'W':
                t['z'][i] = (z1[i] + z2[i]) / 2
                if abs(z1 [i]- z2[i]) > 20:
                    t['z'][i] = 0
            else:
                t['z'][i] = z1[i]

    #get thick
    thick0 = abs(np.array(z1) - np.array(z2))
    vector = vector2 - vector1

    for i in range(n):
        vector[i] = unify(vector[i])

    t['thick1'] = [thick0[i] * abs(vector[i][2]) for i in range(n)]
    for i in range(n):
        if t['thick1'][i] > 100:
            t['thick1'][i] = 100


def midthick(t, face1, face2, r_min, num):
    #get the thick of the middle point of triangles
    t['mid_point'] = []
    t['mid_thick'] = []
    for triangle in t['triangles']:
        mid_point = sum(t['vertices'][i] for i in triangle)
        mid_point = mid_point / 3
        t['mid_point'].append(mid_point)
        t['mid_thick'].append(thick(mid_point, face1, face2, r_min, num))
