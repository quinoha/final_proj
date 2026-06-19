class Curl:
    def __init__(self, target_reps=15, user_specs=None):
        self.cnt = 0
        self.stage = None
        self.target_reps = target_reps
        self.user_specs = user_specs

    def update(self, angle):
        if angle > 160:
            self.stage = "down"
        if angle < 30 and self.stage == "down":
            self.stage = "up"
            self.cnt += 1
            print(self.cnt)

        return self.cnt, angle
 
    def accuracy (self, angle):
        if