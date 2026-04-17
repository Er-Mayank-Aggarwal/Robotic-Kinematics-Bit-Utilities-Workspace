'''
14. Is it feasible for the Servo motors [MG996R] to move the gripper tip to [board_row_5, board_column_5] ? Why?

'''
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

alpha, beta = solve(120, -48)   # [board_row_5, board_column_5]
print(f"THe beta = {beta}")

# for gripper tip we will se the beta angle

if 0 <= beta <= 180:
    print("Yes feasible")
else:
    print("Not feasible")

'''
15. If the answer to the above question is No and we still want to use the same motors,
then what other parameters can be modified to make it feasible. What is your solution.
'''
print("""
    to reduce B increase Link Length (L1 or L2)
      Move robot base position
      use high servo range (> 180)

""")
