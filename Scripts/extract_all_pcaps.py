import subprocess
import os

# 1. Define the paths
TSHARK_PATH = r"C:\Program Files\Wireshark\tshark.exe"
PCAP_DIR = r"C:\Users\Admin\Desktop\Forensic_LLM_Project\PCAPs"

# 2. Map the dates to the Scenario names
scenarios = {
    "Scenario_1_Lucky_Turkey": "2026-11-10-traffic-analysis-exercise.pcap",
    "Scenario_2_Natureforce": "2026-10-01-traffic-analysis-exercise.pcap",
    "Scenario_3_Kongtuke_Rebuke": "2026-09-11-traffic-analysis-exercise.pcap",
    "Scenario_4_First_to_Last": "2026-08-09-traffic-analysis-exercise.pcap",
    "Scenario_5_Easy_as_123": "2026-02-28-traffic-analysis-exercise.pcap",
    "Scenario_6_Lumma": "2026-01-31-traffic-analysis-exercise.pcap"
}

print("Starting extraction of all PCAPs... This may take a few minutes depending on file sizes.\n")

for scenario_name, pcap_filename in scenarios.items():
    pcap_path = os.path.join(PCAP_DIR, pcap_filename)
    output_filename = f"{scenario_name}_Evidence.txt"
    output_path = os.path.join(PCAP_DIR, output_filename)

    print(f"Extracting: {scenario_name}...")

    # Check if the pcap file actually exists
    if not os.path.exists(pcap_path):
        print(f"  [!] ERROR: Could not find {pcap_filename} in the PCAPs folder. Skipping.")
        continue

    # Build the TShark command
    command = [
        TSHARK_PATH,
        "-r", pcap_path,
        "-Y", "nbns or kerberos or dhcp",
        "-T", "fields",
        "-e", "frame.number",
        "-e", "eth.src",
        "-e", "ip.src",
        "-e", "nbns.name",
        "-e", "kerberos.CNameString"
    ]

    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Save the output to the text file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            
        print(f"  [✓] Successfully saved: {output_filename}")
        
    except subprocess.CalledProcessError as e:
        print(f"  [!] Error extracting {scenario_name}: {e}")

print("\nAll extractions complete! Check your PCAPs folder.")