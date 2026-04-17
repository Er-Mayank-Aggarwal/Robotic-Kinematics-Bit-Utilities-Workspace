'''
16. If this constraint is introduced, what would be your solution?
Arena grid size / pitch / center to center distance i.e., 24mm should not be changed
Reason: assume that pine wood laser cutting for the Arena is already done
'''
print("""
Grid = 24mm fixed

Allowed changes:
- Change L1 / L2
- Move base
- Change servo

Best: Increase L2
""")



'''
17. If this constraint is introduced, what would be your solution?
Arena grid size / pitch / center to center distance i.e., 24mm should not be changed
Reason: assume that pine wood laser cutting for the Arena is already done
and L1 should NOT be changed
Reason: Assume that Link_1 is already 3D-printed
What should be changed and how much ?
HINT: One of the possible solution:

'''

# l1 is already fixed so optimal L2 to be find i.e minimum value

import numpy as np
L1 = 65

def beta_val(L2):
    dx,dy = 120 , -48
    d = np.sqrt(dx**2 + dy**2)
    cos_beta = (L1**2 + L2**2 - d**2) / (2 * L1 * L2)
    return np.degrees(np.arccos(np.clip(cos_beta, -1, 1)))
for L2 in range(1, 200):
    d = np.sqrt(120**2 + (-48)**2)
    if abs(L1-L2) <= d <= (L1+L2):
        b = beta_val(L2)
        if b <= 180:
            print(f"Minimum L2 ≈ {L2} mm → β = {b:.2f}°")
            break