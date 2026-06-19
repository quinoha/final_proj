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
            if all(key in profile_data for key in ["gender", "height", "weight"]):
                print(f"User data loaded: {profile_data}")
                return profile_data
        except Exception as e:
            print(f"Error reading profile JSON: {e}. Corrupted file?")
    
    print("No valid user profile found: using Default profile")
    return default_profile

parsed_specs = get_user_specs(args.specs)

routine_map = {
    "curl": Curl,
    "squat": Squat,
    "plank": Plank,
    "pushup": Pushup
}

planner = WorkoutPlanner()

if args.routine:
    if args.routine.strip().lower() == "auto":
        print("Requesting AI for workout recommendation...")
        available_exercises = list(routine_map.keys())
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

