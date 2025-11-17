import numpy as np
import cv2
import mediapipe as mp
import argparse

# Use mediapie model to implement pose detection #
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video Feed
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('Medapipe Feed', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()