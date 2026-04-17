"""
6) In a TL_ram if the arm is resting on positive horizontal axis, and Link 2 is rotated clockwise 30 degree what will be the new coordinate of the gripper tip?

"""

import numpy as np

L1 = 65
L2 = 65

# Initial configuration
t1 = 0                      # Link 1 along x-axis
t2 = -np.radians(30)        # clockwise rotation

# Joint 1
x1 = L1 * np.cos(t1)
y1 = L1 * np.sin(t1)

# End effector
x2 = x1 + L2 * np.cos(t1 + t2)
y2 = y1 + L2 * np.sin(t1 + t2)

print("Q6 Gripper:", (round(x2,2), round(y2,2)))