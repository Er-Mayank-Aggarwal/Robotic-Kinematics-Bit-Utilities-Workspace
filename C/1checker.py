"""
Q1: Robot Rack Coordinates (2D array generation)
Corrected and accurate version of the provided example.
Uses 2D list (or numpy) to generate exactly the required output format.
Robot Rack: Co-ordinates for checker pick-up:
[-48.00, 96.00] [-24.00, 96.00] [0.00, 96.00] [24.00, 96.00] [48.00, 96.00] [72.00, 96.00]
[-48.00, 72.00] [-24.00, 72.00] [0.00, 72.00] [24.00, 72.00] [48.00, 72.00] [72.00, 72.00]
"""

# import numpy as np

# Rack: 2 rows, 6 columns
# x: -48 to 72 step 24mm
# y: 96 and 72
rack_coords = []
x_start = -48.0
y_values = [96.0, 72.0]
for row in range(2):
    row_coords = []
    for col in range(6):
        x = x_start + col * 24.0
        y = y_values[row]
        row_coords.append([round(x, 2), round(y, 2)])
    rack_coords.append(row_coords)

print("Robot Rack: Co-ordinates for checker pick-up:")
for row in rack_coords:
    print(' '.join(f"[{x:.2f}, {y:.2f}]" for x, y in row))


