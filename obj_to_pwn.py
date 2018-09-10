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
        N = 0
        for line in f0:
            if line.startswith('# Vertices:'):
                tmp = line.split()
                N = int(tmp[2])
                break
        vertices = [[0 for i in range(6)] for j in range(N)]
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

def faces(filename):
    with open(filename, 'r') as f0:
        N = 0
        for line in f0:
            if line.startswith('# Faces:'):
                tmp = line.split()
                N = int(tmp[2])
                break
        faces = [[0 for i in range(3)] for j in range(N)]
        i = 0
        for line in f0:
            if line.startswith('f '):
                tmp = line.split()
                for j in range(1, 4):
                    tmp[j] = tmp[j].split('//')[0]
                faces[i] = [int(tmp[1]), int(tmp[2]), int(tmp[3])]
                i += 1
    return faces

def topwn(points, filename):
    with open(filename, 'w') as f0:
        for point in points:
            for num in point:
                print(num, end = '', file = f0)
                if num != point[-1]:
                    print(' ', end = '', file = f0)
            print('', file = f0)

def tooff(points, faces, filename):
    with open(filename, 'w') as f0:
        print('OFF', file = f0)
        print(len(points), len(faces), 0, file = f0)
        for point in points:
            for num in point[0:3]:
                print(num, end = '', file = f0)
                if num != point[2]:
                    print(' ', end = '', file = f0)
            print('', file = f0)
        for face in faces:
            print(3, end = ' ', file = f0)
            for num in face:
                print(num-1, end = '', file = f0)
                if num != face[-1]:
                    print(' ', end = '', file = f0)
            print('', file = f0)
                
points = vertices('data/input/half height_100k.obj')
faces = faces('data/input/half height_100k.obj')
#topwn(points, 'data/half height/half height_4M.pwn')
tooff(points, faces, 'data/output/half height_100k.off')