import numpy as np
import cv2
import argparse
import time
import utils
from config import *
from detector import PoseDetector
from exercise import *
from profiler import PerfettoProfiler
#from llm import 
#from workalon_V1.llm import WorkoutPlanner

'''
============== Main Code (Top module) for Workalon ==============
--> Use Python argparse library to change and add workout routine.
--> One session can have at most five exercises along with short breaks.
--> AI gives feedback according to the user age, male/female, Height, Weight.  
--> Feedback: to-dos

Note that the angle detection using vision models can be distorted according to the depth.
In other words, 
'''

# Gemini API call


# Argparse for setting routines
parser = argparse.ArgumentParser(description="WARKALON-V1: add your workout routine")
parser.add_argument('--routine', type=str, help='routines')
parser.add_argument('--specs', type=str, help='Male/Female, Height, Weight')
args = parser.parse_args()

detector = PoseDetector()
current_exercise = Curl()

# Video Capture
cap = cv2.VideoCapture(0)

# Instantiate Profiler object
profiler = PerfettoProfiler("cpu_baseline.json")
frame_count = 0
Max_Frames = 100
print("Starting profiling")

# Main Loop
while cap.isOpened():
    # Get image frame
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Waiting for camera frame...")
        continue

    t1 = time.perf_counter_ns()

    # Model analyze landmark dictionary
    image, landmarks = detector.find_pose(frame)

    t2 = time.perf_counter_ns()
    profiler.add_event("Mediapipe_Inference", "AI", t1/1000, (t2-t1)/1000)

    # begin workout routine
    if landmarks:
        t3 = time.perf_counter_ns()

        # begin calculating time used in angle extraction
        start_time = time.perf_counter()

        count, stage = current_exercise.update(landmarks)

        t4 = time.perf_counter_ns()
        profiler.add_event("Calculate_Angle_CPU", "Logic", t3/1000, (t4-t3)/1000)

        end_time = time.perf_counter()
        latency_us = (end_time - start_time) * 1000000
        print(f"CPU calculation time: {latency_us:.2f} us")
    
        # plot landmarks, reps, accuracy
        utils.draw_status(image, count, stage, accuracy, landmarks['left_elbow'])
    
    cv2.imshow('Workout Advisor', image)
    frame_count += 1
    
    if cv2.waitKey(10) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

profiler.save()
