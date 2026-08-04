import os
import json
import pandas as pd
import argparse
from run_banglasummeval import run_pipeline, openrouter_keys, gemini_keys, openai_keys

def main():
    parser = argparse.ArgumentParser(description="Evaluate sample 0 across all 8 Bengali models using BanglaSummEval")
    parser.add_argument("--sample_index", type=int, default=0, help="Sample index to evaluate")
    parser.add_argument("--data_path", type=str, default="bengali_test.jsonl", help="Dataset path")
    parser.add_argument("--keys_file", type=str, default="api keys", help="API keys file")
    parser.add_argument("--key", type=str, default=None, help="Explicit API key")
    parser.add_argument("--model", type=str, default="gpt-5.6-luna", help="Frontier model to verify")
    parser.add_argument("--threshold", type=float, default=85.0, help="BERTScore Recall match threshold")
    args = parser.parse_args()

    # Load keys
    global openrouter_keys, gemini_keys, openai_keys
    provider = "gemini" if "gemini" in args.model.lower() else ("openai" if ("gpt-" in args.model.lower() or "luna" in args.model.lower()) else "openrouter")
    
    if args.key:
        if provider == "gemini":
            gemini_keys.extend([args.key])
        elif provider == "openai":
            openai_keys.extend([args.key])
        else:
            openrouter_keys.extend([args.key])
    else:
        if os.path.exists(args.keys_file):
            with open(args.keys_file, "r", encoding="utf-8") as kf:
                for line in kf:
                    key = line.strip()
                    if not key or key.startswith("#"):
                        continue
                    if key.startswith("sk-or-v1-"):
                        openrouter_keys.append(key)
                    elif key.startswith("AQ.") or key.startswith("AIzaSy"):
                        gemini_keys.append(key)
                    elif key.startswith("sk-proj-") or (key.startswith("sk-") and not key.startswith("sk-or-v1-")):
                        openai_keys.append(key)

    # Load dataset sample
    with open(args.data_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx == args.sample_index:
                sample = json.loads(line)
                break

    source_document = sample['text']
    sample_id = str(sample['id'])
    
    # List of 8 models to evaluate
    model_csvs = [
        ("Deepseek V4 Flash", "deepseek_v4_flash_bengali_results.csv"),
        ("Gemini 2.5 Flash", "gemini_2.5_flash_bengali_results.csv"),
        ("Gemini 3.1 Flash Lite", "gemini_3.1_flash_lite_bengali_results.csv"),
        ("Gpt 4O Mini", "gpt_4o_mini_bengali_results.csv"),
        ("Gpt 5.6 Luna", "gpt_5.6_luna_bengali_results.csv"),
        ("Llama 3.3 70B (Groq)", "groq_llama70b_1000_results.csv"),
        ("Qwen 3.5 Flash", "qwen_3.5_flash_bengali_results.csv"),
        ("Qwen 3.6 27B", "qwen_3.6_27b_bengali_results.csv"),
    ]

    results_table = []
    
    print(f"[+] Loaded Sample ID: {sample_id} for cross-model evaluation.")
    
    for model_name, csv_file in model_csvs:
        if not os.path.exists(csv_file):
            print(f"[!] Warning: CSV file {csv_file} not found. Skipping.")
            continue
            
        print(f"\nEvaluating Model: {model_name}")
        df = pd.read_csv(csv_file)
        matched_rows = df[df['id'].astype(str) == sample_id]
        if matched_rows.empty:
            print(f"[!] Warning: Could not find sample ID {sample_id} in {csv_file}. Skipping.")
            continue
            
        generated_summary = matched_rows.iloc[0]['generated']
        
        try:
            prec, rec, f1 = run_pipeline(source_document, generated_summary, args.model, provider, args.threshold)
            results_table.append({
                "Model": model_name,
                "Precision (Factuality)": f"{prec:.2f}%",
                "Recall (Coverage)": f"{rec:.2f}%",
                "BanglaSummEval F1": f"{f1:.2f}%"
            })
        except Exception as e:
            print(f"[!] Error evaluating {model_name}: {e}")
            results_table.append({
                "Model": model_name,
                "Precision (Factuality)": "Error",
                "Recall (Coverage)": "Error",
                "BanglaSummEval F1": "Error"
            })

    # Output final summary table
    print("\n\n" + "="*80)
    print(f"BanglaSummEval Cross-Model Benchmarks for Sample 0 ({sample_id})")
    print("="*80)
    df_res = pd.DataFrame(results_table)
    print(df_res.to_string(index=False))
    print("="*80)
    
    # Save to TSV
    df_res.to_csv("banglasummeval_sample0_comparison.tsv", sep="\t", index=False)
    print("[+] Saved comparison to banglasummeval_sample0_comparison.tsv")

if __name__ == "__main__":
    main()
