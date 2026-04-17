'''
12. Tabulate the values of α and β for all board positions
Note the minimum and maximum values of α and β
'''

# Q12: Board coordinates and angles

import numpy as np

L1 = L2 = 65

board = [(24 + c*24, 48 - r*24) for r in range(5) for c in range(5)]

def solve(dx, dy):
    d = np.sqrt(dx**2 + dy**2)
    cos_beta = (L1**2 + L2**2 - d**2) / (2 * L1 * L2)
    beta = np.degrees(np.arccos(np.clip(cos_beta, -1, 1)))

    phi = np.arctan2(dy, dx)
    cos_delta = (L1**2 + d**2 - L2**2) / (2 * L1 * d)
    delta = np.arccos(np.clip(cos_delta, -1, 1))

    alpha = np.degrees(phi + delta)
    return alpha, beta

alphas, betas = [], []

for i in range(5):
    row = board[i*5:(i+1)*5]
    out = []
    for x, y in row:
        a, b = solve(x, y)
        out.append(f"[{a:.2f},{b:.2f}]")
        alphas.append(a)
        betas.append(b)
    print(" ".join(out))

print(f"\nα min/max: {min(alphas):.2f}, {max(alphas):.2f}")
print(f"β min/max: {min(betas):.2f}, {max(betas):.2f}")