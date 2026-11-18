import os
from openai import OpenAI
from dotenv import load_dotenv

# Absolute path to your .env file
load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
API_KEY = os.getenv("NVIDIA_API_KEY")

if not API_KEY:
    print("ERROR: Could not find NVIDIA_API_KEY in the .env file.")
    exit()

client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=API_KEY)

print("Sending tiny test to NVIDIA...")
try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": "Say exactly: API is working!"}],
        timeout=15 # Stop trying after 15 seconds
    )
    print("SUCCESS:", response.choices[0].message.content)
except Exception as e:
    print(f"ERROR: {e}")