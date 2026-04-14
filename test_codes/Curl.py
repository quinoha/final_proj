import numpy as np
import cv2
import mediapipe as mp
from functions import calculate_angle

'''
----------------- CURL COUNTER -----------------
Uses threshold values to count up arm curls.
Referred to online tutorial from: https://www.youtube.com/watch?v=06TE_U21FK4&t=642s 

'''

# counter variables
counter = 0
stage = None

# Use mediapie model to implement pose detection #
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

## setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # Video Feed
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # image (which is the frame) gets processed and is stored back in results
        results = pose.process(image)
        
        # Recoloring back to BGR format (opencv)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # print(results)
        
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        
            # Calculate Angles
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # Visualize
            cv2.putText(image, str(angle), 
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            # Curl Counter logic
            if angle > 160:
                stage = "down"
            if angle < 30 and stage == "down":
                stage = "up"
                counter += 1
                print(counter)

            print(landmarks)
        except:
            pass

        # Render curl counter
        # setup status box
        cv2.rectangle(image, (0,0), (255, 73), (245, 117, 16), -1)

        # Rep data
        cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        # Rep data
        cv2.putText(image, 'STAGE', (65, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (60, 60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Render landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(247,117,66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                  )
        
        
        cv2.imshow('Medapipe Feed', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

    