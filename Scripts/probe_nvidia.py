import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the new API key from your .env file
load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
API_KEY = os.getenv("NVIDIA_API_KEY")

if not API_KEY:
    print("ERROR: Could not find NVIDIA_API_KEY in the .env file.")
    exit()

print(f"Connecting to NVIDIA with key: {API_KEY[:10]}...")

# 2. Connect to NVIDIA's endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1", 
    api_key=API_KEY,
    timeout=20 # Stop trying if it takes longer than 20 seconds
)

# 3. Ask for the list of models
print("Fetching available models...\n")
try:
    models = client.models.list()
    
    print("SUCCESS! Here are the models you can access:")
    print("==========================================")
    
    # Sort them alphabetically so it's easier to read
    model_ids = sorted([model.id for model in models.data])
    
    for model_id in model_ids:
        print(f"- {model_id}")
        
    print("==========================================")
    print(f"Total models available: {len(model_ids)}")

except Exception as e:
    print("\nERROR: Could not connect to NVIDIA.")
    print(f"Details: {e}")