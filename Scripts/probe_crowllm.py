import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the API key
load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
API_KEY = os.getenv("CROWLLM_API_KEY")

if not API_KEY:
    print("ERROR: Could not find CROWLLM_API_KEY in the .env file. Check the spelling!")
    exit()

print(f"Connecting to CrowLLM with key: {API_KEY[:10]}...\n")

# 2. Connect to CrowLLM
client = OpenAI(
    base_url="https://crowllm.com/v1", 
    api_key=API_KEY
)

# 3. Try to fetch the models list
print("Fetching available models...\n")
try:
    models = client.models.list()
    print("SUCCESS! Here are the models you can access on CrowLLM:")
    print("==========================================")
    
    model_ids = sorted([model.id for model in models.data])
    for model_id in model_ids:
        print(f"- {model_id}")
        
    print("==========================================")
    
except Exception as e:
    print(f"Could not fetch model list automatically. Error: {e}")
    print("\nAttempting a direct test with the model from your documentation...")
    
    # Fallback test if the /models endpoint isn't supported
    try:
        response = client.chat.completions.create(
            model="crow-uncensored:free",
            messages=[{"role": "user", "content": "Say exactly: CrowLLM is working!"}],
            timeout=20
        )
        print(f"SUCCESS! The model 'crow-uncensored:free' works!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as test_e:
        print(f"Direct test failed as well: {test_e}")