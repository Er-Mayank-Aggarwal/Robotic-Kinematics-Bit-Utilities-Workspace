"""


9. What will be the value of a and β if TL_RAM is moved to [board_row_5, board_column_5]
Solution: [-15.62, 167.64] See figure below and verify the correctness visually

10. What will be the value of a and β if TL_RAM is moved to [rack_row_2, rack_column_1]
Solution: [171.96, 83.46] See figure below and verify the correctness visually
"""
# Q9: Target = [120, -48]

import numpy as np

L1 = L2 = 65
DEG = np.pi / 180

def solve(dx, dy):
    d = np.sqrt(dx**2 + dy**2)

    cos_beta = (L1**2 + L2**2 - d**2) / (2 * L1 * L2)
    beta = np.degrees(np.arccos(np.clip(cos_beta, -1, 1)))

    phi = np.arctan2(dy, dx)
    cos_delta = (L1**2 + d**2 - L2**2) / (2 * L1 * d)
    delta = np.arccos(np.clip(cos_delta, -1, 1))

    alpha = np.degrees(phi + delta)

    return alpha, beta

a, b = solve(120, -48)
print(f"Alpha and beta → α = {a:.2f}°, β = {b:.2f}°")

# 10
a, b = solve(-48, 72)
print(f"Q10 → α = {a:.2f}°, β = {b:.2f}°")