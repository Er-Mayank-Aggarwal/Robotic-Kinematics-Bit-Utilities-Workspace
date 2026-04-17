"""
 core idea : the position and orientation both changes with link rotation


  thus in transformation matrix -> translation + rotation motion 

    T = [
        [cos, -sin, x],
        [sin,  cos, y],
        [0,    0,   1]
        ]


  

"""

import numpy as np
import matplotlib.pyplot as plt
import math

def hut_local():
    return np.array([
        [0, 4, 4, 2, 0,0],
        [0, 0, 3, 5, 3,0],
        [1, 1, 1, 1, 1,1]
    ])

def transform(T, points):
    return T @ points

r = 10

plt.ion()
fig, ax = plt.subplots()

while True:
    for deg in range(0, 361, 10):
        theta = math.radians(deg)

        x = r * math.cos(theta)
        y = r * math.sin(theta)

        # FULL transformation (rotation + translation)
        T = np.array([
            [math.cos(theta), -math.sin(theta), x],
            [math.sin(theta),  math.cos(theta), y],
            [0, 0, 1]
        ])

        hut = hut_local()
        transformed = transform(T, hut)

        ax.clear()
        ax.plot([0, x], [0, y], 'b-', linewidth=3)
        ax.plot(transformed[0], transformed[1], 'k-')
        text = ax.text(-18,5, "", fontsize=12)
        text.set_text(
            f"x: {x:.2f}\n"
            f"y: {y:.2f}\n"
            f"theta : {deg}"
        )
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        # ax.annotate(
        #     f"({x:.1f}, {y:.1f})\nθ={deg}°",
        #     (x, y),
        #     textcoords="offset points",
        #     xytext=(10,10),
        #     fontsize=10,
        #     color='black'
        # )
        ax.set_aspect('equal')
        ax.set_title("Relative Rotation (Rigid Body Motion)")
        ax.grid()

        plt.pause(0.2)