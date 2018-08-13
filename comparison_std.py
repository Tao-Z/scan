import time
import math
import ReadData as RD
import Locate as Lc
import GetZ as GZ
from openpyxl import Workbook
import numpy as np
import copy
import matplotlib.pyplot as plt

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

t = {'vertices':[[-84.08,-175.82],[-44.15,-175.83],[-4.18,-175.88],[35.84,-175.84],[76.0,-175.84],[-84.2,-165.92],[-44.18,-165.92],[-4.13,-165.82],[35.86,-165.85],[75.84,-165.96],
[-78.12,45.56],[-38.08,45.59],[1.91,45.62],[41.91,45.62],[81.91,45.62]]}
T = [7.2, 6.77, 6.82, 6.97, 6.51, 6.17, 7.16, 7.39, 6.22, 5.67, 9.64, 9.58, 9.52, 9.48, 9.44]

t_result = []
for R in np.arange(0.5, 5.1, 0.1):
    tx = copy.deepcopy(t)
    t_result.append(GZ.getz(tx, face1, face2, R, 1))

#write data to excel
wb = Workbook()

#sheet and figure
ws1 = wb.active
ws1.title = 'vertices'
fig1 = plt.figure()
fig1.canvas.set_window_title('error/standard deviation with radius')
fig2 = plt.figure()
fig2.canvas.set_window_title('error with standard deviation')
fig3 = plt.figure()
fig3.canvas.set_window_title('θ with radius')
for i in range(len(t['vertices'])):
    ws1.append(['Point'+str(i+1), t['vertices'][i][0], t['vertices'][i][1], 'thick', T[i]])

    R = ['R']
    R.extend(list(np.arange(0.5, 5.1, 0.1)))
    ws1.append(R)

    #error statistic
    #write to excel
    error_0 = ['error_0(%)']
    for res in t_result:
        T0 = res['thick0'][i]
        error_0.append(100 * abs(T0-T[i]) / T[i])
    ws1.append(error_0)

    #draw the figure
    color = 'tab:red'
    ax1 = fig1.add_subplot(3, 5, i+1)
    ax1.set_xlabel('radius/mm')
    ax1.set_ylabel('error(%)', color = color)
    ax1.set_xlim([0, 5])
    if i < 5:
        ax1.set_ylim([0, 10])
    elif i < 10:
        ax1.set_ylim([0, 5])
    else:
        ax1.set_ylim([0, 0.1])
    ax1.plot(R[1:], error_0[1:], color = color)
    ax1.tick_params(axis = 'y', labelcolor = color)

    #std statistic
    #write to excel
    std = ['std']
    for res in t_result:
        std_z1 = res['std_z1'][i]
        std_z2 = res['std_z2'][i]
        std.append((std_z1 + std_z2) / 2)
    ws1.append(std)

    #draw the figure
    color = 'tab:blue'
    ax2 = ax1.twinx()
    ax2.set_ylabel('standard deviation', color=color)
    if i < 5:
        ax2.set_ylim([0, 1])
    elif i < 10:
        ax2.set_ylim([0, 0.8])
    else:
        ax2.set_ylim([0, 0.05])
    ax2.plot(R[1:], std[1:], color = color)
    ax2.tick_params(axis='y', labelcolor = color)

    #draw the figure of relationship between error and std
    ax3 = fig2.add_subplot(3, 5, i+1)
    ax3.set_xlabel('standard deviation')
    ax3.set_ylabel('error(%)')
    if i < 5:
        ax3.set_xlim([0, 1])
        ax3.set_ylim([0, 10])
    elif i < 10:
        ax3.set_xlim([0, 0.8])
        ax3.set_ylim([0, 5])
    else:
        ax3.set_xlim([0, 0.05])
        ax3.set_ylim([0, 0.1])
    ax3.scatter(std[1:], error_0[1:], marker='.')

    #theta statistic
    theta = ['theta']
    for res in t_result:
        theta.append(res['theta'][i])
    ws1.append(theta)

    #draw the figure of relationship between theta and radius
    ax4 = fig3.add_subplot(3, 5, i+1)
    ax4.set_xlabel('radius/mm')
    ax4.set_ylabel('θ/rad')
    ax4.set_xlim([0, 5])
    if i<10:
        ax4.set_ylim([0, 1])
    else:
        ax4.set_ylim([0, 0.05])
    ax4.plot(R[1:], theta[1:])

    ws1.append([])

wb.save('data/output/thickness_std.xlsx')
fig1.subplots_adjust(left=0.05, right=0.95, top=0.98, bottom=0.07, hspace=0.3, wspace=0.8)
fig2.subplots_adjust(left=0.05, right=0.98, top=0.98, bottom=0.07, hspace=0.3, wspace=0.35)
fig3.subplots_adjust(left=0.05, right=0.98, top=0.98, bottom=0.07, hspace=0.3, wspace=0.35)
end=time.time()
print('Time=', end - start)
plt.show()
