def locate(Points):
    #get the coordinates of midy, thick_of_top_flange and thick_of_bottom_flange
    maxy = miny = Points[0][1]
    maxz = minz = Points[0][2]
    for point in Points[1:]:
        if point[1] > maxy:
            maxy = point[1]
        elif point[1] < miny:
            miny = point[1]
        if point[2] > maxz:
            maxz = point[2]
        elif point[2] < minz:
            minz = point[2]
    midy = (maxy + miny) / 2
    midz = (maxz + minz) / 2
    z1 = (minz * 3 + maxz) / 4
    z2 = (minz + maxz * 3) / 4

    #recognize the position of points
    TF = [[], []]
    W = [[], []]
    BF = [[], []]
    EG = [[], []]
    SF = [[], []]

    m = 0.3
    for point in Points:
        if point[3] > abs(point[4]) and point[3] > abs(point[5]):
            EG[0].append(point)
        elif -point[3] > abs(point[4]) and -point[3] > abs(point[5]):
            EG[1].append(point)
        elif point[2] < z1 and abs(point[5]) > m * abs(point[4]):
            SF[0].append(point)
        elif point[2] > z2 and abs(point[5]) > m * abs(point[4]):
            SF[1].append(point)
        elif point[1] > midy and point[4] > abs(point[5]):
            TF[0].append(point)
        elif point[1] < midy and -point[4] > abs(point[5]):
            BF[0].append(point)
        else:
            if point[2] < midz and -point[5] > m * abs(point[4]):
                W[0].append(point)
            elif point[2] > midz and point[5] > m * abs(point[4]):
                W[1].append(point)
            if point[1] > midy and -point[4] > m * abs(point[5]):
                TF[1].append(point)
            elif point[1] < midy and point[4] > m * abs(point[5]):
                BF[1].append(point)
    Points_located = {'TF':TF, 'BF':BF, 'W':W}
    return Points_located

if __name__ == '__main__':
    import ReadData as RD
    import WriteData as WD
    import time
    points = RD.obj_vertices('data/input/sh f.obj')
    normals = RD.obj_normals('data/input/sh f.obj')
    pwns = [points[i] + normals[i] for i in range(len(points))]
    start = time.time()
    P = locate(pwns)
    end = time.time()
    #write point into seperate files accrding to their position
    WD.toAutoCAD_points3d(P['TF'][0], 'data/output/1_upside_of_top_flange.txt', 2)
    WD.toAutoCAD_points3d(P['TF'][1], 'data/output/2_underside_of_top_flange.txt', 2)
    WD.toAutoCAD_points3d(P['W'][0], 'data/output/3_leftside_of_web.txt', 2)
    WD.toAutoCAD_points3d(P['W'][1], 'data/output/4_rightside_of_web.txt', 2)
    WD.toAutoCAD_points3d(P['BF'][0], 'data/output/5_upside_of_bottom_flange.txt', 2)
    WD.toAutoCAD_points3d(P['BF'][1], 'data/output/6_underside_of_bottom_flange.txt', 2)

    #the whole model
    WD.toAutoCAD_points3d(points, 'data/output/whole.txt', 2)
    print('Time=', end - start, 's')
