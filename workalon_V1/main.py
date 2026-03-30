import numpy as np
import cv2
import argparse
from config import *
from detector import PoseDetector
from exercises import CurlCounter
import utils

'''
Main Code (Top module) for Workalone
--> Use Python argparse library to 
-->
-->
-->
'''



detector = PoseDetector()
current_exercise = CurlCounter()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    image, landmarks = detector.find_pose(frame)

    if landmarks:
        angle = utils.calculate_angle(landmarks['left_shoulder'],
                                      landmarks['left_elbow'],
                                      landmarks['left_wrist'])
        
        count, stage = current_exercise.update(angle)

        utils.draw_status(image, count, stage, angle, landmarks['left_elbow'])

    cv2.imshow('Workout Advisor'. image)
    if cv2.waitKey(10) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
    
