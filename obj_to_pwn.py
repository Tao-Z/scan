import math

def len_v(vector):
    return math.sqrt(sum((n**2) for n in vector))

#unify the length of vector to 1
def unify(vector):
    length = len_v(vector)
    for i in range(len(vector)):
        vector[i] /= length
    return vector

def vertices(filename):
    with open(filename, 'r') as f0:
        for line in f0:
            if line.startswith('# Vertices:'):
                tmp = line.split()
                N = int(tmp[2])
                break
        vertices = [[0 for i in range(6)] for i in range(N)]
        i = 0
        j = 0
        for line in f0:
            if line.startswith('v '):
                tmp = line.split()
                vertices[i][0:3] = [float(tmp[1]), float(tmp[2]), float(tmp[3])]
                i += 1
            elif line.startswith('vn '):
                tmp = line.split()
                vertices[j][3:6] = [float(tmp[1]), float(tmp[2]), float(tmp[3])]
                vertices[j][3:6] = unify(vertices[j][3:6])
                j += 1
    return vertices

def topwn(points, filename):
    with open(filename, 'w') as f0:
        for point in points:
            for num in point:
                print(num, end = '', file = f0)
                if num != point[-1]:
                    print(' ', end = '', file = f0)
            print('', file = f0)

points = vertices('data/sh f.obj')

topwn(points, 'data/sh f.pwn')