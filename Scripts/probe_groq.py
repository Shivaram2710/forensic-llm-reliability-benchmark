import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the API key
load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("ERROR: Could not find GROQ_API_KEY in the .env file. Check the spelling!")
    exit()

print(f"Connecting to Groq with key: {API_KEY[:10]}...\n")

# 2. Connect to Groq (It uses the exact same format as OpenAI)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key=API_KEY
)

# 3. Fetch models
print("Fetching available models...\n")
try:
    models = client.models.list()
    print("SUCCESS! Here are the models you can access on Groq:")
    print("==========================================")
    
    model_ids = sorted([model.id for model in models.data])
    for model_id in model_ids:
        print(f"- {model_id}")
        
    print("==========================================")
except Exception as e:
    print(f"\nERROR: {e}")