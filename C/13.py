'''
13. Among all the values of α and β, rack and board combined,
Note the minimum and maximum values of α and β
'''
# Q13: Combined min/max

import numpy as np

L1 = L2 = 65

points = (
    [(-48 + c*24, 96 - r*24) for r in range(2) for c in range(6)] +
    [(24 + c*24, 48 - r*24) for r in range(5) for c in range(5)]
)

def solve(dx, dy):
    d = np.sqrt(dx**2 + dy**2)
    cos_beta = (L1**2 + L2**2 - d**2) / (2 * L1 * L2)
    beta = np.degrees(np.arccos(np.clip(cos_beta, -1, 1)))

    phi = np.arctan2(dy, dx)
    cos_delta = (L1**2 + d**2 - L2**2) / (2 * L1 * d)
    delta = np.arccos(np.clip(cos_delta, -1, 1))

    alpha = np.degrees(phi + delta)
    return alpha, beta

alphas, betas = zip(*[solve(x, y) for x, y in points])

print(f"α min/max: {min(alphas):.2f}, {max(alphas):.2f}")
print(f"β min/max: {min(betas):.2f}, {max(betas):.2f}")