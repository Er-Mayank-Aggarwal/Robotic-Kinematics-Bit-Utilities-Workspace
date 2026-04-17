# import numpy as np
# import matplotlib.pyplot as plt

# def plot_robotic_arm(theta1=30, theta2=45, L1=11, L2=14):
#     """Plots a 2-link robotic arm given joint angles and link lengths."""
    
#     # Convert to radians
#     t1 = np.radians(theta1)
#     t2 = np.radians(theta2)

#     # Joint positions
#     x0, y0 = 0, 0

#     x1 = L1 * np.cos(t1)
#     y1 = L1 * np.sin(t1)

#     x2 = x1 + L2 * np.cos(t1 + t2)
#     y2 = y1 + L2 * np.sin(t1 + t2)

#     # Plot links
#     plt.plot([x0, x1], [y0, y1], 'b-', linewidth=4, label='Link 1')
#     plt.plot([x1, x2], [y1, y2], 'g-', linewidth=4, label='Link 2')

#     # Plot joints
#     plt.scatter([x0, x1, x2], [y0, y1, y2], c=['red','orange','purple'], s=100)

#     plt.text(x1, y1, f'θ1={theta1}°')
#     plt.text(x2, y2, f'θ2={theta2}°')

#     plt.axis('equal')
#     plt.grid()
#     plt.title("2-Link Robotic Arm (With Angles)")
#     plt.legend()
#     plt.show()
    
# if __name__ == "__main__":
#     # Now you can easily test different angles by calling the function!
#     plot_robotic_arm(theta1=45, theta2=90)

import numpy as np
import matplotlib.pyplot as plt

def plot_arm(theta1 = 30 , theta2 = 60, L1 = 45, L2 = 50):
    angle1 = np.radians(theta1)
    angle2 = np.radians(theta2)

    x0,y0 = 0,0

    x1 = x0 + L1*np.cos(angle1)
    y1 = y0 + L1*np.sin(angle1)

    x2 = x1 + L2*np.cos(angle1+angle2)
    y2 = y1 + L2*np.sin(angle1+angle2)

    plt.plot([x0,x1],[y0,y1],'b-',linewidth=4,label = 'Link 1')
    plt.plot([x1,x2],[y1,y2],'g-',linewidth=4,label = 'Link 2')

    plt.scatter([x0,x1,x2],[y0,y1,y2],c=['red','green','orange'],s=100)

    plt.text(x1,y1,f'theta11={theta1}')
    plt.text(x2,y2,f'theta11={theta2}')

    plt.axis('equal')
    plt.grid()
    plt.title('2 link arm')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot_arm(theta1=30,theta2=45)