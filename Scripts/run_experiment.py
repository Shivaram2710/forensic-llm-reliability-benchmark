import os
import csv
import time
from openai import OpenAI
from dotenv import load_dotenv
from score_responses import GROUND_TRUTH, score_answer, analyze_errors

load_dotenv(r"C:\Users\Admin\Desktop\Forensic_LLM_Project\.env")
XKIRO_API_KEY = os.getenv("XKIRO_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") 
CROWLLM_API_KEY = os.getenv("CROWLLM_API_KEY")

PCAP_DIR = r"C:\Users\Admin\Desktop\Forensic_LLM_Project\PCAPs"
RESULTS_DIR = r"C:\Users\Admin\Desktop\Forensic_LLM_Project\Results"
os.makedirs(RESULTS_DIR, exist_ok=True)

SCENARIO_DETAILS = {
    "Scenario_1_Lucky_Turkey": {
        "background": "You are a SOC analyst for a Thanksgiving-themed gambling company. Alerts for NetSupport RAT triggered on 93.152.209.36:443. Environment: LAN 10.11.10.0/24, Domain: theluckyturkey.com, DC: 10.11.10.10.",
        "extra_q": "5. What is the date and start time of the NetSupport RAT traffic?"
    },
    "Scenario_2_Natureforce": {
        "background": "You are a SOC analyst. Alerts: A Windows EXE was sent from 107.175.82.242:9000, and CNCmachineRMS RAT C2 traffic was seen to 195.64.128.106:443. Environment: LAN 10.10.1.0/24, Domain: natureforce.com, DC: 10.10.1.10.",
        "extra_q": "5. What is the SHA-256 hash of the Windows EXE file sent from 107.175.82.242:9000?"
    },
    "Scenario_3_Kongtuke_Rebuke": {
        "background": "You are investigating Kongtuke ClickFix activity. Environment: LAN 10.9.11.0/24, Domain: overhands.org, DC: 10.9.11.2.",
        "extra_q": "5. What is the full name of the user from the user account?"
    },
    "Scenario_4_First_to_Last": {
        "background": "You are covering a SOC shift. Alerts for FormBook CnC Checkin triggered on multiple IPs. Environment: LAN 172.16.8.0/24, Domain: firsttolast.tech, DC: 172.16.8.8.",
        "extra_q": "5. What is the full name of the user from the user account?"
    },
    "Scenario_5_Easy_as_123": {
        "background": "You are a SOC analyst. Signature hits for NetSupport Manager RAT from 45.131.214.85 over TCP 443. Environment: LAN 10.2.28.0/24, Domain: easyas123.tech, DC: 10.2.28.2.",
        "extra_q": "5. What is the full name of the user from the user account?"
    },
    "Scenario_6_Lumma": {
        "background": "You are a SOC analyst. Signature hit for Lumma Stealer on traffic from 153.92.1.49 over TCP 80. Environment: LAN 10.1.21.0/24, Domain: win11office.com, DC: 10.1.21.2.",
        "extra_q": "5. What is the full name of the user from the user account?\n6. What is the domain from 153.92.1.49 that triggered the alert for Lumma Stealer?"
    }
}

MODELS = [
    {"provider": "xkiro", "id": "mistralai/mistral-large-2512"},
    {"provider": "xkiro", "id": "cohere/command-a-reasoning"},
    {"provider": "openrouter", "id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"},
    {"provider": "crowllm", "id": "glm-4.7-flash:free"},
    {"provider": "crowllm", "id": "gemini-3-flash:free"},
    {"provider": "crowllm", "id": "o4-mini:free"}
]

print("Starting FINAL experiment across 6 models and 6 scenarios (36 total tests)...\n")
results_data = []

for model in MODELS:
    provider = model["provider"]
    model_id = model["id"]
    
    print(f"==========================================")
    print(f"MODEL: {model_id} ({provider})")
    print(f"==========================================")
    
    if provider == "xkiro":
        client = OpenAI(base_url="https://api.xkiro.com/v1", api_key=XKIRO_API_KEY)
    elif provider == "crowllm":
        client = OpenAI(base_url="https://crowllm.com/v1", api_key=CROWLLM_API_KEY)
    elif provider == "openrouter":
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

    for scenario_name in GROUND_TRUTH.keys():
        print(f"  Analyzing {scenario_name}...", end="", flush=True)
        
        bg_info = SCENARIO_DETAILS[scenario_name]
        
        evidence_path = os.path.join(PCAP_DIR, f"{scenario_name}_Evidence.txt")
        with open(evidence_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            evidence = "".join(lines[:5000]) 

        prompt = f"""
        You are an expert Security Operations Center (SOC) analyst. 
        
        BACKGROUND CONTEXT:
        {bg_info['background']}
        
        Review the following extracted network traffic logs from the incident:
        {evidence}

        Based ONLY on the evidence above, answer the following questions:
        1. What is the IP address of the infected Windows client?
        2. What is the MAC address of the infected Windows client?
        3. What is the host name of the infected Windows client?
        4. What is the user account name from the infected Windows client?
        {bg_info['extra_q']}

        You MUST format your response exactly like this:
        [EVIDENCE EXTRACTION]
        (Quote the specific lines from the logs that contain the IP, MAC, Hostname, and Username).

        [REASONING]
        (Explain step-by-step how you connected the IP to the MAC, and the IP to the Username).

        [FINAL ANSWERS]
        ANSWER 1: [Your answer]
        ANSWER 2: [Your answer]
        ANSWER 3: [Your answer]
        ANSWER 4: [Your answer]
        (Add ANSWER 5 and ANSWER 6 if the background requested extra questions)
        """

        max_retries = 3
        success = False
        
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    timeout=90 
                )
                
                ai_answer = response.choices[0].message.content
                score, details = score_answer(scenario_name, ai_answer)
                error_type = analyze_errors(scenario_name, ai_answer, evidence_path)
                
                print(f" -> Score: {score} | Errors: {error_type}")
                
                results_data.append({
                    "Model": model_id,
                    "Scenario": scenario_name,
                    "Score": score,
                    "Error_Type": error_type,
                    "IP": details.get("ip", ""),
                    "MAC": details.get("mac", ""),
                    "Hostname": details.get("hostname", ""),
                    "User": details.get("user", ""),
                    "Full_Reasoning_Response": ai_answer.replace("\n", " | ") 
                })
                success = True
                break 
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "rate limit" in error_msg.lower():
                    print(f" [429 Limit. Waiting 20s...]", end="", flush=True)
                    time.sleep(20) 
                elif attempt == max_retries - 1:
                    print(f" -> ERROR: {error_msg[:50]}")
                    results_data.append({
                        "Model": model_id, "Scenario": scenario_name, "Score": "ERROR",
                        "Error_Type": "API Timeout / Error", "IP": "", "MAC": "", "Hostname": "", "User": "",
                        "Full_Reasoning_Response": error_msg
                    })
                else:
                    time.sleep(5)
        
        if provider in ["openrouter", "crowllm"]:
            time.sleep(10)

csv_path = os.path.join(RESULTS_DIR, "experiment_results.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Model", "Scenario", "Score", "Error_Type", "IP", "MAC", "Hostname", "User", "Full_Reasoning_Response"])
    writer.writeheader()
    writer.writerows(results_data)

print(f"\nFINAL experiment complete! Results saved to: {csv_path}")