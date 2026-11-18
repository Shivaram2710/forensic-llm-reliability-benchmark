import os
import re

# ==========================================
# 1. THE GROUND TRUTH (From the PDF Answers)
# ==========================================
GROUND_TRUTH = {
    "Scenario_1_Lucky_Turkey": {
        "ip": "10.11.10.147", "mac": "00:12:f0:e5:17:43", "hostname": "DESKTOP-5OMVI3L", "user": "edward.winslow", "dc_ip": "10.11.10.10",
        "time": "18:22:07"
    },
    "Scenario_2_Natureforce": {
        "ip": "10.10.1.128", "mac": "00:22:fb:ec:7e:e7", "hostname": "DESKTOP-4VGYQX7", "user": "bdiaz", "dc_ip": "10.10.1.10",
        "hash": "b789adce70c028a6d17be45ec34667aa95586350ee0c4057e75b138b1ad35061"
    },
    "Scenario_3_Kongtuke_Rebuke": {
        "ip": "10.9.11.135", "mac": "08:d4:0c:7a:29:1e", "hostname": "DESKTOP-6T17ZFM", "user": "gmcdowell", "dc_ip": "10.9.11.2",
        "fullname": "Gabriel McDowell"
    },
    "Scenario_4_First_to_Last": {
        "ip": "172.16.8.49", "mac": "00:12:f0:28:d4:34", "hostname": "DESKTOP-5NLV63K", "user": "rvance", "dc_ip": "172.16.8.8",
        "fullname": "Ryamond Vance"
    },
    "Scenario_5_Easy_as_123": {
        "ip": "10.2.28.88", "mac": "00:19:d1:b2:4d:ad", "hostname": "DESKTOP-TEYQ2NR", "user": "brolf", "dc_ip": "10.2.28.2",
        "fullname": "Becka Rolf"
    },
    "Scenario_6_Lumma": {
        "ip": "10.1.28.58", "mac": "00:21:5d:c8:0e:f2", "hostname": "DESKTOP-ES9F3ML", "user": "gwyatt", "dc_ip": "10.1.21.2",
        "fullname": "Gabriel Wyatt", "domain": "whitepepper.su"
    }
}

# ==========================================
# 2. ACCURACY SCORER
# ==========================================
def score_answer(scenario_name, ai_response):
    truth = GROUND_TRUTH[scenario_name]
    
    # Only grade the text that comes AFTER [FINAL ANSWERS]
    if "[FINAL ANSWERS]" in ai_response:
        final_section = ai_response.split("[FINAL ANSWERS]")[-1].lower()
    else:
        final_section = ai_response.lower()
    
    score = 0
    results = {}
    
    # Core 4 Questions
    if truth["ip"].lower() in final_section: score += 1; results["ip"] = "Correct"
    else: results["ip"] = "Incorrect"
        
    if truth["mac"].lower() in final_section: score += 1; results["mac"] = "Correct"
    else: results["mac"] = "Incorrect"
        
    if truth["hostname"].lower() in final_section: score += 1; results["hostname"] = "Correct"
    else: results["hostname"] = "Incorrect"
        
    if truth["user"].lower() in final_section: score += 1; results["user"] = "Correct"
    else: results["user"] = "Incorrect"

    # Extra Questions (Dynamically checked based on the scenario)
    if "time" in truth:
        if truth["time"].lower() in final_section: score += 1; results["extra"] = "Correct"
        else: results["extra"] = "Incorrect"
        
    if "hash" in truth:
        if truth["hash"].lower() in final_section: score += 1; results["extra"] = "Correct"
        else: results["extra"] = "Incorrect"
        
    if "fullname" in truth:
        # We split the name to be forgiving if the AI gets the spelling slightly wrong
        first, last = truth["fullname"].split()
        if first.lower() in final_section and last.lower() in final_section: 
            score += 1; results["extra"] = "Correct"
        else: 
            results["extra"] = "Incorrect"
            
    if "domain" in truth:
        if truth["domain"].lower() in final_section: score += 1; results["extra"] = "Correct"
        else: results["extra"] = "Incorrect"
        
    return score, results

# ==========================================
# 3. ERROR ANALYSIS (Objective 2)
# ==========================================
def analyze_errors(scenario_name, ai_response, evidence_file_path):
    truth = GROUND_TRUTH[scenario_name]
    ai_lower = ai_response.lower()
    errors = []

    # 1. Role Confusion (Did it grab the Domain instead of the Desktop hostname?)
    if "desktop-" not in ai_lower:
        if any(domain in ai_lower for domain in ["overhands", "win11office", "natureforce", "theluckyturkey", "easyas123", "firsttolast"]):
            errors.append("Role Confusion (Extracted Domain instead of Hostname)")

    # 2. Distractor Susceptibility (Did it grab the Domain Controller IP?)
    if truth["dc_ip"].lower() in ai_lower and truth["dc_ip"].lower() != truth["ip"].lower():
        errors.append(f"Distractor (Identified DC {truth['dc_ip']} as victim)")

    # 3. Hallucination Check (Did it quote fake lines?)
    quoted_lines = re.findall(r'`([^`]+)`', ai_response)
    
    if os.path.exists(evidence_file_path) and quoted_lines:
        with open(evidence_file_path, "r", encoding="utf-8") as f:
            real_evidence = f.read()
        
        for quote in quoted_lines:
            clean_quote = quote.strip()
            if len(clean_quote) > 15 and clean_quote not in real_evidence:
                errors.append("Hallucination (Quoted fake evidence)")
                break 

    if not errors:
        return "None"
    
    return " | ".join(errors)

if __name__ == "__main__":
    print("Scoring module loaded successfully.")