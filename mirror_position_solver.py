"""
A Script to calculate unknown coordinates of mirrors using trilateration.
Distances from 4 known points are used to solve sets of simultaneous equations.
Uses least squares reg. to solve as 4 distances to each mirror therefore overdetermined.
Sam Muddimer 10/11/23
"""
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Known target coordinates
T1 = np.array([0, 0, 0])
T2 = np.array([0.482, 0, 0.153])
T3 = np.array([0.967, 0, 0])
T4 = np.array([0.4835, 0.4566, 0])

# Measured distances
d_M2T1 = 1.9075
d_M2T2 = 1.9745
d_M2T3 = 2.1453
d_M2T4 = 1.5349

d_M3T1 = 1.9595
d_M3T2 = 1.9934
d_M3T3 = 2.1868
d_M3T4 = 1.5935

d_M4T1 = 2.1872
d_M4T2 = 1.9971
d_M4T3 = 1.9496
d_M4T4 = 1.5848

# Define distance equation
def distance(M, T, d):
    x, y, z = M
    xt, yt, zt = T
    return (x - xt)**2 + (y - yt)**2 + (z - zt)**2 - d**2

#mirror coordinate guesses
#Sensible starting guesses close to true values
#M2_guess = [0, 2, 0]
#M3_guess = [0, 2, 0.5]
#M4_guess = [1, 2, 0.4]

# not sensible
M2_guess = [0, 0, 0]
M3_guess = [0, 0, 0]
M4_guess = [0, 0, 0]

# Solve for Mirrors
def error(M_guess, d_T1, d_T2, d_T3, d_T4):
    return [
        distance(M_guess, T1, d_T1),
        distance(M_guess, T2, d_T2),
        distance(M_guess, T3, d_T3),
        distance(M_guess, T4, d_T4),
    ]

#Calculating mirror positions
M2 = least_squares(error, M2_guess, args=(d_M2T1, d_M2T2, d_M2T3, d_M2T4)).x
M3 = least_squares(error, M3_guess, args=(d_M3T1, d_M3T2, d_M3T3, d_M3T4)).x
M4 = least_squares(error, M4_guess, args=(d_M4T1, d_M4T2, d_M4T3, d_M4T4)).x

# output the solution coordinates
print("M2 Coordinates:", M2)
print("M3 Coordinates:", M3)
print("M4 Coordinates:", M4)

# Plotting the points and distances
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the target points & mirror points
ax.scatter(*T1, color='blue', label='T1')
ax.scatter(*T2, color='blue', label='T2')
ax.scatter(*T3, color='blue', label='T3')
ax.scatter(*T4, color='blue', label='T4')

ax.scatter(*M2, color='red', label='M2')
ax.scatter(*M3, color='green', label='M3')
ax.scatter(*M4, color='purple', label='M4')

# Functon to draw lines between points
def draw_line(p1, p2, color):
    x_values = [p1[0], p2[0]]
    y_values = [p1[1], p2[1]]
    z_values = [p1[2], p2[2]]
    ax.plot(x_values, y_values, z_values, color=color)

# Draw lines represnting distances

draw_line(M2, T1, 'red')
draw_line(M2, T2, 'red')
draw_line(M2, T3, 'red')
draw_line(M2, T4, 'red')

draw_line(M3, T1, 'green')
draw_line(M3, T2, 'green')
draw_line(M3, T3, 'green')
draw_line(M3, T4, 'green')

draw_line(M4, T1, 'purple')
draw_line(M4, T2, 'purple')
draw_line(M4, T3, 'purple')
draw_line(M4, T4, 'purple')

#labels and title
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')
ax.set_title('3D Plot of Mirrors and Targets with Distances')


ax.legend()
plt.show()