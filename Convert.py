import ReadData as RD
import WriteData as WD

def obj_to_off(filename_obj, filename_off):
    points = RD.obj_vertices(filename_obj)
    faces = RD.obj_faces(filename_obj)
    WD.tooff(points, faces, filename_off)

def pwn_to_AutoCAD(filename_pwn, filename_AutoCAD):
    points = RD.pwn_points(filename_pwn)
    WD.toAutoCAD_points3d(points, filename_AutoCAD)

def pwn_to_obj(filename_pwn, filename_obj):
    points = RD.pwn_points(filename_pwn)
    normals = RD.pwn_normals(filename_pwn)
    WD.toobj(points, normals, filename_obj)
    
if __name__ == '__main__':          
    obj_to_off('data/input/half height_100k.obj', 'data/output/half height_100k.off')
    pwn_to_AutoCAD('data/cube.pwn', 'data/AutoCAD.txt')
    pwn_to_obj('data/model.obj')