import numpy as np
import time

'''
=================== Exercise ===================
1. Curl Counter
2. Plank
3. Push-ups
    .
    .
    .
to be updated. 
'''

# Left shoulder, elbow, wrist angle used
def Curl(angle, counter):
    if angle > 160:
        stage = "down"
    if angle < 30 and stage == "down":
        stage = "up"
        counter += 1
        print(counter)
    
    return counter

# Everything neutral: body angle used
def Plank(angle, plank_time): 
    plank_time = time.time()
    #threshold = 
    #if angle < 


# Extension from plank
def Pushups(angle, counter):
    x = 0


