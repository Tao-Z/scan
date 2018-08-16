import ReadData as RD
import Locate as Lc
import Boundary as Bd
import Plate
import WriteData as WD
import numpy as np

class beam:
    def __init__(self, filename):
        self.points = RD.vertices(filename)
        sorted_points = Lc.locate(self.points)
        self.plates = []
        for key in sorted_points:
            points1 = sorted_points[key][0]
            points2 = [[],[]]
            for i in range(len(sorted_points[key])):
                points2[0].extend(sorted_points[key][i][0])
                points2[1].extend(sorted_points[key][i][1])
            self.plates.append(Plate.plate(key, points1, points2))  
        
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
        WD.toAbaqus(self.plates, filename, job_name, model_name)

if __name__ == '__main__':
    import time
    begin = time.time()
    beam1 = beam('data/input/sh_0411.obj')
    for plate in beam1.plates:
        print(plate.name)
        print(plate.line)
        print('')
    #beam1.mesh()
    #beam1.toAutoCAD('data/output/shell_model.txt')
    #beam1.toAutoCAD_thick('data/output/shell_model_thick.txt')
    #beam1.toAbaqus('data/output/Abaqus.inp', 'Job-1', 'Model-1')
    #beam1.boundary_to_AutoCAD('data/output/segment.txt')
    end = time.time()
    print('time =', end - begin)
