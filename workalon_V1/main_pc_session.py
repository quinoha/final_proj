import numpy as np
import os
import json
import cv2
import argparse
import time
import utils


from detector import PoseDetector
from exercise import *
from profiler import PerfettoProfiler
from llm import WorkoutPlanner

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


How-to:
# First time using (make profile)
python main_pc_session.py --routine auto --specs "Gender, Height, weight"
python main_pc_session.py --routine auto --specs "Male, 180, 80"

# from second time, load profile
python main_pc_session.py --routine auto
'''

# Gemini API call
planner = WorkoutPlanner()

# Argparse for setting routines
parser = argparse.ArgumentParser(description="WARKALON-V1: add your workout routine")
parser.add_argument('--routine', type=str, help='routines')
parser.add_argument('--specs', type=str, help='Male/Female, Height, Weight')
args = parser.parse_args()

"""
function for getting user inputs as json file.
1. if input_specs ==> user inputs --specs male,185,80.
2. Load existing profile.
3. No input, no exisiting profile ==> set to default profile.
"""

PROFILE_FILE = "user_profile.json"
def get_user_specs(input_specs):
    default_profile = {"gender": "Unknown", "height": 185.0, "weight": 80.0}

    if input_specs:
        try:
            specs_list = [spec.strip() for spec in input_specs.split(',')]
            if len(specs_list) != 3:
                raise ValueError("Needs exactly 3 arguments (e.g. 'Male, 180, 80')")

            profile_data = {
                "gender": specs_list[0],
                "height": float(specs_list[1]),
                "weight": float(specs_list[2]),
            }

            # Save as josn file
            with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=4)
            print(f"New user profile generated: {profile_data}")
            return profile_data
        except Exception as e:
            print(f"Error parsing input specs: {e}. Falling back to saved or default profile.")
    
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Check if required keys exist
            if all(key in profile_data for key in ["gender", "height", "weight"]):
                print(f"User data loaded: {profile_data}")
                return profile_data
        except Exception as e:
            print(f"Error reading profile JSON: {e}. Corrupted file?")
    
    '''
    print("No user profile nor input: using Default profile")
    return {"gender": "Unknown", "height": 185.0, "weight": 80.0}
    '''
    
    print("No valid user profile found: using Default profile")
    return default_profile

parsed_specs = get_user_specs(args.specs)


# Routine class map
routine_map = {
    "curl": Curl,
    "squat": Squat,
    "plank": Plank,
    #"pushup": Pushup
}

if args.routine:
    if args.routine.strip().lower() == "auto":
        print("Requesting AI for workout recommendation...")
        available_exercises = list(routine_map.keys())
        # Call Gemini AI to get routine
        recommended = planner.get_recommendation(parsed_specs, available_exercises)
        print(f"AI Recommended Routine: {recommended}")
        
        routine_names = [name.strip().lower() for name in recommended.split(',')]
    else:
        routine_names = [name.strip().lower() for name in args.routine.split(',')]
else:
    routine_names = ["curl"]

session_queue = []

for name in routine_names:
    if name in routine_map:
        session_queue.append(routine_map[name](user_specs=parsed_specs))
    else:
        print(f"Unknown routine '{name}' skipped.")

if not session_queue:
    print("No executable routines. Default to curl")
    session_queue.append(Curl(user_specs=parsed_specs))

# Current index
curr_idx = 0

curr_exercise = session_queue[curr_idx]

# Manage break time between sessions
is_resting = False
rest_time = 0
break_duration = 20


# Initialize MediaPipe model detector
detector = PoseDetector()
# Video Capture
cap = cv2.VideoCapture(0)

# Instantiate Profiler object
profiler = PerfettoProfiler("cpu_baseline.json")
frame_count = 0
Max_Frames = 100
print("Starting profiling")

"""
==================== Main Loop ==================== 
"""
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

    # begin workout routine: check is_resting state.
    if landmarks:
        if is_resting:
            elapsed_rest = time.time() - rest_time
            if elapsed_rest >= break_duration:
                # Break over: move on to next routine
                is_resting = False
                curr_idx += 1
                if curr_idx < len(session_queue):
                    curr_exercise = session_queue[curr_idx]
                    print(f"Starting Next routine: {type(curr_exercise).__name__}")
                else:
                    # session over
                    print("Session ended. Great work!")
                    break
            else:
                # Breaktime: skip angle calculation
                cv2.putText(image, f"Rest: {int(break_duration-elapsed_rest)}s", 
                            (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)
                cv2.imshow('Workout Advisor', image)
                continue
                

        t3 = time.perf_counter_ns()

        # begin calculating time used in angle extraction
        start_time = time.perf_counter()
        count, stage, accuracy, is_done = curr_exercise.update(landmarks)
        
        t4 = time.perf_counter_ns()
        profiler.add_event("Calculate_Angle_CPU", "Logic", t3/1000, (t4-t3)/1000)

        end_time = time.perf_counter()
        latency_us = (end_time - start_time) * 1000000
        #print(f"CPU calculation time: {latency_us:.2f} us")
        
        # Pass to rest time
        if is_done:
            is_resting = True
            rest_time = time.time()
            print(f"{type(curr_exercise).__name__} completed! Taking a break.")

        # plot landmarks, reps, accuracy
        utils.draw_status(image, count, stage, accuracy, type(curr_exercise).__name__)
    

    cv2.imshow('Workout Advisor', image)
    frame_count += 1
    
    if cv2.waitKey(10) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

profiler.save()
