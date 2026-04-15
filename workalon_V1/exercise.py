import numpy as np
import time
import utils

'''
Make OOP based exercise routines
=================== Available Exercise ===================
1. Curls
2. Squats
3. Plank
4. Push-ups
    .
    .
    .
to be updated. 

+ Accuracy feature:
Accuracy will be added based on the angles involved in the exercise routines.
Note that accuracy requires constant calculation throughout the exercise.

Penalty feature: Applying score based assessment
accuracy starts at 100.0, and is decremented when the user 

'''

# Left shoulder, elbow, wrist angle used
class Curl:
    def __init__(self, target_reps=15, user_specs=None):
        self.cnt = 0
        self.stage = None
        self.target_reps = target_reps
        self.user_specs = user_specs
        self.angle_history = []

    def update(self, landmarks):
        arm_angle = utils.calculate_angle(landmarks['left_shoulder'],
                                          landmarks['left_elbow'],
                                          landmarks['left_wrist'])

        back_angle = utils.calculate_angle(landmarks['left_shoulder'],
                                           landmarks['left_hip'],
                                           landmarks['left_knee'])

        if arm_angle > 160:
            self.stage = "down"
        if arm_angle < 30 and self.stage == "down":
            self.stage = "up"
            self.cnt += 1
            print(self.cnt)

        curl_accuracy = self.calculate_accuracy(arm_angle, back_angle)

        return self.cnt, self.stage, curl_accuracy
 
    def calculate_accuracy(self, arm_angle, back_angle):
        accuracy = 100.0

        back_penalty = abs(180-back_angle) * 0.5
        
        self.angle_history.append(arm_angle)
        if len(self.angle_history) > 10:
            self.angle_history.pop(0)

        shake_penalty = 0
        if len(self.angle_history) == 10:
            std_dev = np.std(self.angle_history)
            if std_dev > 5.0:
                shake_penalty = std_dev * 2.0

        return max(0, int(accuracy - back_penalty - shake_penalty))


# Squat class
class Squat:
    def __init__(self, target_reps=15, user_specs=None):
        self.cnt = 0
        self.stage = None
        self.target_reps = target_reps
        self.user_specs = user_specs

    def update(self, landmarks):
        """
        TODO: waist, knee, ankle angle squat logic
        """

        left_hip_vis = landmarks['left_hip'].visibility
        right_hip_vis = landmarks['right_hip'].visibility

        if left_hip_vis > right_hip_vis:
            active_hip = landmarks['left_hip']
            active_knee = landmarks['left_knee']
            active_ankle = landmarks['left_ankle']
        else:
            active_hip = landmarks['right_hip']
            active_knee = landmarks['right_knee']
            active_ankle = landmarks['right_ankle']


        leg_angle = utils.calculate_angle(active_hip, active_knee, active_ankle)
        shoulder_balance = utils.calculate_angle(landmarks['left_shoulder'],
                                               landmarks['right_shoulder'])
        
        # Squat counter logic (Counts up when up --> down, unnatural)
        '''
        if left_leg_angle > 100 and right_leg_angle > 100:
            self.stage = "up"
        if left_leg_angle < 90 and right_leg_angle < 90 and self.stage == "up":
            self.stage = "down"
            self.cnt +=1 
            print(f"Squat count: {self.cnt} / {self.target_reps}")
        '''

        # A better way for counting
        if leg_angle < 90:
            if self.stage == "up":
                self.stage = "down"
        
        if leg_angle > 160:
            if self.stage == "down":
                self.stage = "up"
                self.cnt += 1
                print(f"Squat count: {self.cnt} / {self.target_reps}")

        squat_accuracy = self.caculate_accuracy(shoulder_balance, leg_angle)

        return self.cnt, self.stage, squat_accuracy

    def caculate_accuracy(self, shoulder_balance, leg_angle):
        accuracy = 100.0

        upper_balance_penalty = abs(0 - shoulder_balance) * 0.5

        waist_balance_penalty = 0

        return max(0, int(accuracy - upper_balance_penalty - waist_balance_penalty))


# Plank class
class Plank:
    def __init__(self, target_time=60, user_specs=None):
        self.start_time = None    
        self.is_planking = False
        self.target_time = target_time
        self.elapsed_time = 0
    
    # Everything neutral: body angle used
    def update(self, landmarks, plank_time): 
        plank_time = time.time()

        left_hip_vis = landmarks['left_hip'].visibility
        right_hip_vis = landmarks['right_hip'].visibility

        # pick left or right as active side for better tracking
        if left_hip_vis > right_hip_vis:
            active_shoulder = landmarks['left_shoulder']
            active_hip = landmarks['left_hip']
            active_ankle = landmarks['left_ankle']
            print("current side: Left")

        else:
            active_shoulder = landmarks['right_shoulder']
            active_hip = landmarks['right_hip']
            active_ankle = landmarks['right_ankle']
            print("current side: Right")

        active_back_angle = utils.calculate_angle(active_shoulder, active_hip, active_ankle)
        active_arm_angle = utils.calculate_angle(act)

        plank_accuracy = self.calculate_accuracy(active_back_angle)

        return self.elapsed_time, plank_accuracy
    

    def calculate_accuracy(self, arm_angle, back_angle):
        accuracy = 100.0

        back_penalty = 0

        return max(0, accuracy - back_penalty) 


'''
TODO: Pushup routine
# Extension from plank
clas Pushup:
    def __init__(self, target_reps=20, user_specs=None):
        self.cnt = 0
        self.stage = None
        self.target_reps = target_reps

    def Pushups(angle, counter):
        x = 0
'''

