def toAutoCAD_points3d(points, filename, dig = 3):
    with open(filename, 'w') as f0:
        for point in points:
            print('point %.*f,%.*f,%.*f' % (dig, point[0], dig, point[1], dig, point[2]), file = f0)

def toAutoCAD_triangle(tri, filename, opt):
    v = tri['vertices']
    t = tri['triangles']
    z = tri['z']
    with open(filename, opt) as f0:
        for i in range(len(t)):
            print('3dface ', end = '', file = f0)
            for j in range(3):
                print('%f,%f,%f' % (v[t[i][j]][0], v[t[i][j]][1], z[t[i][j]]), file = f0)
            print(' ', file = f0)

def toAutoCAD_thick(tri, p_name, filename, opt):
    v = tri['vertices']
    t = tri['triangles']
    z = tri['z']
    thick = tri['thick1']
    if p_name == 'TF' or p_name == 'BF':
        if p_name == 'TF':
            y_new = [v[i][1] - thick[i] for i in range(len(v))]
        elif p_name == 'BF':
            y_new = [v[i][1] + thick[i] for i in range(len(v))]
        with open(filename, opt) as f0:
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
        with open(filename, opt) as f0:
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

def topwn(points, normals, filename):
    with open(filename, 'w') as f0:
        for i in range(len(points)):
            print('%f %f %f' % (points[i][0], points[i][1], points[i][2]), end = ' ', file = f0)
            print('%f %f %f' % (normals[i][0], normals[i][1], normals[i][2]), file = f0)
            
def tooff(points, faces, filename):
    with open(filename, 'w') as f0:
        print('OFF', file = f0)
        print(len(points), len(faces), 0, file = f0)
        for point in points:
            print('%f %f %f' % (point[0], point[1], point[2]), file = f0)
        for face in faces:
            print('3  %d %d %d' % (face[0], face[1], face[2]), file = f0)

            
def toobj(points, normals, filename):
    with open(filename, 'w') as f0:
        for point in points:
            print('v %f %f %f' % (point[0], point[1], point[2]), file = f0)
        for normal in normals:
            print('vn %f %f %f' % (normal[0], normal[1], normal[2]), file = f0)
            
def toAbaqus(beam, filename, job_name, model_name):
    plates = beam.plates
    with open(filename, 'w') as f0:
        print('*Heading', file = f0)
        print('** Job name: %s Model name: %s' % (job_name, model_name), file = f0)
        print('*Preprint, echo=NO, model=NO, history=NO, contact=NO', file = f0)
        print('**', file = f0)
        print('** PARTS', file = f0)
        print('**', file = f0)
        print('*Part, name=PART-1', file = f0)

        print('*Node', file = f0)
        Node_begin = [1]
        for plate in plates:
            v = plate.mesh['vertices']
            z = plate.mesh['z']
            for i in range(len(v)):
                print('%d, %f, %f, %f' % (Node_begin[-1] + i, v[i][0], v[i][1], z[i]), file = f0)
            Node_begin.append(Node_begin[-1] + len(v))

        print('*Element, type=S3', file = f0)
        Ele_begin = [1]
        i = 0
        for plate in plates:
            t = plate.mesh['triangles']
            for j in range(len(t)):
                print('%d, %d ,%d ,%d' % (Ele_begin[-1]+j, t[j][0]+Node_begin[i], t[j][1]+Node_begin[i], t[j][2]+Node_begin[i]), file = f0)
            Ele_begin.append(Ele_begin[-1] + len(t))
            i += 1

        i = 0
        for plate in plates:
            print('*Elset, elset=%s, generate' % plate.name, file = f0)
            print('%d, %d, %d' % (Ele_begin[i], Ele_begin[i+1] - 1, 1), file = f0)
            i += 1
   
        i = 0
        offset = {'TF':' offset=SPOS,', 'BF':' offset=SNEG,'}
        for plate in plates:
            print('*Nodal Thickness', file = f0)
            v = plate.mesh['vertices']
            for j in range(len(v)):
                print('%d, %f' % (Node_begin[i] + j, plate.mesh['thick1'][j]), file = f0)
            print('** Section: Sect_%s' % plate.name, file = f0)
            print('*Shell General Section, elset=%s, material=Steel,%s nodal thickness' % (plate.name, offset.get(plate.name, '')), file = f0)
            print('1.,', file = f0)
            i += 1

        print('*End Part', file = f0)
        print('**', file = f0)
        print('**', file = f0)
        print('** ASSEMBLY', file = f0)
        print('**', file = f0)
        print('*Assembly, name=Assembly', file = f0)
        print('**', file = f0)
        print('*Instance, name=PART-1-1, part=PART-1', file = f0)
        print('*End Instance', file = f0)
        print('**', file = f0)

        for i in range(len(plates)):
            for j in range(len(plates[i].segment_nums)):
                for k in range(len(plates[i].segment_nums[j])):
                    print('*Nset, nset=%s_%d_%d, instance=PART-1-1' % (plates[i].name, j, k), file = f0)
                    print('%d,' % (Node_begin[i] + plates[i].segment_nums[j][k]), file = f0 )
                    print('*Surface, type=NODE, name=%s_%d_%d_CNS_' % (plates[i].name, j, k), file = f0)
                    print('%s_%d_%d, 1.' % (plates[i].name, j, k), file = f0)
        ins_markers = beam.inter_segment_markers
        for i in range(len(ins_markers)):
            p_num_0 = ins_markers[i][0][0]
            seg_num_0 = ins_markers[i][0][1]
            p_num_1 = ins_markers[i][1][0]
            seg_num_1 = ins_markers[i][1][1]
            for j in range(len(plates[p_num_0].segment_nums[seg_num_0])):
                print('** Constraint: Constraint-%d-%d' % (i, j), file = f0)
                print('*Tie, name=Constraint-%d-%d, adjust=yes, position tolerance=0.001' % (i, j), file = f0)
                print('%s_%d_%d_CNS_,' % (plates[p_num_0].name, seg_num_0, j), end = '', file = f0)
                print(' %s_%d_%d_CNS_' % (plates[p_num_1].name, seg_num_1, j), file = f0)
        
        print('*End Assembly', file = f0)
        print('**', file = f0)
        print('** MATERIALS', file = f0)
        print('**', file = f0)
        print('*Material, name=Steel', file = f0)
        print('*Elastic', file = f0)
        print('200000., 0.3', file = f0)
        print('**', file = f0)