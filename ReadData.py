def points(filename,N = 0): #if N!=0, read at most N lines data from filename
    Points = []
    with open(filename, 'r') as f0:
        i = 0
        for line in f0:
            tmp1 = line.split()
            tmp2 = tmp1[1].split(',')
            Points.append([float(tmp2[0]), float(tmp2[1]), float(tmp2[2])])
            i = i + 1
            if N != 0 and i > N-1:
                break
    return Points

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
                j += 1
    return vertices

if __name__ == '__main__':
    Points = points('data/output/3_leftside_of_web.txt')
    for point in Points:
        print(point)
    print(len(Points))
