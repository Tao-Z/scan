#compare with Artec

import time
import math
import ReadData as RD
import Locate as Lc
import GetZ as GZ
import GetThick as GT
from openpyxl import Workbook

start = time.time()
Point = RD.vertices('data/input/sh_0411.obj')
P = Lc.locate(Point)
face1 = []
face2 = []
for point in P['LW']:
    face1.append(point)
for point in P['RW']:
    face2.append(point)

face1.sort()
face2.sort()

t = {'vertices':[[-84.08,-175.82], [-44.15,-175.83], [-4.18,-175.88], [35.84,-175.84], [76.0,-175.84], [-84.2,-165.92], [-44.18,-165.92], [-4.13,-165.82], [35.86,-165.85], [75.84,-165.96]]}
GZ.getz(t, face1, face2, 2, 20)
GT.thick(t, face1, face2, 2, 20)

#write data to excel
wb = Workbook()

#sheet1
ws1 = wb.active
ws1.title = 'vertices'
ws1.append(['point', 'x', 'y', 'z', 'R1', 'a1', 'b1', 'R2', 'a2', 'b2'])
for i in range(len(t['vertices'])):
    ws1.append([i+1, t['vertices'][i][0], t['vertices'][i][1], t['z'][i], t['R1'][i], t['a1'][i], t['b1'][i],
    t['R2'][i], t['a2'][i], t['b2'][i]])

#sheet2
ws2 = wb.create_sheet(title = 'thick')
P = ['point']
P.extend(list(range(1, 11)))
P.extend(['RMS', 'Max'])
ws2.append(P)

T = ['thick_Artec']
T.extend([7.2, 6.77, 6.82, 6.97, 6.51, 6.17, 7.16, 7.39, 6.22, 5.67])
ws2.append(T)

T0 = ['thick0']
T0.extend(t['thick0'])
ws2.append(T0)

T1 = ['thick1']
T1.extend(t['thick1'])
ws2.append(T1)

T2 = ['thick2']
T2.extend(t['thick2'])
ws2.append(T2)

error_0 = ['error_0']
for i in range(1, 11):
    error_0.append(100 * (T0[i] - T[i]) / T[i])
RMS = math.sqrt(sum(map(lambda x:x**2, error_0[1:11])) / 10)
error_0.append(RMS)
error_0.append(max(map(lambda x:abs(x), error_0[1:11])))
ws2.append(error_0)

error_1 = ['error_1']
for i in range(1, 11):
    error_1.append(100 * (T1[i] - T[i]) / T[i])
RMS = math.sqrt(sum(map(lambda x:x**2, error_1[1:11])) / 10)
error_1.append(RMS)
error_1.append(max(map(lambda x:abs(x), error_1[1:11])))
ws2.append(error_1)

error_2 = ['error_2']
for i in range(1, 11):
    error_2.append(100 * (T2[i] - T[i]) / T[i])
RMS = math.sqrt(sum(map(lambda x:x**2, error_2[1:11])) / 10)
error_2.append(RMS)
error_2.append(max(map(lambda x:abs(x), error_2[1:11])))
ws2.append(error_2)

std_z1 = ['std_z1']
std_z1.extend(t['std_z1'])
ws2.append(std_z1)

std_z2 = ['std_z2']
std_z2.extend(t['std_z2'])
ws2.append(std_z2)

wb.save('data/output/thickness_Artec.xlsx')
end = time.time()
print('Time=', end - start)
