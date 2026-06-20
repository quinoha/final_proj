import os
import numpy as np
import cv2
import argparse
import time
import utils
import json
#from config import *
from detector import PoseDetector
from exercise import *
from profiler import PerfettoProfiler
from picamera2 import Picamera2

#from llm import 
#from workalon_V1.llm import WorkoutPlanner

'''
============== Main Code (Top module) for Workalone ==============
--> Use Python argparse library to change and add workout routine.
--> One session can have at most five exercises along with short breaks.
--> AI gives feedback according to the user age, male/female, Height, Weight.  
--> Feedback: to-dos

Note that the angle detection using vision models can be distorted according to the depth.
In other words, 

============== BPM and sensor monitoring ==============
BPM monitoring via ESP32 and AFib sensor:
AFib sensor gets heartrate data from wrist, and is sent to Raspberry pi via BLE.
heartrate is monitore throughout the execute stage, and overall data is assessed afterwards.

--> BYTE sending



============== Personnel Tracking ==============


'''

# Gemini API call



# Argparse for setting routines
parser = argparse.ArgumentParser(description="WARKALON-V1: add your workout routine")
parser.add_argument('--routine', type=str, help='routines')
parser.add_argument('--specs', type=str, help='Male/Female, Height, Weight')
args = parser.parse_args()

PROFILE_FILE = "user_profile.json"

def get_user_specs(input_specs):
    # 1. Get input specs when user types --specs for the first time
    if input_specs:
        specs_list = []
        profile_data = {
            "gender": specs_list[0],
            "height": float(specs_list[1]),
            "weight": float(specs_list[2])
        }
    
        with open(PROFILE_FILE, 'w') as f:
            json.dump(profile_data, f, indent=4)
        print(f"User profile made: {profile_data}")
        return profile_data
    
    # 2. Load specs from existing json file
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            profile_data = json.load(f)
        print(f"Loading existing user data: {profile_data}")
        return profile_data
    
    # 3. No input, no saved json
    
    pass

parsed_specs = None
#
if args.specs:
    parsed_specs = [spec.strip]


# Routine dictionary
routine_map = {
    "curl": Curl,
    "squat": Squat,
    "plank": Plank,
    "push": Pushup
}

# if there are no routines, default is set as curl
routine_name = args.routine.lower() if args.routine else "curl"
exercise_class = routine_map.get(routine_name, Curl)

current_exercise = exercise_class(user_specs = parsed_specs)
detector = PoseDetector()

# cv2.VideoCapture does not work anymore
#cap = cv2.VideoCapture(1)
# Video Capture
picam2 = Picamera2()

config = picam2.create_preview_configuration(main={"size": (640,480), "format": "BGR888"})
picam2.configure(config)
picam2.start()


# Instantiate Profiler object
profiler = PerfettoProfiler("cpu_baseline.json")
frame_count = 0
Max_Frames = 100
print("Starting profiling")

# Main Loop
while True:
    try:

        frame = picam2.capture_array()
    except Exception as e:
        print(f"error while fetching camera frame: {e}")

    if frame is None:
        print("Waiting for camera frame...")
        continue
    
    '''
    # Get image frame
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Waiting for camera frame...")
        continue
    '''
    
    # Switch color from rgb to bgr (prevent smurf skin)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
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
        count, stage, accuracy = current_exercise.update(landmarks)
        
        t4 = time.perf_counter_ns()
        profiler.add_event("Calculate_Angle_CPU", "Logic", t3/1000, (t4-t3)/1000)

        end_time = time.perf_counter()
        latency_us = (end_time - start_time) * 1000000
        print(f"CPU calculation time: {latency_us:.2f} us")
    
        # plot landmarks, reps, accuracy
        utils.draw_status(image, count, stage, accuracy)
    
    cv2.imshow('Workout Advisor', image)
    frame_count += 1
    
    if cv2.waitKey(10) & 0xFF == ord('q'): \
        break

picam2.stop()

cv2.destroyAllWindows()

profiler.save()
