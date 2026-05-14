import os
from dotenv import load_dotenv
from google import genai

"""
Use Gemini API for workout routine recommendation
prompt is as follows:

"""

# Load api key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# 1. Choose model
model = genai.Client(api_key=gemini_api_key)


# 2. Prompt and response
prompt = '''[Output rules - Strict]

            ONLY use words in No need for any other explanation,
            ONLY lower-case english strings should be output. ex: curl, squat, pushup
            recommend a workout routine for male, 185cm, 80kg             
            '''

r = model.models.generate_content(model='gemini-2.5-flash', contents=prompt)

# 3. Print response
print(r)
