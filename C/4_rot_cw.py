"""
Assume a line segment L1 from [0,0] to [65,0]
if L1 is rotated clockwise 30 wrt origin. new coordinates will be?


T = [
        [cos, -sin, x],
        [sin,  cos, y],
        [0,    0,   1]
        ]


"""
import numpy as np
import matplotlib.pyplot as plt

# Link length (corrected)
L = 65

# Point in homogeneous form
point = np.array([L, 0, 1])

# Angle
theta = np.radians(-30)   # a clockwise angle is negative 

# Rotation matrix (about origin)
T = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0,              0,             1]
])

# Transform
rotated_point = T @ point

# Extract
x_new, y_new = rotated_point[0], rotated_point[1]
print("Original Point:", (L, 0))
print("New Rotated Point:", (round(x_new,2), round(y_new,2)))


# Plot
plt.plot([0, L], [0, 0], 'b-', linewidth=3, label="Original Link")
plt.plot([0, x_new], [0, y_new], 'r-', linewidth=3, label="Rotated Link")

plt.scatter([L, x_new], [0, y_new])

# Show coordinates on plot
plt.text(L, 0, f"({L}, 0)", fontsize=10, color='blue')

plt.text(x_new, y_new,
         f"({round(x_new,2)}, {round(y_new,2)})",
         fontsize=10,
         color='red')


plt.legend()
plt.grid()
plt.gca().set_aspect('equal')
plt.title("Robotics Rotation using Transformation Matrix")
plt.show()