import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def ask_gemini(prompt="Hello from Gemini API!"):
    API_KEY = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    try:
        result = response.json()
        print("Response:\n", json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print("فشل في قراءة الاستجابة:", e)

if __name__ == "__main__":
    ask_gemini("اشرح كيف يعمل الذكاء الاصطناعي؟")
