import numpy as np

def rect(corner, m, n):
    A = np.array(corner[0])
    B = np.array(corner[1])
    C = np.array(corner[2])
    D = np.array(corner[3])
    vertices = []
    segments = []
    for i in range(m + 1):
        for j in range(n + 1):
            P=((m * n - n * i - m * j + i * j) * A + i * (n - j) * B + j *(m - i) * C + i * j * D) / m / n
            vertices.append(P)
    for i in range(m + 1):
        for j in range(n):
            segments.append([i * (n + 1) + j, i * (n + 1) + j + 1])
    for j in range(n + 1):
        for i in range(m):
            segments.append([i * (n + 1) + j, (i + 1) * (n + 1) + j])
    rect = dict(vertices = vertices, segments = segments)
    return rect
if __name__ == '__main__':
    import ReadData as RD

    corner = [[-150, -174], [136, -174], [-150, -164], [136, -164]]
    rect = rect(corner, 25, 1)
    with open('data/output/mesh.txt','w') as f0:
        for vertex in rect['vertices']:
            print('point %.2f,%.2f' % (vertex[0], vertex[1]), file = f0)
        for segment in rect['segments']:
            a = segment[0]
            b = segment[1]
            print('line %.2f,%.2f %.2f,%.2f ' % (rect['vertices'][a][0], rect['vertices'][a][1], rect['vertices'][b][0], rect['vertices'][b][1]), file = f0)
