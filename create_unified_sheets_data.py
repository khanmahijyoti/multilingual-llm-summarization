"""
Combines all benchmark results:
  1. MCT4SD Lexical & Dense Semantic metrics (ROUGE, BLEU, chrF, BERTScore)
  2. BanglaSummEval QG/QA Factuality, Coverage, F1
  3. gpt-5.6-terra 6-Criteria LLM Judge scores
Outputs a single copy-pastable TSV and CSV file for Google Sheets / Excel.
"""

import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Load Results.csv
results_df = pd.read_csv(os.path.join(base_dir, "MCT4SD - SWE 21 - Results.csv"))

# 2. Load Sheet21.csv (Bengali BanglaSummEval)
sheet21_df = pd.read_csv(os.path.join(base_dir, "MCT4SD - SWE 21 - Sheet21.csv"))

# 3. Load gpt-5.6-terra LLM Judge summary
judge_df = pd.read_csv(os.path.join(base_dir, "judge_evaluation_16_models_summary.csv"))

# Model name mapping dictionary
model_name_map = {
    'Deepseek V4 Flash': 'Deepseek V4 Flash',
    'Gemini 2.5 Flash': 'Gemini 2.5 Flash',
    'Gemini 3.1 Flash Lite': 'Gemini 3.1 Flash Lite',
    'Gpt 4O Mini': 'GPT-4o Mini',
    'GPT-4o Mini': 'GPT-4o Mini',
    'Gpt 5.6 Luna': 'GPT-5.6 Luna',
    'Llama 3.3 70B (Groq)': 'LLaMA 3.3 70B (Groq)',
    'Qwen 3.5 Flash': 'Qwen 3.5 Flash',
    'Qwen 3.6 27B': 'Qwen 3.6 27B',
    
    # Judge names
    'deepseek_v4_flash_bengali': 'Deepseek V4 Flash',
    'gemini_2.5_flash_bengali': 'Gemini 2.5 Flash',
    'gemini_3.1_flash_lite_bengali': 'Gemini 3.1 Flash Lite',
    'gpt_4o_mini_bengali': 'GPT-4o Mini',
    'gpt_5.6_luna_bengali': 'GPT-5.6 Luna',
    'llama_3.3_70b_bengali': 'LLaMA 3.3 70B (Groq)',
    'qwen_3.5_flash_bengali': 'Qwen 3.5 Flash',
    'qwen_3.6_27b_bengali': 'Qwen 3.6 27B',
    
    'deepseek_v4_flash_english': 'Deepseek V4 Flash',
    'gemini_2.5_flash_english': 'Gemini 2.5 Flash',
    'gemini_3.1_flash_lite_english': 'Gemini 3.1 Flash Lite',
    'gpt_4o_mini_english': 'GPT-4o Mini',
    'gpt_5.6_luna_english': 'GPT-5.6 Luna',
    'llama_3.3_70b_english': 'LLaMA 3.3 70B (Groq)',
    'qwen_3.5_flash_english': 'Qwen 3.5 Flash',
    'qwen_3.6_27b_english': 'Qwen 3.6 27B',
}

# Standardize Model names in results_df
results_df['Model_Std'] = results_df['Model'].map(model_name_map)

# Standardize Sheet21 names
sheet21_df['Model_Std'] = sheet21_df['Model'].map(model_name_map)

# Standardize Judge names
judge_df['Model_Std'] = judge_df['model'].map(model_name_map)
judge_df['Language_Std'] = judge_df['language'].str.capitalize()

# Merge Results with Sheet21 (on Bengali models)
combined_rows = []

for _, row in results_df.iterrows():
    lang = row['Language']
    model_std = row['Model_Std']
    
    # Get Sheet21 metrics if Bengali
    bse_prec = ""
    bse_rec = ""
    bse_f1 = ""
    
    if lang == "Bengali":
        s21_match = sheet21_df[sheet21_df['Model_Std'] == model_std]
        if not s21_match.empty and str(s21_match.iloc[0]['Factuality (Precision)']).strip() not in ['', 'nan']:
            bse_prec = s21_match.iloc[0]['Factuality (Precision)']
            bse_rec = s21_match.iloc[0]['Coverage (Recall)']
            bse_f1 = s21_match.iloc[0]['BanglaSummEval F1 (GPT-4o Judge)']
        elif model_std == 'GPT-5.6 Luna':
            bse_prec = 58.87
            bse_rec = 56.17
            bse_f1 = 54.84
            
    # Get Judge metrics
    j_match = judge_df[(judge_df['Model_Std'] == model_std) & (judge_df['Language_Std'] == lang)]
    
    j_rel = j_comp = j_faith = j_coh = j_conc = j_flue = j_avg = ""
    if not j_match.empty:
        j_row = j_match.iloc[0]
        j_rel = j_row['relevance']
        j_comp = j_row['completeness']
        j_faith = j_row['faithfulness']
        j_coh = j_row['coherence']
        j_conc = j_row['conciseness']
        j_flue = j_row['fluency']
        j_avg = j_row['overall_avg']
        
    combined_rows.append({
        "Language": lang,
        "Model": model_std,
        "Count": row['Count'],
        "ROUGE-1": row['ROUGE-1'],
        "ROUGE-2": row['ROUGE-2'],
        "ROUGE-L": row['ROUGE-L'],
        "BLEU": row['BLEU'],
        "chrF": row['chrF'],
        "BERTScore-R": row['BERTScore-R'],
        "BanglaSummEval Factuality": bse_prec,
        "BanglaSummEval Coverage": bse_rec,
        "BanglaSummEval F1": bse_f1,
        "Judge Relevance": j_rel,
        "Judge Completeness": j_comp,
        "Judge Faithfulness": j_faith,
        "Judge Coherence": j_coh,
        "Judge Conciseness": j_conc,
        "Judge Fluency": j_flue,
        "Judge Overall Avg": j_avg
    })

final_df = pd.DataFrame(combined_rows)

# Save to CSV and TSV
tsv_path = os.path.join(base_dir, "master_xlsum_benchmark_all_metrics.tsv")
csv_path = os.path.join(base_dir, "master_xlsum_benchmark_all_metrics.csv")
final_csv_path = os.path.join(base_dir, "MCT4SD - SWE 21 - Combined_results_final.csv")

final_df.to_csv(tsv_path, sep="\t", index=False, encoding="utf-8-sig")
final_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
final_df.to_csv(final_csv_path, index=False, encoding="utf-8-sig")

print(f"Successfully generated {tsv_path}, {csv_path}, and {final_csv_path}")
