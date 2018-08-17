import Transform as Tf
import sympy
from math import pi
import numpy as np
x, y, z= sympy.symbols('x y z')
line = 2*x + 3*y - 5*z - 12345
step = [['m', np.array([1,2,3])], ['rz', 2*pi/7], ['rx', pi/3], ['ry', 3*pi/5]]
r_step = Tf.reverse(step)
line1 = Tf.bystep_line(line, step)
print('line1')
print(line1)
line2 = Tf.bystep_line(line1, r_step)
print('line2')
print(line2)
