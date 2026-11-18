# Forensic LLM Reliability Benchmark (2026 Network Traffic)

## Overview
This repository contains the code, dataset, and results for an MSc dissertation titled "Measuring the Forensic Reliability of Large Language Models." 

Unlike previous studies using synthetic data, this project utilizes real-world malware packet captures (PCAPs) from *Malware-Traffic-Analysis.net*. To prevent data contamination, a strict **Temporal Firewall** was applied: six reasoning-capable LLMs released between 2025 and early 2026 were tested, ensuring they could not have memorized the 2026 answers.

## Project Structure
*   `Scripts/` - The Python pipeline (Extraction, Querying, Scoring, Chart Generation).
*   `PCAPs/` - The extracted `.txt` network evidence logs (raw binary `.pcap` files are omitted to save space).
*   `Results/` - The raw CSV data showing the scores of all 36 tests.
*   `Final_Charts/` - Publication-ready visualizations (Bar chart, Heatmap, Error Distribution).

## The 5 Proposed Metrics
1. Baseline Accuracy
2. Hallucination Rate (fabricated evidence)
3. Role Confusion (Domain vs Hostname)
4. Distractor Susceptibility (accusing the Domain Controller)
5. Anchoring Bias (fixating on the first log entry)

## How to Reproduce
1. Install dependencies: `pip install openai python-dotenv pandas matplotlib seaborn`
2. Create a `.env` file with your API keys.
3. Run `python Scripts/extract_all_pcaps.py` to parse network logs.
4. Run `python Scripts/run_experiment.py` to query the LLMs.
5. Run `python Scripts/generate_charts.py` to generate the figures.