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
