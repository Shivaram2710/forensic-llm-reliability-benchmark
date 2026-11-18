import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
API_KEY = os.getenv("XKIRO_API_KEY")

if not API_KEY:
    print("ERROR: Could not find XKIRO_API_KEY in the .env file.")
    exit()

# xKiro uses a different URL
client = OpenAI(base_url="https://api.xkiro.com/v1", api_key=API_KEY)

print("Sending tiny test to xKiro...")
try:
    response = client.chat.completions.create(
        model="cohere/command-a-reasoning",
        messages=[{"role": "user", "content": "Say exactly: xKiro is working!"}],
        timeout=15
    )
    print("SUCCESS:", response.choices[0].message.content)
except Exception as e:
    print(f"ERROR: {e}")