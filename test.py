import Transform as Tf
import sympy
from math import pi
import numpy as np
x, y = sympy.symbols('x y')
line = x + y
point = [4,5,6]
step = [['m', np.array([1,2,3])], ['rz', pi/3]]
r_step = Tf.reverse(step)
line1 = Tf.bystep_line(line, step)
print('line1')
print(line1)
line2 = Tf.bystep_line(line1, r_step)
print('line2')
print(line2)