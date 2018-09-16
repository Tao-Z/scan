def AutoCAD_points(filename,N = 0): #if N!=0, read at most N lines data from filename
    points = []
    with open(filename, 'r') as f0:
        i = 0
        for line in f0:
            tmp1 = line.split()
            tmp2 = tmp1[1].split(',')
            points.append([float(tmp2[0]), float(tmp2[1]), float(tmp2[2])])
            i = i + 1
            if N != 0 and i > N-1:
                break
    return points

def obj_vertices(filename):
    with open(filename, 'r') as f0:
        vertices = []
        for line in f0:
            if line.startswith('v '):
                tmp = line.split()
                vertices.append([float(tmp[1]), float(tmp[2]), float(tmp[3])])
    return vertices

def obj_normals(filename):
    with open(filename, 'r') as f0:
        normals = []
        for line in f0:
            if line.startswith('vn '):
                tmp = line.split()
                normals.append([float(tmp[1]), float(tmp[2]), float(tmp[3])])
    return normals

def obj_faces(filename):
    with open(filename, 'r') as f0:
        faces = []
        for line in f0:
            if line.startswith('f '):
                tmp = line.split()
                for j in range(1, 4):
                    tmp[j] = tmp[j].split('//')[0]
                faces.append([int(tmp[1]), int(tmp[2]), int(tmp[3])])
    return faces

def pwn_points(filename):
    with open(filename, 'r') as f0:
        data = [float(x) for x in f0.read().split()]
        points = []
        for i in range(0, len(data)//6, 6):
            points.append(data[i:i+3])
    return points

def pwn_normals(filename):
    with open(filename, 'r') as f0:
        data = [float(x) for x in f0.read().split()]
        normals = []
        for i in range(0, len(data)//6, 6):
            normals.append(data[i+3:i+6])
    return normals

def off_points(filename):
    with open(filename, 'r') as f0:
        for i, line in enumerate(f0):
            if i == 1:
                num_points = line.split()[0]
                break
        points = []
        for i, line in enumerate(f0):
            if i >= 3 and i < 3 + num_points:
                points.append(line.split())
    return points

def xyz(filename):
    pass
    
if __name__ == '__main__':
    points = AutoCAD_points('data/output/3_leftside_of_web.txt')
    for point in points:
        print(point)
    print(len(points))
