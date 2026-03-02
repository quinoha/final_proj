import numpy as np
import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self, complexity=1, detection_con=0.5):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(

        )
    
    def find_pose(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BAYER_BGGR2RGB)
        results = self.pose.process(img_rgb)
    
    def get_landmarks(self, results):
        lm_list = []
    

