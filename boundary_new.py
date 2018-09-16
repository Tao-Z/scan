import math
import bisect

def exist(points, x1, x2, y1, y2):
    p = bisect.bisect(points, [x1, 0])
    q = bisect.bisect(points, [x2, 0])
    for point in points[p:q]:
        if point[1] > y1 and point[1] < y2:
            return 1
    return 0
    
def boundary(points, precision):
    points.sort()
    corner=[points[0][0], points[0][0], points[0][1], points[0][1]]
    for point in points[1:]:
        if point[0] < corner[0]:
            corner[0] = point[0]
        elif point[0] > corner[1]:
            corner[1] = point[0]
        if point[1] < corner[2]:
            corner[2] = point[1]
        elif point[1] > corner[3]:
            corner[3] = point[1]
    
    M = math.ceil((corner[1] - corner[0]) / precision)
    N = math.ceil((corner[3] - corner[2]) / precision)
    Matrix = [[0 for j in range(N)] for i in range(M)]
    for i in range(M):
        for j in range(N):
            Matrix[i][j] = exist(points, corner[0]+i*precision, corner[0]+(i+1)*precision, corner[2]+j*precision, corner[2]+(j+1)*precision)
    return Matrix, corner[0], corner[2]

if __name__ == '__main__':
    import time
    import ReadData as RD
    import matplotlib.pyplot as plt
    import random
    points = []
    N = 100000
    while len(points) <= N:
        point = [random.uniform(-10, 10), random.uniform(-10,10)]
        r = math.sqrt(point[0]**2 + point[1]**2)
        if r >= 5 and r <= 10:
            points.append(point)
    begin = time.time()
    precision = 0.02
    b, x0, y0 = boundary(points, precision)
    end = time.time()
    print(end - begin, 's')
    fig, ax = plt.subplots()
    x = []
    y = []
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j] == 1:
                x.append(x0 + i * precision)
                y.append(y0 + j * precision)
    ax.plot(x, y, '.')
    plt.show()