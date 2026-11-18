import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the API key
load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
XKIRO_API_KEY = os.getenv("XKIRO_API_KEY")

# 2. Absolute path to the evidence file
EVIDENCE_FILE = r"C:\Users\Admin\Desktop\Forensic_LLM_Project\PCAPs\Scenario_2_Natureforce_Evidence.txt"

# 3. Read the file and TRUNCATE it (only take the first 500 lines to prevent token limits)
with open(EVIDENCE_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()
    evidence = "".join(lines[:500])

prompt = f"""
You are a Security Operations Center (SOC) analyst. 
Review the following extracted network traffic logs:

{evidence}

Based ONLY on the evidence above, answer the following questions:
1. What is the IP address of the infected Windows client?
2. What is the MAC address of the infected Windows client?
3. What is the host name of the infected Windows client?
4. What is the user account name from the infected Windows client?

Format your answer strictly as:
ANSWER 1: [Your answer]
ANSWER 2: [Your answer]
ANSWER 3: [Your answer]
ANSWER 4: [Your answer]
"""

print("Sending query to xKiro (Cohere Command A Reasoning)... please wait.\n")

# 4. Connect to xKiro
client = OpenAI(base_url="https://api.xkiro.com/v1", api_key=XKIRO_API_KEY)

try:
    # We give it 60 seconds because reasoning models "think" before answering
    response = client.chat.completions.create(
        model="cohere/command-a-reasoning",
        messages=[
            {"role": "system", "content": "You are a forensic network analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        timeout=60 
    )
    
    print("--- LLM RESPONSE ---")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"An error occurred: {e}")