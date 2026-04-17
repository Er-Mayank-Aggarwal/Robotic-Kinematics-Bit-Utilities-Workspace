In part A)

gcc main.c bits_utils.c -o program 

/program


In part C)
the 17 questions can be divided into 3 major parts 

Grid Generation -> array and coordinate sysem 

Transformations

Inverse Kinematics -> By triangle and reachability


on Grid Generation

'''
why 24 mm spacing? => to define discrete reachable points

2d array for physical grid formed of row and columns

negative qhy because coordinate fram at origin centered extend into negative y


Concept: workspace discretization.
process of converting robot's continous operational environment into finite point cells or graph...
-> for motion planning
-> obstacle avoidance
'''

on Tranformation

Difference between rotation about origin vs joint?
ABout origin -> direct transformation
about joint -> translate rotate translate back

WHat is singularity

A specific restricted configuration of a robotic arm where it looses its one or more deegree or freedom thus unable to move in certain directions

When a robot reaches singularity the joint speeds can become extremely hgih and cause instability

WHy study it ?? in q 16 and 17 if beta > 180 degree it will cause singularity.
When the arm is fully extended, the inverse kinematic algorithm (which calculates joint angles from a target position) cannot determine a unique solution.
Result: The arm becomes confused or stuck, as multiple or infinite combinations of joint angles could correspond to that single fully stretched position.

types
Boundary Singularity: Occurs at the edge of the robot's range, such as when the arm is fully extended or fully retracted.
Elbow Singularity: A type of interior or boundary singularity that happens when the wrist center lies on the plane formed by the joint 2 and joint 3 axes.



eror sources: 
floating point error
servo backlash
mechanical misalignment
Sources:

FOr inverse kinmatics:

[Click here to view mathematic visualization](https://www.alanzucconi.com/2018/05/02/ik-2d-1/)


