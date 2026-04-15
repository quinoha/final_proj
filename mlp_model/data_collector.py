import cv2
import mediapipe as mp
import csv
import time

# ==================== initialize mediapipe ==================== 
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, )

CORE_JOINTS = []
    

def get_normalized_landmarks(landmarks):
    """
    Use main angle coordinates and
    """

    # set zero point
    left_hip = landmarks.landmark[23]
    

    #


# ============================ MAIN ============================