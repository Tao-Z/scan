import ReadData as RD
import Locate as Lc
import Boundary as Bd
import Plate
import WriteData as WD
import numpy as np

class beam:
    def __init__(self, filename):
        points = RD.obj_vertices(filename)
        normals = RD.obj_normals(filename)
        self.pwns = [points[i] + normals[i] for i in range(len(points))]
        sorted_pwns = Lc.locate(self.pwns)
        self.plates = []
        for key in sorted_pwns:
            self.plates.append(Plate.plate(key, sorted_pwns[key]))
        
        self.intersect_matrix = np.matrix([[0,0,1],
                                           [0,0,1],
                                           [1,1,0]])
        n = 10
        self.inter_segments = []
        self.inter_segment_markers = []
        for i in range(len(self.plates)):
            for j in range(i+1, len(self.plates)):
                if self.intersect_matrix[i, j] == 1:
                    segment = Bd.intersect_of_plate(self.plates[j], self.plates[i])
                    Bd.sub_segment(segment, n)
                    self.inter_segments.append(segment)
                    self.plates[i].add_segment(segment)
                    self.plates[j].add_segment(segment)
                    self.inter_segment_markers.append([[i, len(self.plates[i].segments)-1], [j, len(self.plates[j].segments)-1]])

    def mesh(self):
        for plate in self.plates:
            plate.mesh()

    def toAutoCAD(self, filename):
        opt = 'w'
        for plate in self.plates:
            plate.toAutoCAD(filename, opt)
            opt = 'a'

    def toAutoCAD_thick(self, filename):
        opt = 'w'
        for plate in self.plates:
            plate.toAutoCAD_thick(filename, opt)
            opt = 'a'

    def boundary_to_AutoCAD(self, filename):
        opt = 'w'
        for plate in self.plates:
            plate.boundary_to_AutoCAD(filename, opt)
            opt = 'a'

    def toAbaqus(self, filename, job_name, model_name):
        WD.toAbaqus(self, filename, job_name, model_name)

if __name__ == '__main__':
    import time
    begin = time.time()
    beam1 = beam('data/input/sh_0411.obj')
    beam1.mesh()
    beam1.toAutoCAD('data/output/shell_model.txt')
    beam1.toAutoCAD_thick('data/output/shell_model_thick.txt')
    #beam1.toAbaqus('data/output/Abaqus.inp', 'Job-1', 'Model-1')
    #beam1.boundary_to_AutoCAD('data/output/segment.txt')
    end = time.time()
    print('time =', end - begin)
