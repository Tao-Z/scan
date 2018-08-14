def points3d(points, filename, dig = 0):
    with open(filename, 'w') as f0:
        for point in points:
            print('point %.*f,%.*f,%.*f' % (dig, point[0], dig, point[1], dig, point[2]), file = f0)

def toAutoCAD(tri, filename, type):
    v = tri['vertices']
    t = tri['triangles']
    z = tri['z']
    with open(filename, type) as f0:
        for i in range(len(t)):
            print('3dface ', end = '', file = f0)
            for j in range(3):
                print('%f,%f,%f' % (v[t[i][j]][0], v[t[i][j]][1], z[t[i][j]]), file = f0)
            print(' ', file = f0)

def toAutoCAD_thick(tri, p_name, filename, type):
    v = tri['vertices']
    t = tri['triangles']
    z = tri['z']
    thick = tri['thick1']
    if p_name == 'TF' or p_name == 'BF':
        if p_name == 'TF':
            y_new = [v[i][1] - thick[i] for i in range(len(v))]
        elif p_name == 'BF':
            y_new = [v[i][1] + thick[i] for i in range(len(v))]
        with open(filename, type) as f0:
            for i in range(len(t)):
                print('3dface ', end = '', file = f0)
                for j in range(3):
                    print('%f,%f,%f' % (v[t[i][j]][0], v[t[i][j]][1], z[t[i][j]]), file = f0)
                print(' ', file = f0)
            for i in range(len(t)):
                print('3dface ', end = '', file = f0)
                for j in range(3):
                    print('%f,%f,%f' % (v[t[i][j]][0], y_new[t[i][j]], z[t[i][j]]), file = f0)
                print(' ', file = f0)

    if p_name == 'W':
        y_1 = [z[i] - thick[i] / 2 for i in range(len(z))]
        y_2 = [z[i] + thick[i] / 2 for i in range(len(z))]
        with open(filename, type) as f0:
            for i in range(len(t)):
                print('3dface ', end = '', file = f0)
                for j in range(3):
                    print('%f,%f,%f' % (v[t[i][j]][0], v[t[i][j]][1], y_1[t[i][j]]), file = f0)
                print(' ', file = f0)
            for i in range(len(t)):
                print('3dface ', end = '', file = f0)
                for j in range(3):
                    print('%f,%f,%f' % (v[t[i][j]][0], v[t[i][j]][1], y_2[t[i][j]]), file = f0)
                print(' ', file = f0)

def toAbaqus(plates, filename, job_name, model_name):
    with open(filename, 'w') as f0:
        print('*Heading', file = f0)
        print('** Job name:'+job_name+'Model name:'+model_name, file = f0)
        print('*Preprint, echo=NO, model=NO, history=NO, contact=NO', file = f0)
        print('**', file = f0)
        print('** PARTS', file = f0)
        print('**', file = f0)
        print('*Part, name=Part-1', file = f0)

        print('*Node', file = f0)
        Node_begin = [0]
        for plate in plates.values():
            v = plate.mesh['vertices']
            z = plate.mesh['z']
            for i in range(len(v)):
                print('%d, %f, %f, %f' % (Node_begin[-1] + i + 1, v[i][0], v[i][1], z[i]), file = f0)
            Node_begin.append(Node_begin[-1] + len(v))

        print('*Element, type=S3', file = f0)
        Ele_begin = [0]
        i = 0
        for plate in plates.values():
            t = plate.mesh['triangles']
            for j in range(len(t)):
                print('%d, %d ,%d ,%d' % (Ele_begin[-1]+j+1, t[j][0]+Node_begin[i]+1, t[j][1]+Node_begin[i]+1, t[j][2]+Node_begin[i]+1), file = f0)
            Ele_begin.append(Ele_begin[-1] + len(t))
            i += 1

        for key in plates:
            print('*Elset, elset=' + plates[key].name + ', generate', file = f0)
            print(Ele_begin, )
        print('*Nset, nset=web', file = f0)
        pass
