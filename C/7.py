"""
7) In a TL_RAM if the arm is resting on positive horizontal axis, and Link 1 is rotated 45 degree clockwise what will new coordinates of gripper tip?
(consider assumptions mentioned)
"""
import numpy as np
# Link 1 rotates, Link 2 stays aligned
L1,L2=65,65
t1 = -np.radians(45)
t2 = 0

x1 = L1 * np.cos(t1)
y1 = L1 * np.sin(t1)

x2 = x1 + L2 * np.cos(t1 + t2)
y2 = y1 + L2 * np.sin(t1 + t2)

print("Gripper:", (round(x2,2), round(y2,2)))