import Boundary as Bd
import Mesh
import Transform as Tf
import copy
import numpy as np
import WriteData as WD

class plate:
    def __init__(self, name, points):
        self.name = name
        self.points = copy.deepcopy(points)
        self.keypoint = Bd.plane(self.points, self.name)
        self.boundary, self.step = Bd.boundary(self.points, self.keypoint, 5)
        self.line = []
        self.segments = []

    def add_segment(self, segment):
        self.segments.append(segment)
        seg = copy.deepcopy(segment)
        Tf.bystep(seg, self.step)
        seg = [seg[i][0:2] for i in range(len(seg))]
        Bd.add_segment(self.boundary, seg)

    def mesh(self):
        self.mesh = Mesh.mesh(self)
        self.segment_nums = [[] for i in range(len(self.segments))]
        for i in range(len(self.segments)):
            for j in range(len(self.segments[i])):
                for k in range(len(self.mesh['vertices'])):
                    if Bd.P2P(self.segments[i][j], self.mesh['vertices'][k]) < 1e-5:
                        self.segment_nums[i].append(k)
                        break
        '''
        print('segment1')
        for segment_num in self.segment_nums:
            for num in segment_num:
                print(self.mesh['vertices'][num])
            print('')
        print('segment2')
        for segment in self.segments:
            for point in segment:
                print(point)
            print('')
        '''


    def boundary_to_AutoCAD(self, filename, opt='w'):
        self.get_boundary_3D()
        ver = self.boundary_3D['vertices']
        with open(filename, opt) as f0:
            for seg in self.boundary_3D['segments']:
                print('line %f,%f,%f %f,%f,%f ' % (ver[seg[0]][0],ver[seg[0]][1],ver[seg[0]][2],ver[seg[1]][0],ver[seg[1]][1],ver[seg[1]][2]), file = f0)

    def toAutoCAD(self, filename, opt='w'):
        WD.toAutoCAD_triangle(self.mesh, filename, opt)

    def toAutoCAD_thick(self, filename, opt='w'):
        WD.toAutoCAD_thick(self.mesh, self.name, filename, opt)

    def get_boundary_3D(self):
        r_step = Tf.reverse(self.step)
        vertices = copy.deepcopy(self.boundary['vertices'])
        segments = copy.deepcopy(self.boundary['segments'])
        for i in range(len(vertices)):
            vertices[i] = np.append(vertices[i], 0)
        Tf.bystep(vertices, r_step)
        self.boundary_3D = {'vertices': vertices, 'segments': segments}
