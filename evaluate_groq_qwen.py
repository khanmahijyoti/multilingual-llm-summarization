import sys
import os
import json
import time
import argparse
import pandas as pd
from tqdm import tqdm
import re
from rouge_score import rouge_scorer
from groq import Groq

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class BengaliTokenizer:
    def tokenize(self, text):
        return re.findall(r'[\u0980-\u09FF\w]+', text)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def strip_thinking_tags(text):
    if not text:
        return ""
    # Strip closed <think>...</think> blocks
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Strip unclosed <think>... blocks
    cleaned = re.sub(r'<think>.*$', '', cleaned, flags=re.DOTALL)
    return cleaned.strip()


def call_groq_qwen(prompt, api_key, model="qwen/qwen3.6-27b", timeout=30):
    client = Groq(api_key=api_key, timeout=timeout, max_retries=2)
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_completion_tokens=2048,
        top_p=1,
        stream=True
    )
    full_text = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        full_text += content
    return strip_thinking_tags(full_text)

def main():
    parser = argparse.ArgumentParser(description="Qwen 3.6 27B Evaluator via Groq Key Pool")
    parser.add_argument("--data_path", type=str, required=True, help="Path to jsonl dataset file")
    parser.add_argument("--keys_file", type=str, default=r"E:\sounds\bengali_XLSum_v2.0\api keys", help="File containing Groq API keys")
    parser.add_argument("--limit", type=int, default=1012, help="Number of items to evaluate")
    parser.add_argument("--output_csv", type=str, required=True, help="Output CSV file path")
    parser.add_argument("--lang", type=str, default="bengali", choices=["bengali", "english"], help="Language of dataset")
    args = parser.parse_args()

    # Load Groq keys
    groq_keys = []
    if os.path.exists(args.keys_file):
        with open(args.keys_file, "r", encoding="utf-8") as kf:
            for line in kf:
                key = line.strip()
                if key and key.startswith("gsk_"):
                    groq_keys.append(key)

    if not groq_keys:
        raise ValueError(f"No valid gsk_ Groq keys found in {args.keys_file}")

    print(f"[+] Loaded {len(groq_keys)} Groq API key(s) in rotation pool.")
    print(f"[+] Target Model: 'qwen/qwen3.6-27b' | Language: {args.lang}")

    with open(args.data_path, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for i, line in enumerate(f) if i < args.limit]

    print(f"[+] Loaded {len(dataset)} dataset items.")

    # Auto-Resume logic
    existing_results = {}
    results = []
    if os.path.exists(args.output_csv):
        try:
            df_old = pd.read_csv(args.output_csv)
            for _, row in df_old.iterrows():
                gen = str(row.get('generated', ''))
                if gen and gen != 'nan' and gen.strip():
                    item_dict = {
                        "id": str(row['id']),
                        "reference": str(row['reference']),
                        "generated": gen,
                        "rouge1": float(row['rouge1']),
                        "rouge2": float(row['rouge2']),
                        "rougeL": float(row['rougeL']),
                    }
                    existing_results[str(row['id'])] = item_dict
                    results.append(item_dict)
            print(f"[+] Resuming from existing CSV: Found {len(existing_results)} already-completed summaries!")
        except Exception as e:
            print(f"[!] Warning reading CSV: {e}")

    # ROUGE Scorer
    if args.lang == "bengali":
        bengali_tokenizer = BengaliTokenizer()
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], tokenizer=bengali_tokenizer)
    else:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    current_key_idx = 0
    r1_list, r2_list, rl_list = [], [], []

    for item in tqdm(dataset, desc=f"Evaluating Qwen 3.6 27B ({args.lang.upper()})"):
        item_id = str(item['id'])
        ref_summary = clean_text(item['summary'])

        if item_id in existing_results:
            saved = existing_results[item_id]
            gen_summary = saved['generated']
            r1 = saved['rouge1']
            r2 = saved['rouge2']
            rl = saved['rougeL']
        else:
            text = clean_text(item['text'])[:1500]
            if args.lang == "bengali":
                prompt = f"নিচের বাংলা সংবাদ নিবন্ধটির একটি নির্ভুল ও সংক্ষিপ্ত সারসংক্ষেপ ৩ বাক্যে বাংলায় লিখুন:\n\n{text}\n\nসারসংক্ষেপ:"
            else:
                prompt = f"Summarize the following news article concisely in 3 sentences:\n\n{text}\n\nSummary:"

            gen_summary = ""
            success = False
            attempts = 0
            max_attempts = 100

            while not success and attempts < max_attempts:
                attempts += 1
                k_key = groq_keys[current_key_idx]

                try:
                    gen_summary = call_groq_qwen(prompt, api_key=k_key)
                    if gen_summary:
                        success = True
                        current_key_idx = (current_key_idx + 1) % len(groq_keys)
                except Exception as e:
                    err_msg = str(e)
                    print(f"\n[!] Key #{current_key_idx+1} error: {err_msg[:100]}. Waiting & rotating key...")
                    current_key_idx = (current_key_idx + 1) % len(groq_keys)
                    time.sleep(3)

            if not success:
                print(f"\n[!] Skipped item {item_id} after retries.")
                continue


            scores = scorer.score(ref_summary, gen_summary)
            r1 = scores['rouge1'].fmeasure * 100
            r2 = scores['rouge2'].fmeasure * 100
            rl = scores['rougeL'].fmeasure * 100

            results.append({
                "id": item_id,
                "reference": ref_summary,
                "generated": gen_summary,
                "rouge1": round(r1, 2),
                "rouge2": round(r2, 2),
                "rougeL": round(rl, 2),
            })

            df_out = pd.DataFrame(results)
            df_out.to_csv(args.output_csv, index=False, encoding="utf-8-sig")

        r1_list.append(r1)
        r2_list.append(r2)
        rl_list.append(rl)

    valid_count = len(r1_list)
    avg_r1 = sum(r1_list) / valid_count if valid_count else 0
    avg_r2 = sum(r2_list) / valid_count if valid_count else 0
    avg_rl = sum(rl_list) / valid_count if valid_count else 0

    print("\n==================================================")
    print(f"  Qwen 3.6 27B ({args.lang.upper()}) Benchmark Results   ")
    print("==================================================")
    print(f"Valid Summaries Completed: {valid_count} / {len(dataset)}")
    print(f"ROUGE-1 (F1 %): {avg_r1:.2f}%")
    print(f"ROUGE-2 (F1 %): {avg_r2:.2f}%")
    print(f"ROUGE-L (F1 %): {avg_rl:.2f}%")
    print(f"[+] All predictions saved to {args.output_csv}")

if __name__ == "__main__":
    main()
