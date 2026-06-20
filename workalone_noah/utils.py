import numpy as np
import cv2

'''
======================== utility function file ========================
1. angles (three points)
2. balance angles (two points)
3. Drawing functions (cv2 library functions)
'''

# ============= angles calculation =============
# Calculate angle between three coordinates.
def calculate_angle(a, b, c):
    a = np.array(a) # 1st point
    b = np.array(b) # 2st point
    c = np.array(c) # 3st point

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if(angle > 180.0):
        angle = int(360 - angle)
    return angle

# Added Caculate balance angle between two points.
def calculate_balance(a, b):
    a = np.array(a)
    b = np.array(b)

    radians = np.arctan2(a[1]-b[1], a[0]-b[0]) - 0
    angle = np.abs(radians * 180.0 / np.pi)

    if(angle > 180.0):
        angle = int(360 - angle)

    return angle

'''
def calculate_angle_fpga(a, b, c):
    """
    Will be used for transceving angle data between Pi and FPGA.
    """

    return calculate_angle(a, b, c)
'''

def draw_status(image, cnt, stage, accuracy, curr_ex):
    """ 
    Used for drawing status according to current exercise

    """

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Status box
    cv2.rectangle(image, (0,0), (450,73), (245, 117, 16), -1)

    # Current workout action 
    cv2.putText(image, 'Session: ', (15, 20), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(curr_ex), (15, 60), font, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Rep data
    cv2.putText(image, 'REPS: ', (120, 20), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(cnt), (120, 60), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
    
    # Stage data
    cv2.putText(image, 'STAGE: ', (220, 20), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(stage), (220, 60), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
    
    # Accuracy data
    cv2.putText(image, 'Accuracy: ', (340, 20), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, f'{accuracy:1.2f}', (340, 60), font, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Angle data
    #cv2.putText(image, 'Angle', (15, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)