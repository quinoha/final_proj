import google.generativeai as genai
from config import * 
import os

"""
Use Gemini API for workout routine recommendation
prompt is as follows:

"""

genai.configure(api_key=GEMINI_API_KEY)

# 1. Choose model
model = genai.GenerativeModel('gemini-2.5-flash') # 혹은 최신 버전 사용
# 2. Prompt and response
response = model.generate_content("Recommend a workout routine for a 24 year-old male, 185cm, 80kg.")
# 3. Print response
print(response.text)