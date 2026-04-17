""" core idea: The object move but does not rotate with link
    That is: Position changes but Orientation is fix

    thus in transformation matrix -> only translation motion 

    T = [
        [cos, -sin, x],
        [sin,  cos, y],
        [0,    0,   1]
        ]


    Becomes (theta = 0)
    T = [
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
        ]


"""

import numpy as np
import matplotlib.pyplot as plt

def hut_local():

    """ 
    x coordinate, y coordinate, unit 1 
    p0 [0,0]        p1 [4,0]       p2[4,3]
    p3 [2,5]        p4 [0,3]       p5 [0,0]
    """
    return np.array([
        [0,4,4,2,0,0],
        [0,0,3,5,3,0],
        [1,1,1,1,1,1]
    ])


def transform(T,points):
    return T @ points

r=10

plt.ion()
fig,ax = plt.subplots()


while True:

    for deg in range(0,361,10):
        theta=np.radians(deg)

        #Joint positions
        x = r*np.cos(theta)
        y = r*np.sin(theta)

        #Only translation (no rotation)
        T= np.array([
            [1,0,x],
            [0,1,y],
            [0,0,1]
        ])

        hut = hut_local()
        transformed = transform(T,hut)

        ax.clear()
        ax.plot([0,x],[0,y],'b-',linewidth=4)
        ax.plot(transformed[0],transformed[1],'k-')
        text = ax.text(-18,5, "", fontsize=12)
        text.set_text(
            f"x: {x:.2f}\n"
            f"y: {y:.2f}\n"
            
        )
        ax.set_xlim(-20,20)
        ax.set_ylim(-20,20)
        ax.set_aspect('equal')
        ax.set_title("Rotation of Hut (absolute)")
        ax.grid()

        plt.pause(0.2)