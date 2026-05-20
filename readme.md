# Robotic Kinematics & Bit Utilities Workspace

A comprehensive workspace bridging low-level system utilities implemented in **C** with high-level robotic arm kinematics, workspace discretization, and transformation algorithms implemented in **Python**.

---

# 📁 Repository Structure

The project is systematically organized into four distinct functional modules:

```text
A/  -> Core execution runtime and low-level bit utility implementations
B/  -> Auxiliary calculation and supporting modules
C/  -> Robotics kinematics core engine
       (Grid generation, Frame transformations, and Singularity analysis)
D/  -> Evaluation suites and verification scripts
```

---

# 🛠️ Compilation and Execution

## Part A: Bit Utilities

To compile and run the low-level bit utilities locally using `gcc`, execute the following commands from your terminal:

```bash
gcc main.c bits_utils.c -o program
./program
```

---

# 🤖 Part C: Robotics Architecture & Theory

The core robotics module addresses **17 foundational problems**, divided into three primary architectural pillars.

---

# 1. Grid Generation & Workspace Discretization

## Workspace Discretization

Workspace discretization is the process of converting a robot's continuous operational environment into a finite set of point cells or topological graph structures.

This approach is fundamental for:

- Deterministic motion planning
- Real-time obstacle avoidance
- Reachability analysis
- Efficient path computation

---

## Physical Grid Representation

The physical workspace layout is represented using a structured **2D array** composed of rows and columns.

Each grid cell corresponds to a discrete reachable coordinate for the robotic manipulator.

---

## Grid Spacing (24 mm)

A fine spatial resolution of **24 mm** is used throughout the workspace.

This enables:

- Accurate end-effector positioning
- Stable coordinate indexing
- Consistent geometric transformations

---

## Negative Y Quadrant Mapping

The coordinate frame origin is centered such that the active operational workspace extends directly into the **negative \(Y\)** quadrant.

This mapping simplifies:

- Frame alignment
- Target generation
- Motion traversal logic

---

# 2. Coordinate Transformations

Understanding spatial frame transformations is essential for solving forward and inverse kinematics.

---

## Rotation About the Origin

A standard global transformation matrix is applied directly across the coordinate frame:

\[
R(\theta)=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
\]

This transformation rotates every coordinate about the global origin.

---

## Rotation About a Specific Joint

Rotating around an arbitrary joint requires a sequential three-step geometric transformation pipeline:

\[
\text{Translate to Origin}
\longrightarrow
\text{Rotate Frame}
\longrightarrow
\text{Translate Back to Joint}
\]

This method preserves the local joint reference frame while applying rotational motion.

---

# 3. Inverse Kinematics, Constraints, and Singularities

Inverse kinematics functions map desired end-effector target positions back into corresponding joint angle configurations.

These calculations are generally solved using:

- Geometric triangle laws
- Trigonometric relations
- Reachability constraints

---

# ⚠️ Robotic Singularity

A robotic singularity is a restricted physical configuration where the robotic arm loses one or more degrees of freedom (**DoF**).

At singularity points:

- Certain directional movements become impossible
- The Jacobian matrix becomes non-invertible
- Motion control becomes unstable

---

# ⚠️ Risks of Singularities

When approaching a singularity:

- The inverse kinematics solver may fail to determine a unique solution
- Joint velocities can spike toward infinity
- Physical instability or actuator locking may occur

These conditions can severely impact:

- Motion precision
- Controller stability
- Mechanical safety

---

# Core Singularity Types

## 1. Boundary Singularity

Occurs at the outer or inner structural limits of the robotic workspace.

Typical examples include:

- Fully extended arm configuration
- Fully retracted arm configuration

When fully extended, multiple joint configurations collapse into a single stretched geometry, causing the solver to lose uniqueness.

---

## 2. Elbow Singularity

An interior or boundary singularity occurring when the wrist center lies exactly on the geometric plane formed by:

- Joint 2 axis
- Joint 3 axis

This alignment reduces effective motion freedom.

---

# 🚨 Critical Operational Constraint

For Questions **16** and **17**:

\[
\beta > 180^\circ
\]

triggers an **absolute singularity constraint**.

Under this condition:

- The mathematical solver fails
- The robotic arm becomes kinematically invalid
- Motion computation may freeze or diverge

---

# Primary Kinematic Error Sources

When transitioning simulations into real-world hardware implementations, discrepancies commonly emerge from:

## Floating-Point Precision Errors

Complex trigonometric calculations introduce cumulative numerical inaccuracies.

---

## Mechanical Servo Backlash

Small gear gaps create positional offsets during directional changes.

---

## Structural Misalignment

Imperfect assembly alignment causes deviations between theoretical and physical coordinate frames.

---

# 📌 Technologies Used

## Low-Level Systems

- C
- GCC Compiler
- Bitwise Operations
- Memory-Level Utilities

## Robotics & Mathematical Modeling

- Python
- NumPy
- Matrix Transformations
- Kinematic Solvers
- Workspace Simulation

---

# 📚 Core Learning Domains

This workspace integrates concepts from:

- Robotics
- Embedded Systems
- Coordinate Geometry
- Numerical Computation
- System Programming
- Motion Planning
- Transform Mathematics
- Kinematic Analysis

---

# 🧠 Project Objective

The primary objective of this repository is to bridge:

- Low-level computational efficiency
- High-level robotic intelligence

by combining:

- Bit-level system utilities
- Spatial mathematics
- Workspace analysis
- Robotic motion computation

into a unified educational and experimental robotics framework.
