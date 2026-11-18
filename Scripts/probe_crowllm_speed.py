import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the API key
load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
API_KEY = os.getenv("CROWLLM_API_KEY")

if not API_KEY:
    print("ERROR: Could not find CROWLLM_API_KEY in the .env file.")
    exit()

client = OpenAI(base_url="https://crowllm.com/v1", api_key=API_KEY)

# 2. The 5 models we want to test
MODELS_TO_TEST = [
    "o3:free",
    "gemini-2.5-pro:free",
    "openai/gpt-oss-20b:free",
    "openai/gpt-oss-safeguard-20b:free",
    "gemini-3-pro:free"
]

print("Starting Speed Probe (Tokens/Second)...")
print("Prompt: 'Write a 150-word paragraph explaining the TCP 3-way handshake.'\n")
print("==========================================")

for model_id in MODELS_TO_TEST:
    print(f"Testing {model_id}...")
    
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "Write a 150-word paragraph explaining the TCP 3-way handshake."}],
            temperature=0.0,
            timeout=60
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Count words to estimate tokens (1 word ≈ 1.3 tokens)
        text = response.choices[0].message.content
        word_count = len(text.split())
        estimated_tokens = word_count * 1.3
        
        # Calculate speed
        speed = estimated_tokens / duration
        
        print(f"  [SUCCESS]")
        print(f"  Time taken: {duration:.2f} seconds")
        print(f"  Estimated tokens generated: {int(estimated_tokens)}")
        print(f"  Speed: {speed:.2f} tokens/second")
        print(f"  Preview: {text[:60]}...")
        
    except Exception as e:
        print(f"  [ERROR] {str(e)[:100]}")
    
    print("------------------------------------------")
    time.sleep(2) # Wait 2 seconds between models to avoid spamming

print("\nSpeed probe complete.")