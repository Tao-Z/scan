import Boundary as Bd
import Mesh
import Transform as Tf
import copy
import numpy as np
import WriteData as WD

class plate:
    def __init__(self, name, points1, points2):
        self.name = name
        self.points_mesh = copy.deepcopy(points1)
        self.points_scan = copy.deepcopy(points2)
        self.keypoint = Bd.plane(self.points_mesh, self.name)
        self.boundary, self.step = Bd.boundary(self.points_mesh, self.keypoint, 5)
        self.line = []
        self.segments = []

    def add_segment(self, segment):
        seg = copy.deepcopy(segment)
        self.segments.append(seg)
        Tf.bystep(seg, self.step)
        seg = [seg[i][0:2] for i in range(len(seg))]
        self.line.append(Bd.getline_2D(seg[0], seg[-1]))
        Bd.add_segment(self.boundary, seg)

    def mesh(self):
        self.mesh = Mesh.mesh(self)
        '''
        self.segments_marker = []
        for segment in self.segments:
            for point in segment:
                for i in range(len(self.mesh['vertices'])):
                    if point == self.mesh['vertices']:
                        self.segments_marker.append(i)
        print(self.segments_marker)
        '''

    def boundary_to_AutoCAD(self, filename, type='w'):
        self.get_boundary_3D()
        ver = self.boundary_3D['vertices']
        with open(filename, type) as f0:
            for seg in self.boundary_3D['segments']:
                print('line %f,%f,%f %f,%f,%f ' % (ver[seg[0]][0],ver[seg[0]][1],ver[seg[0]][2],ver[seg[1]][0],ver[seg[1]][1],ver[seg[1]][2]), file = f0)

    def toAutoCAD(self, filename, type='w'):
        WD.toAutoCAD(self.mesh, filename, type)

    def toAutoCAD_thick(self, filename, type='w'):
        WD.toAutoCAD_thick(self.mesh, self.name, filename, type)

    def get_boundary_3D(self):
        r_step = Tf.reverse(self.step)
        vertices = copy.deepcopy(self.boundary['vertices'])
        segments = copy.deepcopy(self.boundary['segments'])
        for i in range(len(vertices)):
            vertices[i] = np.append(vertices[i], 0)
        Tf.bystep(vertices, r_step)
        self.boundary_3D = {'vertices': vertices, 'segments': segments}
