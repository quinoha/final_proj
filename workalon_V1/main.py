import numpy as np
import cv2
import argparse
import time
from config import *
from detector import PoseDetector
from exercise import *
from workalon_V1.llm import WorkoutPlanner
import utils

'''
Main Code (Top module) for Workalone
--> Use Python argparse library to change and add workout routine.
--> One session can have at most five exercises along with short breaks.
--> AI gives feedback according to the user age, male/female, Height, Weight.  
--> Feedback: to-dos
'''

parser = argparse.ArgumentParser(description="WARKALON-V1: add your workout routine")
parser.add_argument('--routine', type=str, help='routines')
parser.add_argument('--specs', type=str, help='Male/Female, Height, Weight')
args = parser.parse_args()

detector = PoseDetector()
current_exercise = Curl()

# Video Capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Get image frame
    ret, frame = cap.read()

    # Model analyze landmark dictionary
    image, landmarks = detector.find_pose(frame)

    # begin workout routine
    if landmarks:
        # begin calculating time used in angle extraction
        start_time = time.perf_counter()

        angle = utils.calculate_angle(landmarks['left_shoulder'],
                                      landmarks['left_elbow'],
                                      landmarks['left_wrist'])
        
        count, stage = current_exercise.update(angle)

        end_time = time.perf_counter()
        latency_us = (end_time - start_time) * 1000000
        print(f"CPU calculation time: {latency_us:.2f} us")
    
        utils.draw_status(image, count, stage, angle, landmarks['left_elbow'])
        


    cv2.imshow('Workout Advisor', image)
    if cv2.waitKey(10) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
    
