"""
Assume a line sengment L2 (65mm) from [65,0] to [135,0] if L2 is rotated clockwise 30 degree wrt [65,0], what will be new coordinates
Now the rotation is about some arbitary point
steps:
shift to origin -> Rotate -> SHift back
"""


import numpy as np
import matplotlib.pyplot as plt

#Joint (pivot)

joint = np.array([65,0,1])

#End point

point = np.array([135,0,1])

# Shift to origin
relative = point - joint

# rotation
theta = np.radians(-30) # clockwise

T = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0,              0,             1]
])

rotated = T @ relative

#shift back
final = rotated + joint

print("new coordinate: " ,(round(final[0],2), round(final[1],2)))
