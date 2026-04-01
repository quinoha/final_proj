import google.generativeai as genai
from config import * 
import os

"""
Use Gemini API for workout routine recommendation
prompt is as follows:
    
"""

genai.configure(api_key=GEMINI_API_KEY)

# 2. 모델 설정
model = genai.GenerativeModel('gemini-2.5-flash') # 혹은 최신 버전 사용

# 3. 콘텐츠 생성 (오타 주의: generate_content)
response = model.generate_content("Recommend a workout routine for a 24 year-old male, 185cm, 80kg.")

# 4. 결과 출력
print(response.text)