import numpy as np

'''
======================== utility function file ========================
1. angles
2. thresholds
3. color
4. detecting model

Referred to an online tutorial
https://www.youtube.com/watch?v=06TE_U21FK4 
'''

# function for calculating angle
def calc_angle(a, b, c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] -b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# def
