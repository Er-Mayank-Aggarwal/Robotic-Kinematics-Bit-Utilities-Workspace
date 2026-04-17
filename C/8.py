"""
8. The initial position of TL_RAM is Home Position (see assumptions)
What will be the value of Alpha (α) and Beta (β) if [dx, dy] = [board_row_1, board_column_4] = [96.00, 48.00]
"""
import numpy as np
import matplotlib.pyplot as plt

L1 = 65
L2 = 65

dx, dy = 96, 48

# Solve angles
r = np.sqrt(dx**2 + dy**2)
theta = np.arctan2(dy, dx)

cos_gamma = (L1**2 + L2**2 - r**2) / (2 * L1 * L2)
gamma = np.arccos(cos_gamma)
beta = np.pi - gamma

cos_phi = (L1**2 + r**2 - L2**2) / (2 * L1 * r)
phi = np.arccos(cos_phi)
alpha = theta + phi

print(f"value of alpha and beta = {np.degrees(alpha)} and {np.degrees(beta)}")

# Animate
alphas = np.linspace(np.pi/2, alpha, 50)
betas  = np.linspace(np.pi/2, beta, 50)
print(f"alphas = {alphas} \n betas = {betas}")
plt.figure()

for a, b in zip(alphas, betas):
    plt.cla()

    # Joint positions
    x0, y0 = 0, 0
    x1 = L1 * np.cos(a)
    y1 = L1 * np.sin(a)

    x2 = x1 + L2 * np.cos(a - b)
    y2 = y1 + L2 * np.sin(a - b)

    # Draw links
    plt.plot([x0, x1], [y0, y1], marker='o')  # Link1
    plt.plot([x1, x2], [y1, y2], marker='o')  # Link2

    # Draw triangle line (r)
    plt.plot([x0, dx], [y0, dy], linestyle='dashed')

    # Points
    plt.scatter([x0, x1, x2], [y0, y1, y2])
    plt.scatter(dx, dy)

    # Labels for points
    plt.text(x0, y0, " Origin (0,0)")
    plt.text(x1, y1, " Elbow")
    plt.text(dx, dy, " Target")

    # Length labels
    plt.text((x0+x1)/2, (y0+y1)/2, " L1")
    plt.text((x1+x2)/2, (y1+y2)/2, " L2")
    plt.text((x0+dx)/2, (y0+dy)/2, " r")

    # Angle labels (in degrees)
    plt.text(5, 5, f"α = {np.degrees(a):.1f}°")
    plt.text(x1+5, y1, f"β = {np.degrees(b):.1f}°")
    plt.text(x1-20, y1+10, f"γ = {np.degrees(gamma):.1f}°")

    # φ label near origin
    plt.text(20, 0, f"φ = {np.degrees(theta):.1f}°")

    # Setup
    plt.xlim(0, 120)
    plt.ylim(0, 120)
    plt.title("2-Link Arm with Variables")
    plt.grid()

    plt.pause(0.05)

plt.show()