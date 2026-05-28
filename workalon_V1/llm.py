import os
import json
import argparse
from dotenv import load_dotenv
from google import genai


"""
Use Gemini API for workout routine recommendation

    
"""

load_dotenv()
your_api_key = os.getenv("GEMINI_API_KEY")


class WorkoutPlanner:
    def __init__(self):
        self.client = genai.Client(api_key=your_api_key)

    def get_recommendation(self, user_specs, available_exercises):
        """
        Function for getting recommendation from Gemini
        """

        # read user profile .json file
        with open('user_profile.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(data)


        prompt = f"""
        
        [user specs]
        gender: {user_specs['gender']}
        height: {user_specs['height']}cm
        weight: {user_specs['weight']}kg

        [available exercise list]
        {', '.join(available_exercises)}

        [Output rules - Strict]
        Recommend a workout routine following the given [user specs] and [available routines].
        ONLY use words in the response.
        No need for any other explanation, ONLY lower-case english strings should be output.
        ex: curl, squat, pushup

        """

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        return response.text.strip().lower()


# test code
planner = WorkoutPlanner()
result = planner.get_recommendation()
