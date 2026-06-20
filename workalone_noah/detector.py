import numpy as np
import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self, mode=False, complexity=1, detection_con=0.5, tracking_con=0.5):
        """
        Initialize Mediapipe model.
        """
        
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

        # Parse the arguements and initialize the model
        self.pose = self.mp_pose.Pose(
            static_image_mode = mode,
            model_complexity = complexity,
            min_detection_confidence = detection_con,
            min_tracking_confidence = tracking_con
        )

        self.results = None
    
    def find_pose(self, img, draw=True):
        """
        Get the frame from the image and draw the landmarks, return image with landmarks.
        """

        # For raspberry-Pi
        #img_rgb = cv2.cvtColor(img, cv2.COLOR_BAYER_BGGR2RGB)
        # For webcam
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        img_rgb.flags.writeable = False
        self.results = self.pose.process(img_rgb)
        
        img_rgb.flags.writeable = True
        # Draw the landmarks if 'draw=True'
        if self.results.pose_landmarks and draw:
            self.mp_drawing.draw_landmarks(
                img,
                self.results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(247,117,66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(247,66,230), thickness=2, circle_radius=2)
            )
        
        lm_dict = self.get_landmarks()
        return img, lm_dict

    def get_landmarks(self):
        """
        Return a dictionary of extracted landmarks
        ex: lm_dict['left_shoulder'] = [x,y,z]
        """
        
        lm_list = {}
        if self.results and self.results.pose_landmarks:
            #
            for name in self.mp_pose.PoseLandmark:
                lm = self.results.pose_landmarks.landmark[name.value]

                key_name = name.name.lower()

                # 가시성(visibility) 데이터 추가
                lm_list[key_name] = [lm.x, lm.y, lm.z, lm.visibility]

        return lm_list
