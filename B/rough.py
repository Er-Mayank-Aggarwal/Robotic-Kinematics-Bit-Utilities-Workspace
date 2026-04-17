#3 link rotation

import matplotlib.pyplot as plt
import numpy as np

plt.ion()
fig,ax = plt.subplots()

L1, L2, L3 = 11, 14, 7

line, = ax.plot([],[],'-o',linewidth=3)
text = ax.text(-18,15,"",fontsize=10)

ax.set_xlim(-25,25)
ax.set_ylim(-25,25)
ax.set_aspect('equal')
ax.grid()

while True:
    for deg in range(0,361,10):
        t = np.radians(deg)

        t1 = t
        t2 = 0.5*t
        t3 = -0.7*t

        t12 = t1 + t2
        t123 = t1 + t2 + t3

        x0,y0 = 0,0
        x1 = L1*np.cos(t1)
        y1 = L1*np.sin(t1)

        x2 = x1 + L2*np.cos(t12)
        y2 = y1 + L2*np.sin(t12)

        x3 = x2 + L3*np.cos(t123)
        y3 = y2 + L3*np.sin(t123)

        line.set_data([x0,x1,x2,x3],[y0,y1,y2,y3])

        text.set_text(
            f"θ1={np.degrees(t1):.1f}°\n"
            f"θ2={np.degrees(t2):.1f}°\n"
            f"θ3={np.degrees(t3):.1f}°"
        )

        plt.pause(0.3)