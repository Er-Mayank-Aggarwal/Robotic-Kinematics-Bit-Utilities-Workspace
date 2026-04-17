'''
11. Tabulate the values of α and β for all rack positions
Note the minimum and maximum values of α and β
Output format:

Robot Rack: Co-ordinates for checker pick-up:
[-48.00, 96.00] [-24.00, 96.00] [0.00, 96.00] [24.00, 96.00] [48.00, 96.00] [72.00, 96.00]
[-48.00, 72.00] [-24.00, 72.00] [0.00, 72.00] [24.00, 72.00] [48.00, 72.00] [72.00, 72.00]

Corresponding Rack Robot: Angles [alpha, beta] for checker pick-up:
[α11, β11] [α12, β12] [α13, β13] [α14, β14] [α15, β15] [α16, β16]
[α21, β21] [α22, β22] [α23, β23] [α24, β24] [α25, β25] [α26, β26]


'''

import numpy as np

L1 = L2 = 65

rack = [ (-48 + c*24, 96 - r*24) for r in range(2) for c in range(6)]

def solve(dx, dy):
    d = np.sqrt(dx**2 + dy**2)
    cos_beta = (L1**2 + L2**2 - d**2) / (2 * L1 * L2)
    beta = np.degrees(np.arccos(np.clip(cos_beta, -1, 1)))

    phi = np.arctan2(dy, dx)
    cos_delta = (L1**2 + d**2 - L2**2) / (2 * L1 * d)
    delta = np.arccos(np.clip(cos_delta, -1, 1))

    alpha = np.degrees(phi + delta)
    return alpha, beta

print("Rack Coordinates:")
for i in range(2):
    print(rack[i*6:(i+1)*6])
print("\nAngles [α, β]:")
alphas, betas = [], []

for i in range(2):
    row = rack[i*6:(i+1)*6]
    out = []
    for x, y in row:
        a, b = solve(x, y)
        out.append(f"[{a:.2f},{b:.2f}]")
        alphas.append(a)
        betas.append(b)
    print(" ".join(out))

print(f"\nα min/max: {min(alphas):.2f}, {max(alphas):.2f}")
print(f"β min/max: {min(betas):.2f}, {max(betas):.2f}")