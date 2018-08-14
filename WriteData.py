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
        Node_begin = [1]
        for plate in plates.values():
            v = plate.mesh['vertices']
            z = plate.mesh['z']
            for i in range(len(v)):
                print('%d, %f, %f, %f' % (Node_begin[-1] + i, v[i][0], v[i][1], z[i]), file = f0)
            Node_begin.append(Node_begin[-1] + len(v))

        print('*Element, type=S3', file = f0)
        Ele_begin = [1]
        i = 0
        for plate in plates.values():
            t = plate.mesh['triangles']
            for j in range(len(t)):
                print('%d, %d ,%d ,%d' % (Ele_begin[-1]+j, t[j][0]+Node_begin[i], t[j][1]+Node_begin[i], t[j][2]+Node_begin[i]), file = f0)
            Ele_begin.append(Ele_begin[-1] + len(t))
            i += 1
        
        i = 0
        for plate in plates.values():
            print('*Elset, elset=%s, generate' % plate.name, file = f0)
            print(Ele_begin[i], Ele_begin[i+1] - 1, 1, file = f0)
        
        print('*Nodal Thickness', file = f0)
        i = 0
        offset = {'TF':' offset=SPOS,', 'BF':' offset=SNEG,'}
        for plate in plates.values():
            v = plate.mesh['vertices']
            for j in range(len(v)):
                print(Node_begin[i] + j, plate.mesh['thick1'][j], file = f0)
            print('** Section: Sect_%s' % plate.name, file = f0)
            print('*Shell General Section, elset=%s, material=Steel,%s nodal thickness' % (plate.name, offset.get(plate.name, '')), file = f0)
            print('1.,', file = f0)
            i += 1
        
        print('''
*End Part
**  
**
** ASSEMBLY
**
*Assembly, name=Assembly
**  
*Instance, name=PART-1-1, part=PART-1
*End Instance
**  
              ''', file = f0)
        