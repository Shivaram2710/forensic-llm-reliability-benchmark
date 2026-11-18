import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup paths
RESULTS_DIR = r"C:\Users\Admin\Desktop\Forensic_LLM_Project\Results"
CHART_DIR = r"C:\Users\Admin\Desktop\Forensic_LLM_Project\Final_Charts"
os.makedirs(CHART_DIR, exist_ok=True)

csv_path = os.path.join(RESULTS_DIR, "experiment_results.csv")
df = pd.read_csv(csv_path)

# Clean up the data
df['Score'] = pd.to_numeric(df['Score'], errors='coerce').fillna(0)
model_order = df.groupby('Model')['Score'].sum().sort_values(ascending=False).index

print("Generating charts...")

# ==========================================
# FIGURE 1: Total Score by Model
# ==========================================
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Model', y='Score', estimator=sum, errorbar=None, order=model_order, hue='Model', palette="viridis", legend=False)
plt.title('Total Correct Answers by Model (Max 36)', fontsize=14, fontweight='bold')
plt.ylabel('Total Correct Answers', fontsize=12)
plt.xlabel('LLM Model', fontsize=12)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "Figure_1_Total_Score.png"), dpi=300, bbox_inches='tight')
plt.close()
print("[✓] Figure 1 saved.")

# ==========================================
# FIGURE 2: Heatmap (Model vs Scenario)
# ==========================================
plt.figure(figsize=(12, 6))
pivot = df.pivot(index='Model', columns='Scenario', values='Score').reindex(model_order)
sns.heatmap(pivot, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Score'}, linewidths=.5)
plt.title('LLM Performance by Scenario (0 = Total Failure)', fontsize=14, fontweight='bold')
plt.ylabel('LLM Model', fontsize=12)
plt.xlabel('Forensic Scenario', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "Figure_2_Scenario_Heatmap.png"), dpi=300, bbox_inches='tight')
plt.close()
print("[✓] Figure 2 saved.")

# ==========================================
# FIGURE 3: Error Distribution (FIXED FOR CLEAN LABELS)
# ==========================================
def categorize_error(err_str):
    if pd.isna(err_str) or err_str == 'None':
        return None
    categories = []
    # Group all hallucinations together
    if 'Hallucination' in err_str: 
        categories.append('Hallucination (Fake Evidence)')
    # Group all distractors together regardless of the specific IP
    if 'Distractor' in err_str: 
        categories.append('Distractor Susceptibility')
    # Group role confusion
    if 'Role Confusion' in err_str: 
        categories.append('Role Confusion')
    # Group API errors
    if 'API Timeout' in err_str or 'Error' in err_str: 
        categories.append('API Timeout / Error')
    return categories

# Apply the cleaning function to the Error_Type column
all_errors = df['Error_Type'].apply(categorize_error).explode()
error_counts = all_errors.dropna().value_counts()

plt.figure(figsize=(10, 6))
# Draw the bar chart
ax = sns.barplot(x=error_counts.values, y=error_counts.index, hue=error_counts.index, palette="magma", legend=False)

# Add the exact numbers to the end of each bar so the reader doesn't have to guess
for i, v in enumerate(error_counts.values):
    ax.text(v + 0.2, i, str(v), color='black', va='center', fontweight='bold')

plt.title('Distribution of Forensic Errors (Objective 2)', fontsize=14, fontweight='bold')
plt.xlabel('Frequency of Occurrence', fontsize=12)
plt.ylabel('Type of Error', fontsize=12)
plt.xlim(0, max(error_counts.values) + 2) # Add a little space for the numbers
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "Figure_3_Error_Distribution.png"), dpi=300, bbox_inches='tight')
plt.close()
print("[✓] Figure 3 saved with clean labels.")

print(f"\nAll charts saved to: {CHART_DIR}")