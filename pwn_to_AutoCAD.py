def read(filename):
    f = open(filename, 'r')
    data = [float(x) for x in f.read().split()]
    points = []
    for i in range(0, len(data)//6, 6):
        points.append(data[i:i+6])
    return points

def toAutoCAD(points, filename):
    with open(filename, 'w') as f0:
        for point in points:
            print('Point %f,%f,%f' % (point[0], point[1], point[2]), file = f0)

def toOBJ(points, filename):
    with open(filename, 'w') as f0:
        for point in points:
            print('v %f %f %f' % (point[0], point[1], point[2]), file = f0)
            print('vn %f %f %f' % (point[3], point[4], point[5]), file = f0)
    
if __name__ == '__main__':
    points = read('data/cube.pwn')
    toAutoCAD(points, 'data/AutoCAD.txt')
    toOBJ(points, 'data/model.obj')

