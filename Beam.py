import ReadData as RD
import Locate as Lc
import Boundary as Bd
import Plate
import WriteData as WD

class beam:
    def __init__(self, filename):
        self.points = RD.vertices(filename)
        sorted_points = Lc.locate(self.points)
        self.plates = {}
        for key in sorted_points:
            points1 = sorted_points[key][0]
            points2 = [[],[]]
            for i in range(len(sorted_points[key])):
                points2[0].extend(sorted_points[key][i][0])
                points2[1].extend(sorted_points[key][i][1])
            self.plates[key] = Plate.plate(key, points1, points2)

        self.inter_segment = []
        self.inter_segment.append(Bd.intersect_of_plate(self.plates['W'], self.plates['TF']))
        self.inter_segment.append(Bd.intersect_of_plate(self.plates['W'], self.plates['BF']))

        for segment in self.inter_segment:
            Bd.sub_segment(segment, 10)
        
        self.plates['W'].add_segment(self.inter_segment[0])
        self.plates['TF'].add_segment(self.inter_segment[0])
        self.plates['W'].add_segment(self.inter_segment[1])
        self.plates['BF'].add_segment(self.inter_segment[1])

    def mesh(self):
        for plate in self.plates.values():
            plate.mesh()

    def toAutoCAD(self, filename):
        opt = 'w'
        for plate in self.plates.values():
            plate.toAutoCAD(filename, opt)
            opt = 'a'

    def toAutoCAD_thick(self, filename):
        opt = 'w'
        for plate in self.plates.values():
            plate.toAutoCAD_thick(filename, opt)
            opt = 'a'

    def boundary_to_AutoCAD(self, filename):
        opt = 'w'
        for plate in self.plates.values():
            plate.boundary_to_AutoCAD(filename, opt)
            opt = 'a'

    def toAbaqus(self, filename, job_name, model_name):
        WD.toAbaqus(self.plates, filename, job_name, model_name)

if __name__ == '__main__':
    import time
    begin = time.time()
    beam1 = beam('data/input/sh_0411.obj')
    beam1.mesh()
    #beam1.toAutoCAD('data/output/shell_model.txt')
    #beam1.toAutoCAD_thick('data/output/shell_model_thick.txt')
    #beam1.toAbaqus('data/output/Abaqus.inp', 'Job-1', 'Model-1')
    #beam1.boundary_to_AutoCAD('data/output/segment.txt')
    end = time.time()
    print('time =', end - begin)
