import triangle as tri
import matplotlib.pyplot as plt
import copy
import Transform as Tf
import GetZ as GZ
import GetThick as GT
import Refine as Rf
import Triplot as Tplt
import time

def mesh(plate):
    points = copy.deepcopy(plate.points_scan)
    boundary = plate.boundary
    Tf.bystep(points[0], plate.step)
    Tf.bystep(points[1], plate.step)
    points[0].sort()
    points[1].sort()
    t=tri.triangulate(boundary,'Dpq30a4000')
    num_point = len(t['vertices'])
    num_element = len(t['triangles'])
    print(0, num_point, num_element)
    #ax = plt.subplot(2,3,i, aspect='equal')
    #Tplt.plot(ax, **t)

    GZ.getz(t, points[0], points[1], 1, 5, plate.name, plate.line)
    #GT.thick(t, face1, face2, 2, 20)

    #parameters of refinement
    k1 = 15
    k2 = 4
    d2 = 40
    k3 = 1.5
    d3 = 5

    #refine1
    for i in range(1,10):
        time1 = time.time()
        GZ.midthick(t, points[0], points[1] , 1, 5)
        t, m = Rf.refine1(t, k1)
        if m == 0:
            break
        num_point = len(t['vertices'])
        num_element = len(t['triangles'])
        GZ.getz(t, points[0], points[1], 1, 5, plate.name, plate.line)
        #GT.thick(t, face1, face2, 2, 20)
        time2 = time.time()
        print('refine1:', i, 'points:', num_point, 'elements:', num_element, 'time:', time2 - time1)
        #ax = plt.subplot(2,3,i, aspect='equal')
        #Tplt.plot(ax, **t)
    '''
    #refine2
    for i in range(1,10):
        time1 = time.time()
        t, m = Rf.refine2(t, k2, d2)
        if m == 0:
            break
        num_point = len(t['vertices'])
        num_element = len(t['triangles'])
        GZ.getz(t, points[0], points[1], 1, 5, plate.name, plate.line)
        #GT.thick(t, face1, face2, 1, 10)
        time2 = time.time()
        print('refine2:', i, 'points:', num_point, 'elements:', num_element, 'time:', time2 - time1)
        #ax = plt.subplot(2, 3, i, aspect='equal')
        #Tplt.plot(ax, **t)
    '''
    #refine3
    for i in range(1,10):
        time1 = time.time()
        GZ.midthick(t, points[0], points[1], 1, 5)
        t, m = Rf.refine3(t, k3, d3)
        if m == 0:
            break
        num_point = len(t['vertices'])
        num_element = len(t['triangles'])
        GZ.getz(t, points[0], points[1], 1, 5, plate.name, plate.line)
        #GT.thick(t, face1, face2, 2, 20)
        time2 = time.time()
        print('refine3:', i, 'points:', num_point, 'elements:', num_element, 'time:', time2 - time1)
        #ax = plt.subplot(2,3,i, aspect='equal')
        #Tplt.plot(ax, **t)

    #rotate to original position
    r_step = Tf.reverse(plate.step)
    Tf.tri_step(t, r_step)
    return t


if __name__ == '__main__':
    import time
    import ReadData as RD
    import Locate as Lc
    Point = RD.vertices('data/input/sh_0411.obj')
    P = Lc.locate(Point)
    face1 = [point for point in P['DTF2']]
    face2 = [point for point in P['UTF']]
    start = time.time()
    t = mesh(face1, face2, area)
    end = time.time()
    print('Time=', end - start)
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, aspect='equal')
    Tplt.plot(ax, **t)
    #for point in t['mid_point']:
    #    ax.scatter(point[0], point[1], color = 'red', marker = '.')
    fig1.subplots_adjust(top = 0.95, bottom = 0.05)
    plt.show()
