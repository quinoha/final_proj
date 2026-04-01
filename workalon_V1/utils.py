import numpy as np

'''
======================== utility function file ========================
1. angles
2. thresholds
3. color
4. detecting model
'''

# ============= angles calculation =============
def calculate_angle(a, b, c):
    a = np.array(a) # 1st point
    b = np.array(b) # 2st point
    c = np.array(c) # 3st point

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if(angle > 180.0):
        angle = 360 - angle
    return angle

def calculate_angle_fpga(a, b, c):
    """
    Will be used for transceving angle data between Pi and FPGA.
    """

    return calculate_angle(a, b, c)



