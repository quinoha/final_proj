import numpy as np


# Caculate balance angle between two points.
def calculate_balance(a, b):
    a = np.array(a)
    b = np.array(b)

    radians = np.arctan2(a[1]-b[1], a[0]-b[0]) - 0.0
    angle = np.abs(radians * 180.0 / np.pi)

    if(angle > 180.0):
        angle = int(360 - angle)

    return angle

a = [10, 20]
b = [0, 10]


x = calculate_balance(a, b)
print(x)
