"""
2. Write a program to generate the following output.

TicTacToe Game Board: Co-ordinates for checker placement:
[24.00, 48.00] [48.00, 48.00] [72.00, 48.00] [96.00, 48.00] [120.00, 48.00]
[24.00, 24.00] [48.00, 24.00] [72.00, 24.00] [96.00, 24.00] [120.00, 24.00]
[24.00, 0.00] [48.00, 0.00] [72.00, 0.00] [96.00, 0.00] [120.00, 0.00]
[24.00, -24.00] [48.00, -24.00] [72.00, -24.00] [96.00, -24.00] [120.00, -24.00]
[24.00, -48.00] [48.00, -48.00] [72.00, -48.00] [96.00, -48.00] [120.00, -48.00]


"""

import matplotlib.pyplot as plt

start_x,start_y = 24,48

# grid spacing
d = 24

coords_x, coords_y = [],[]


# to generate a 5 x 5 grid
for i in range(5):
    y = start_y - i * d
    for j in range(5):
        x = start_x + j *d        
        coords_x.append(x)
        coords_y.append(y)
        print(f"[{x:.2f},{y:.2f}]",end=",")
    print()

# Plot
plt.scatter(coords_x, coords_y, color='red')
plt.title("Board Coordinates")
plt.grid()
plt.gca().set_aspect('equal')
plt.show()