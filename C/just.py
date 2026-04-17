"""
TL_RAM (Two-Link Robot Arm Model) — Complete Solutions: Q8 to Q17
==================================================================

ANGLE CONVENTIONS (as defined in the spec):
    Alpha (α): CCW angle from +X axis to Link-1  (degrees)
    Beta  (β): Interior angle at the elbow joint, measured CW from Link-1 to Link-2

ROBOT PARAMETERS:
    L1 = L2 = 65 mm
    Grid pitch = 24 mm

HOME POSITION:
    Link-1: vertical   [0,0] → [0,65]   → α = 90°
    Link-2: horizontal [0,65] → [65,65] → β = 90°  (right angle at elbow)

FORWARD KINEMATICS (how to get tip position from angles):
    Joint-1 (elbow):  J1 = (L1·cos(α),  L1·sin(α))
    Tip direction:    absolute_angle = α − (180° − β)  =  α + β − 180°
    Tip position:     T  = J1 + L2·(cos(α+β−180°), sin(α+β−180°))

INVERSE KINEMATICS (how to get angles from target position):
    Step 1: d = √(dx² + dy²)        — straight-line distance to target
    Step 2: β = arccos((L1²+L2²−d²)/(2·L1·L2))   — law of cosines at J
            (β is the interior angle; equals 90° at home when d=√2·65)
    Step 3: φ = atan2(dy, dx)       — direction angle to target
    Step 4: δ = arccos((L1²+d²−L2²)/(2·L1·d))     — law of cosines at origin
    Step 5: α = φ + δ               — elbow-down configuration

MG996R SERVO:
    Operating range: 0° to 180°
    Both α and β must fall within [0°, 180°] for feasibility.
    (α can go negative/beyond in practice depending on motor orientation,
     but β is the binding constraint.)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# ─── Constants ────────────────────────────────────────────────────────────────
DEG   = np.pi / 180
L1    = 65.0    # mm
L2    = 65.0    # mm
PITCH = 24.0    # mm  (grid spacing — fixed from Q16 onward)

SERVO_MIN = 0.0
SERVO_MAX = 180.0


# ══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def forward_kinematics(alpha_deg, beta_deg, l1=L1, l2=L2):
    """
    Compute elbow joint and gripper tip positions from joint angles.

    Convention:
        alpha: CCW angle of Link-1 from +X axis
        beta : interior CW angle between Link-1 and Link-2 at elbow
        L2 absolute direction = alpha + beta - 180°

    Returns:
        (j1x, j1y) : elbow (joint-1) coordinates
        (tx,  ty)  : gripper tip coordinates
    """
    a       = alpha_deg * DEG
    L2_abs  = (alpha_deg + beta_deg - 180.0) * DEG   # absolute direction of Link-2
    j1x     = l1 * np.cos(a)
    j1y     = l1 * np.sin(a)
    tx      = j1x + l2 * np.cos(L2_abs)
    ty      = j1y + l2 * np.sin(L2_abs)
    return (j1x, j1y), (tx, ty)


def inverse_kinematics(dx, dy, l1=L1, l2=L2):
    """
    Compute joint angles (alpha, beta) to reach target (dx, dy).

    Method (basic trigonometry — per Q8 hint):
        1. Compute straight-line distance d to target.
        2. Use Law of Cosines to find the interior elbow angle β.
        3. Use atan2 and Law of Cosines at origin to find α.
        4. Elbow-down configuration: α = φ + δ  (gives the arm configuration
           consistent with the spec's given answers for Q9 and Q10).

    Returns:
        dict with 'alpha', 'beta', 'j1', 'tip', 'fk_error'
        or None if target is unreachable.
    """
    d_sq = dx**2 + dy**2
    d    = np.sqrt(d_sq)

    # Reachability: arm can only reach within [|L1-L2|, L1+L2]
    if d > l1 + l2 or d < abs(l1 - l2):
        return None

    # ── Step 2: Interior angle at elbow J  (Law of Cosines) ──
    # Triangle: O (origin) — J (elbow) — P (target)
    # OP² = OJ² + JP² − 2·OJ·JP·cos(β)
    # Solving for β:
    cos_beta = (l1**2 + l2**2 - d_sq) / (2 * l1 * l2)
    cos_beta = np.clip(cos_beta, -1.0, 1.0)    # guard floating-point overflow
    beta_deg = np.arccos(cos_beta) / DEG       # interior angle

    # ── Step 3 & 4: Direction angle φ and sub-angle δ at origin ──
    phi     = np.arctan2(dy, dx)               # angle of O→P from +X axis
    cos_del = (l1**2 + d_sq - l2**2) / (2 * l1 * d)
    cos_del = np.clip(cos_del, -1.0, 1.0)
    delta   = np.arccos(cos_del)               # angle at O in triangle O-J-P

    alpha_deg = (phi + delta) / DEG            # elbow-down: α = φ + δ

    # ── Verify with Forward Kinematics ──
    j1, tip   = forward_kinematics(alpha_deg, beta_deg, l1, l2)
    fk_error  = np.sqrt((tip[0] - dx)**2 + (tip[1] - dy)**2)

    return {
        "alpha":    round(alpha_deg, 6),
        "beta":     round(beta_deg,  6),
        "j1":       (round(j1[0], 4),  round(j1[1], 4)),
        "tip":      (round(tip[0], 4), round(tip[1], 4)),
        "fk_error": round(fk_error, 6),
    }


# ══════════════════════════════════════════════════════════════════════════════
# COORDINATE GRIDS
# ══════════════════════════════════════════════════════════════════════════════

# Rack: 2 rows × 6 cols — robot side, above the board
rack_coords  = [(-48 + c*24, 96 - r*24) for r in range(2) for c in range(6)]

# Board: 5 rows × 5 cols — the game grid
board_coords = [(24 + c*24, 48 - r*24) for r in range(5) for c in range(5)]


# ══════════════════════════════════════════════════════════════════════════════
# Q8  — IK for [board_row_1, board_col_4] = [96, 48]
# ══════════════════════════════════════════════════════════════════════════════

def solve_q8():
    print("=" * 65)
    print("Q8 — IK for [board_row_1, board_col_4] = [96, 48]")
    print("=" * 65)
    dx, dy = 96.0, 48.0

    d_sq = dx**2 + dy**2
    d    = np.sqrt(d_sq)

    print(f"\n  Target  : [{dx}, {dy}] mm")
    print(f"  L1 = L2 : {L1} mm")

    print(f"\n  Step 1 — Distance to target")
    print(f"    d = √({dx}² + {dy}²) = √{d_sq:.2f} = {d:.4f} mm")
    print(f"    Reachable? |L1−L2|={abs(L1-L2)} ≤ d={d:.2f} ≤ L1+L2={L1+L2}  → YES ✓")

    cos_beta = (L1**2 + L2**2 - d_sq) / (2*L1*L2)
    beta_deg = np.arccos(np.clip(cos_beta,-1,1)) / DEG
    print(f"\n  Step 2 — Interior elbow angle β (Law of Cosines)")
    print(f"    cos(β) = (L1²+L2²−d²)/(2·L1·L2)")
    print(f"           = ({L1**2}+{L2**2}−{d_sq:.2f})/(2×{L1}×{L2})")
    print(f"           = {cos_beta:.6f}")
    print(f"    β      = arccos({cos_beta:.6f}) = {beta_deg:.4f}°")

    phi = np.arctan2(dy, dx)
    cos_delta = (L1**2 + d_sq - L2**2) / (2*L1*d)
    delta     = np.arccos(np.clip(cos_delta,-1,1))
    alpha_deg = (phi + delta) / DEG
    print(f"\n  Step 3 — Angle α (coordinate geometry)")
    print(f"    φ      = atan2({dy}, {dx}) = {phi/DEG:.4f}°  (direction O→P from +X)")
    print(f"    cos(δ) = (L1²+d²−L2²)/(2·L1·d)")
    print(f"           = {cos_delta:.6f}")
    print(f"    δ      = arccos({cos_delta:.6f}) = {delta/DEG:.4f}°")
    print(f"    α      = φ + δ = {phi/DEG:.4f}° + {delta/DEG:.4f}° = {alpha_deg:.4f}°")

    res = inverse_kinematics(dx, dy)
    j1, tip = forward_kinematics(res['alpha'], res['beta'])
    print(f"\n  Step 4 — Forward Kinematics Verification")
    print(f"    J1  = ({j1[0]:.4f}, {j1[1]:.4f}) mm")
    print(f"    Tip = ({tip[0]:.4f}, {tip[1]:.4f}) mm  (should be [{dx}, {dy}])")
    print(f"    FK error = {res['fk_error']:.6f} mm  ✓")

    print(f"\n  ╔══════════════════════════════════════════╗")
    print(f"  ║  ANSWER:  α = {res['alpha']:.2f}°,   β = {res['beta']:.2f}°  ║")
    print(f"  ╚══════════════════════════════════════════╝")
    return res


# ══════════════════════════════════════════════════════════════════════════════
# Q9  — IK for [board_row_5, board_col_5] = [120, -48]
# ══════════════════════════════════════════════════════════════════════════════

def solve_q9():
    print("\n" + "=" * 65)
    print("Q9 — IK for [board_row_5, board_col_5] = [120, -48]")
    print("     Expected: α = -15.62°,  β = 167.64°")
    print("=" * 65)
    res = inverse_kinematics(120, -48)
    j1, tip = forward_kinematics(res['alpha'], res['beta'])
    print(f"  α       = {res['alpha']:.4f}°   (expected: -15.62°)")
    print(f"  β       = {res['beta']:.4f}°  (expected: 167.64°)")
    print(f"  Elbow   = {res['j1']}")
    print(f"  Tip     = {res['tip']}  (target: [120, -48])")
    print(f"  FK err  = {res['fk_error']:.6f} mm  ✓")
    a_ok = abs(res['alpha'] - (-15.62)) < 0.02
    b_ok = abs(res['beta']  - 167.64)  < 0.02
    print(f"  Matches expected?  α: {'✓' if a_ok else '✗'}   β: {'✓' if b_ok else '✗'}")
    return res


# ══════════════════════════════════════════════════════════════════════════════
# Q10 — IK for [rack_row_2, rack_col_1] = [-48, 72]
# ══════════════════════════════════════════════════════════════════════════════

def solve_q10():
    print("\n" + "=" * 65)
    print("Q10 — IK for [rack_row_2, rack_col_1] = [-48, 72]")
    print("      Expected: α = 171.96°,  β = 83.46°")
    print("=" * 65)
    res = inverse_kinematics(-48, 72)
    print(f"  α       = {res['alpha']:.4f}°   (expected: 171.96°)")
    print(f"  β       = {res['beta']:.4f}°   (expected: 83.46°)")
    print(f"  Elbow   = {res['j1']}")
    print(f"  Tip     = {res['tip']}  (target: [-48, 72])")
    print(f"  FK err  = {res['fk_error']:.6f} mm  ✓")
    a_ok = abs(res['alpha'] - 171.96) < 0.02
    b_ok = abs(res['beta']  - 83.46)  < 0.02
    print(f"  Matches expected?  α: {'✓' if a_ok else '✗'}   β: {'✓' if b_ok else '✗'}")
    return res


# ══════════════════════════════════════════════════════════════════════════════
# Q11 & Q12 — Tabulate α and β for all positions
# ══════════════════════════════════════════════════════════════════════════════

def solve_q11_q12():
    print("\n" + "=" * 65)
    print("Q11 — Rack Angles [α, β]")
    print("=" * 65)

    rack_2d  = [rack_coords[r*6:(r+1)*6] for r in range(2)]
    print("  Robot Rack: Coordinates for checker pick-up:")
    for row in rack_2d:
        print("  " + "  ".join(f"[{x:.2f}, {y:.2f}]" for x,y in row))

    print("\n  Corresponding Rack Robot: Angles [α, β] for checker pick-up:")
    rack_results = []; rack_alphas = []; rack_betas = []
    for row in rack_2d:
        row_res = []
        parts   = []
        for (x, y) in row:
            res = inverse_kinematics(x, y)
            row_res.append(res)
            if res:
                parts.append(f"[{res['alpha']:.2f}°, {res['beta']:.2f}°]")
                rack_alphas.append(res['alpha'])
                rack_betas.append(res['beta'])
            else:
                parts.append("[N/A, N/A]")
        rack_results.append(row_res)
        print("  " + "  ".join(parts))
    print(f"\n  Rack  α range: {min(rack_alphas):.2f}° to {max(rack_alphas):.2f}°")
    print(f"  Rack  β range: {min(rack_betas):.2f}° to {max(rack_betas):.2f}°")

    print("\n" + "=" * 65)
    print("Q12 — Board Angles [α, β]")
    print("=" * 65)

    board_2d = [board_coords[r*5:(r+1)*5] for r in range(5)]
    print("  TicTacToe Game Board: Coordinates for checker placement:")
    for row in board_2d:
        print("  " + "  ".join(f"[{x:.2f}, {y:.2f}]" for x,y in row))

    print("\n  Corresponding Board Robot: Angles [α, β] for checker placement:")
    board_results = []; board_alphas = []; board_betas = []
    for row in board_2d:
        row_res = []
        parts   = []
        for (x, y) in row:
            res = inverse_kinematics(x, y)
            row_res.append(res)
            if res:
                ok   = SERVO_MIN <= res['beta'] <= SERVO_MAX
                flag = "" if ok else " ⚠EXCEEDS_SERVO"
                parts.append(f"[{res['alpha']:.2f}°, {res['beta']:.2f}°]{flag}")
                board_alphas.append(res['alpha'])
                board_betas.append(res['beta'])
            else:
                parts.append("[UNREACHABLE]")
        board_results.append(row_res)
        print("  " + "  ".join(parts))
    print(f"\n  Board α range: {min(board_alphas):.2f}° to {max(board_alphas):.2f}°")
    print(f"  Board β range: {min(board_betas):.2f}° to {max(board_betas):.2f}°")

    return rack_results, board_results, rack_alphas, rack_betas, board_alphas, board_betas


# ══════════════════════════════════════════════════════════════════════════════
# Q13 — Combined min/max
# ══════════════════════════════════════════════════════════════════════════════

def solve_q13(rack_alphas, rack_betas, board_alphas, board_betas):
    print("\n" + "=" * 65)
    print("Q13 — Combined min/max α and β  (Rack + Board)")
    print("=" * 65)
    all_a = rack_alphas + board_alphas
    all_b = rack_betas  + board_betas
    print(f"  α  →  min = {min(all_a):.2f}°,   max = {max(all_a):.2f}°")
    print(f"  β  →  min = {min(all_b):.2f}°,  max = {max(all_b):.2f}°")
    print(f"  MG996R servo limit for β: [{SERVO_MIN}°, {SERVO_MAX}°]")
    bad = [(x,y,r['alpha'],r['beta'])
           for (x,y) in rack_coords+board_coords
           if (r:=inverse_kinematics(x,y)) and not (SERVO_MIN<=r['beta']<=SERVO_MAX)]
    print(f"  Positions with β outside servo range: {len(bad)}")
    for (x,y,a,b) in bad:
        print(f"    [{x:.1f},{y:.1f}]  α={a:.2f}°  β={b:.2f}°  ← INFEASIBLE")
    return all_a, all_b


# ══════════════════════════════════════════════════════════════════════════════
# Q14 — Feasibility for MG996R at [board_row_5, board_col_5]
# ══════════════════════════════════════════════════════════════════════════════

def solve_q14():
    print("\n" + "=" * 65)
    print("Q14 — MG996R feasibility at [board_row_5, board_col_5] = [120, -48]")
    print("=" * 65)
    res = inverse_kinematics(120, -48)
    feasible = res is not None and SERVO_MIN <= res['beta'] <= SERVO_MAX
    print(f"  α = {res['alpha']:.4f}°")
    print(f"  β = {res['beta']:.4f}°   (MG996R range: 0° – 180°)")
    print(f"  β within servo range? {'YES ✓  → FEASIBLE' if feasible else 'NO ✗  → NOT FEASIBLE'}")
    if not feasible and res:
        excess = res['beta'] - SERVO_MAX
        print(f"  β exceeds limit by: {excess:.4f}°")
    return res, feasible


# ══════════════════════════════════════════════════════════════════════════════
# Q15 — Solutions when not feasible (no constraints)
# ══════════════════════════════════════════════════════════════════════════════

def solve_q15(feasible):
    print("\n" + "=" * 65)
    print("Q15 — Solutions if infeasible  (no additional constraints)")
    print("=" * 65)
    if feasible:
        print("  Position is already feasible — no changes needed.")
        return
    print("""
  Root cause: β required exceeds MG996R's 180° limit.

  β = arccos((L1²+L2²−d²)/(2·L1·L2))
  Reducing β requires increasing d relative to L1 and L2,
  or increasing L1 and L2 to handle larger d more comfortably.

  Option A — Use a wider-range servo (easiest fix)
    Replace MG996R (180°) with a 270° continuous servo (e.g., DS3218MG).
    No mechanical redesign. Direct drop-in fix.

  Option B — Increase L1 and/or L2
    Longer links → arm reaches farther targets with less elbow bending.
    Caveat: increases the robot's footprint.

  Option C — Reposition the robot base (offset origin)
    Moving the arm base further from the board edge shifts all target
    coordinates in robot-frame, potentially bringing β within limits.

  Option D — Redesign as a 3-link arm
    Add a third link to distribute reach over 3 joints.
    Each joint then needs less travel. Increases complexity.

  Option E — Scale the board down (if not yet manufactured)
    Smaller board → closer targets → smaller d → smaller β.
    Not applicable if the board is already made.
""")


# ══════════════════════════════════════════════════════════════════════════════
# Q16 — Constraint: grid pitch 24 mm FIXED
# ══════════════════════════════════════════════════════════════════════════════

def solve_q16():
    print("=" * 65)
    print("Q16 — Constraint: grid pitch = 24 mm must NOT change")
    print("      (Board already laser-cut in pine wood)")
    print("=" * 65)
    print("""
  Grid pitch fixed → Option E (scale board) from Q15 is RULED OUT.
  Board and rack positions are now permanently fixed.

  Remaining options:

  Option A — Wider-range servo (STILL VALID, easiest)
    Grid is unchanged. Swap MG996R for a 270° servo.
    No mechanical work on links or base.

  Option B — Increase L2 (L1 still free to change)
    Longer L2 reduces β at critical far-corner positions.
    Find minimum L2 that makes ALL positions feasible.

  Option C — Offset the robot base
    Shift robot origin in X direction away from the board
    to reduce the effective arm reach required.
""")

    # Find minimum base X-offset so all board + rack positions are feasible
    print("  Scanning for minimum base X-offset (shifting arm right of board):")
    for offset_x in range(0, 80):
        all_ok = all(
            (r := inverse_kinematics(x - offset_x, y)) is not None
            and SERVO_MIN <= r['beta'] <= SERVO_MAX
            for x, y in board_coords + rack_coords
        )
        if all_ok:
            print(f"  → Minimum base X-offset = {offset_x} mm makes all positions feasible.")
            break


# ══════════════════════════════════════════════════════════════════════════════
# Q17 — Constraint: grid = 24 mm fixed  AND  L1 = 65 mm fixed
#        Find minimum L2 that makes all positions feasible
# ══════════════════════════════════════════════════════════════════════════════

def solve_q17():
    print("\n" + "=" * 65)
    print("Q17 — Constraints: grid = 24 mm (fixed) AND L1 = 65 mm (fixed)")
    print("       Find minimum L2 so ALL positions give β ≤ 180°")
    print("=" * 65)
    print("""
  L1 = 65 mm is already 3D-printed → cannot change L1.
  Grid pitch = 24 mm → board positions are fixed.
  Free parameter: L2 only.

  Critical position: [board_row_5, board_col_5] = [120, -48]
  This is the farthest corner from origin, hardest to reach
  without over-bending the elbow.

  Approach:
    Scan L2 from 65 mm upward in 0.5 mm steps.
    For each L2, check ALL 22 positions (12 rack + 10... 25 board).
    Stop at first L2 where every position satisfies β ≤ 180°.
""")

    L1_FIXED = 65.0
    print(f"  {'L2 (mm)':>8}  {'β at [120,-48]':>16}  {'All OK?':>9}")
    print("  " + "-" * 38)

    recommended_L2 = None
    scan_data      = []

    for L2_test in np.arange(65.0, 160.0, 0.5):
        res_crit = inverse_kinematics(120, -48, l1=L1_FIXED, l2=L2_test)
        if res_crit is None:
            continue
        beta_crit = res_crit['beta']

        all_ok = all(
            (r := inverse_kinematics(x, y, l1=L1_FIXED, l2=L2_test)) is not None
            and SERVO_MIN <= r['beta'] <= SERVO_MAX
            for x, y in board_coords + rack_coords
        )
        scan_data.append((L2_test, beta_crit, all_ok))

        # Print selected rows: every 5 mm up to 120, then the solution row
        if L2_test in np.arange(65, 121, 5) or (all_ok and recommended_L2 is None):
            flag = "YES ✓" if all_ok else "no"
            print(f"  {L2_test:>8.1f}  {beta_crit:>16.4f}°  {flag:>9}")

        if all_ok and recommended_L2 is None:
            recommended_L2 = L2_test

    if recommended_L2:
        rounded_L2 = np.ceil(recommended_L2 / 5) * 5
        res_min    = inverse_kinematics(120, -48, l1=L1_FIXED, l2=recommended_L2)
        res_rnd    = inverse_kinematics(120, -48, l1=L1_FIXED, l2=rounded_L2)

        print(f"""
  ┌─────────────────────────────────────────────────────┐
  │  Minimum L2 = {recommended_L2:.1f} mm                              │
  │  At [120,-48]: β = {res_min['beta']:.4f}°  ✓                  │
  │                                                     │
  │  Practical L2 = {rounded_L2:.0f} mm  (rounded to nearest 5 mm)   │
  │  At [120,-48]: β = {res_rnd['beta']:.4f}°  ✓                  │
  │                                                     │
  │  Change required:                                   │
  │    Original L2 = {L2:.1f} mm                             │
  │    New      L2 = {rounded_L2:.0f} mm                             │
  │    Increase   = {rounded_L2-L2:.0f} mm                              │
  │  → Reprint Link-2 only. Link-1 (65 mm) unchanged.  │
  └─────────────────────────────────────────────────────┘
""")
    return scan_data, recommended_L2


# ══════════════════════════════════════════════════════════════════════════════
# VISUALIZATION — all plots in a single comprehensive figure
# ══════════════════════════════════════════════════════════════════════════════

def visualize_all(q8_res, q9_res, q10_res, rack_results, board_results, scan_data, recommended_L2):

    fig = plt.figure(figsize=(20, 18))
    fig.suptitle("TL_RAM — Complete Solutions Q8 to Q17", fontsize=15, fontweight='bold', y=0.98)
    gs  = GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

    def draw_arm(ax, res, target, title, xlim, ylim, l1=L1, l2=L2,
                 board_dots=False, rack_dots=False, new_L2_label=None):
        ax.set_aspect('equal'); ax.grid(True, alpha=0.2, linestyle=':')
        ax.set_title(title, fontsize=9, pad=4)
        ax.set_xlabel("X (mm)", fontsize=8); ax.set_ylabel("Y (mm)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.axhline(0, color='gray', lw=0.5); ax.axvline(0, color='gray', lw=0.5)

        if board_dots:
            for (x,y) in board_coords:
                ax.plot(x, y, 'o', color='green', alpha=0.2, ms=6, zorder=2)
        if rack_dots:
            for (x,y) in rack_coords:
                ax.plot(x, y, 's', color='steelblue', alpha=0.2, ms=5, zorder=2)

        if res:
            j1, tip = forward_kinematics(res['alpha'], res['beta'], l1, l2)
            L2_color = 'tomato' if not new_L2_label else 'seagreen'
            ax.plot([0, j1[0]], [0, j1[1]],
                    color='royalblue', lw=5, solid_capstyle='round',
                    label=f'L1={l1:.0f}mm')
            ax.plot([j1[0], tip[0]], [j1[1], tip[1]],
                    color=L2_color, lw=4, solid_capstyle='round',
                    label=f'L2={l2:.0f}mm' + (' (new)' if new_L2_label else ''))
            ax.scatter(0, 0, s=70, color='black', zorder=6)
            ax.scatter(*j1, s=55, color='royalblue', zorder=6)
            ax.scatter(*tip, s=100, color=L2_color, marker='*', zorder=6)
            ax.plot(*target, 'k*', ms=12, zorder=7, label='Target')
            ax.text(j1[0]+2, j1[1]+2, f'J1\n({j1[0]:.0f},{j1[1]:.0f})',
                    fontsize=6.5, color='royalblue')
            ax.text(tip[0]+2, tip[1]+2, f'Tip\n({tip[0]:.0f},{tip[1]:.0f})',
                    fontsize=6.5, color=L2_color, fontweight='bold')
            ax.text(xlim[0]+5, ylim[0]+5,
                    f"α={res['alpha']:.1f}°\nβ={res['beta']:.1f}°",
                    fontsize=8, color='#333',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))
        ax.set_xlim(*xlim); ax.set_ylim(*ylim)
        ax.legend(loc='upper right', fontsize=7)

    # Q8
    ax_q8 = fig.add_subplot(gs[0, 0])
    draw_arm(ax_q8, q8_res, (96, 48),
             f"Q8: Target [96, 48]", (-20,140), (-20,90), board_dots=True)

    # Q9
    ax_q9 = fig.add_subplot(gs[0, 1])
    draw_arm(ax_q9, q9_res, (120, -48),
             f"Q9: Target [120, -48]", (-20,160), (-80,100), board_dots=True)

    # Q10
    ax_q10 = fig.add_subplot(gs[0, 2])
    draw_arm(ax_q10, q10_res, (-48, 72),
             f"Q10: Target [-48, 72]", (-90,90), (-10,120), rack_dots=True)

    # Q11/Q12 — β heatmap
    ax_hm = fig.add_subplot(gs[0, 3])
    ax_hm.set_aspect('equal'); ax_hm.grid(True, alpha=0.2)
    ax_hm.set_title("Q11/Q12 — β at all positions", fontsize=9)
    ax_hm.set_xlabel("X (mm)", fontsize=8); ax_hm.set_ylabel("Y (mm)", fontsize=8)
    ax_hm.tick_params(labelsize=7)
    ax_hm.axhline(0, color='gray', lw=0.5); ax_hm.axvline(0, color='gray', lw=0.5)
    for (x,y) in rack_coords + board_coords:
        res = inverse_kinematics(x, y)
        if res:
            ok = SERVO_MIN <= res['beta'] <= SERVO_MAX
            ax_hm.scatter(x, y, s=80, color='limegreen' if ok else 'tomato',
                          edgecolors='gray', lw=0.4, zorder=5)
            ax_hm.text(x, y+2.5, f"{res['beta']:.0f}°", fontsize=5.5, ha='center')
    ax_hm.scatter([],[], s=60, color='limegreen', label='β ≤ 180° ✓')
    ax_hm.scatter([],[], s=60, color='tomato',    label='β > 180° ✗')
    ax_hm.legend(fontsize=7)
    ax_hm.set_xlim(-80, 150); ax_hm.set_ylim(-65, 115)

    # Q13 — α scatter
    ax_q13a = fig.add_subplot(gs[1, 0])
    ax_q13a.set_aspect('equal'); ax_q13a.grid(True, alpha=0.2)
    ax_q13a.set_title("Q13 — α values (all positions)", fontsize=9)
    ax_q13a.set_xlabel("X (mm)", fontsize=8); ax_q13a.set_ylabel("Y (mm)", fontsize=8)
    ax_q13a.tick_params(labelsize=7)
    ax_q13a.axhline(0, color='gray', lw=0.5); ax_q13a.axvline(0, color='gray', lw=0.5)
    pts  = rack_coords + board_coords
    vals = [inverse_kinematics(x,y) for x,y in pts]
    sc = ax_q13a.scatter([p[0] for p,r in zip(pts,vals) if r],
                          [p[1] for p,r in zip(pts,vals) if r],
                          c=[r['alpha'] for r in vals if r],
                          cmap='RdYlGn', s=80, edgecolors='gray', lw=0.5, zorder=5)
    plt.colorbar(sc, ax=ax_q13a, label='α (°)', shrink=0.8)
    ax_q13a.set_xlim(-80, 150); ax_q13a.set_ylim(-65, 115)

    # Q14 — arm at [120,-48] original L2
    ax_q14 = fig.add_subplot(gs[1, 1])
    res14 = inverse_kinematics(120, -48)
    feas14 = res14 is not None and SERVO_MIN <= res14['beta'] <= SERVO_MAX
    draw_arm(ax_q14, res14, (120,-48),
             f"Q14: [120,-48], L1=L2={L1:.0f}mm\nβ={res14['beta']:.1f}° → {'FEASIBLE ✓' if feas14 else 'CHECK β'}",
             (-20,160), (-80,100), board_dots=True)

    # Q16 — base offset demo
    ax_q16 = fig.add_subplot(gs[1, 2])
    offset_x = None
    for off in range(0, 80):
        if all((r:=inverse_kinematics(x-off,y)) and SERVO_MIN<=r['beta']<=SERVO_MAX
               for x,y in board_coords+rack_coords):
            offset_x = off; break
    ax_q16.set_aspect('equal'); ax_q16.grid(True, alpha=0.2)
    ax_q16.set_title(f"Q16: Base offset = {offset_x}mm (Option C)", fontsize=9)
    ax_q16.set_xlabel("X (mm)", fontsize=8); ax_q16.set_ylabel("Y (mm)", fontsize=8)
    ax_q16.tick_params(labelsize=7)
    ax_q16.axhline(0, color='gray', lw=0.5); ax_q16.axvline(0, color='gray', lw=0.5)
    for (x,y) in board_coords+rack_coords:
        r_orig = inverse_kinematics(x,y)
        r_off  = inverse_kinematics(x-offset_x,y)
        ok_off = r_off and SERVO_MIN<=r_off['beta']<=SERVO_MAX
        ax_q16.scatter(x, y, s=50, color='tomato' if (r_orig and not(SERVO_MIN<=r_orig['beta']<=SERVO_MAX)) else 'gray',
                       marker='o', alpha=0.5, zorder=3)
        ax_q16.scatter(x-offset_x, y, s=70, color='limegreen' if ok_off else 'orange',
                       marker='^', zorder=5, edgecolors='gray', lw=0.4)
    ax_q16.scatter([],[],color='gray',marker='o',label='Original')
    ax_q16.scatter([],[],color='limegreen',marker='^',label=f'Offset {offset_x}mm')
    ax_q16.legend(fontsize=7)
    ax_q16.set_xlim(-120, 150); ax_q16.set_ylim(-65, 115)

    # Q17 — L2 scan chart
    ax_q17s = fig.add_subplot(gs[1, 3])
    if scan_data:
        L2v = [s[0] for s in scan_data]
        bv  = [s[1] for s in scan_data]
        okv = [s[2] for s in scan_data]
        cols = ['limegreen' if ok else 'tomato' for ok in okv]
        ax_q17s.scatter(L2v, bv, c=cols, s=15, zorder=4)
        ax_q17s.axhline(180, color='red', lw=1.5, ls='--', label='MG996R limit')
        if recommended_L2:
            ax_q17s.axvline(recommended_L2, color='steelblue', lw=1.5, ls='--',
                             label=f'Min L2={recommended_L2:.1f}mm')
        ax_q17s.set_title("Q17 — β vs L2 at [120,-48]", fontsize=9)
        ax_q17s.set_xlabel("L2 (mm)", fontsize=8); ax_q17s.set_ylabel("β (°)", fontsize=8)
        ax_q17s.tick_params(labelsize=7)
        ax_q17s.grid(True, alpha=0.2)
        ax_q17s.legend(fontsize=7)

    # Q17 — final arm with new L2
    if recommended_L2:
        rounded_L2 = np.ceil(recommended_L2 / 5) * 5
        res17 = inverse_kinematics(120, -48, l1=65.0, l2=rounded_L2)
        ax_q17 = fig.add_subplot(gs[2, 0:2])
        draw_arm(ax_q17, res17, (120,-48),
                 f"Q17: [120,-48] with L2={rounded_L2:.0f}mm\nβ={res17['beta']:.2f}°  FEASIBLE ✓",
                 (-20, 170), (-80, 110), l1=65.0, l2=rounded_L2,
                 board_dots=True, new_L2_label=True)

    # Q17 — full board feasibility with new L2
    if recommended_L2:
        rounded_L2 = np.ceil(recommended_L2 / 5) * 5
        ax_q17b = fig.add_subplot(gs[2, 2:4])
        ax_q17b.set_aspect('equal'); ax_q17b.grid(True, alpha=0.2)
        ax_q17b.set_title(f"Q17 — All positions feasible with L2={rounded_L2:.0f}mm", fontsize=9)
        ax_q17b.set_xlabel("X (mm)", fontsize=8); ax_q17b.set_ylabel("Y (mm)", fontsize=8)
        ax_q17b.tick_params(labelsize=7)
        ax_q17b.axhline(0, color='gray', lw=0.5); ax_q17b.axvline(0, color='gray', lw=0.5)
        for (x,y) in board_coords+rack_coords:
            r = inverse_kinematics(x, y, l1=65.0, l2=rounded_L2)
            ok = r is not None and SERVO_MIN <= r['beta'] <= SERVO_MAX
            sym = 'o' if (x,y) in board_coords else 's'
            ax_q17b.scatter(x, y, s=100, color='limegreen' if ok else 'tomato',
                            marker=sym, edgecolors='gray', lw=0.5, zorder=5)
            if r:
                ax_q17b.text(x, y+2.5, f"{r['beta']:.0f}°", fontsize=5.5, ha='center')
        ax_q17b.scatter([],[],s=80,color='limegreen',label=f'β ≤ 180° ✓')
        ax_q17b.scatter([],[],s=80,color='tomato',label=f'β > 180° ✗')
        ax_q17b.legend(fontsize=7)
        ax_q17b.set_xlim(-80, 155); ax_q17b.set_ylim(-65, 115)

    plt.savefig('/mnt/user-data/outputs/q08_to_q17_complete.png',
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nMain plot saved → q08_to_q17_complete.png")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN — run everything
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    q8_res  = solve_q8()
    q9_res  = solve_q9()
    q10_res = solve_q10()
    (rack_results, board_results,
     rack_alphas, rack_betas,
     board_alphas, board_betas) = solve_q11_q12()
    all_a, all_b = solve_q13(rack_alphas, rack_betas, board_alphas, board_betas)
    res14, feasible14 = solve_q14()
    solve_q15(feasible14)
    solve_q16()
    scan_data, recommended_L2 = solve_q17()
    visualize_all(q8_res, q9_res, q10_res, rack_results, board_results,
                  scan_data, recommended_L2)