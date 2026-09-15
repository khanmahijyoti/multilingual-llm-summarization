import os
import json
import re
import time
import argparse
from tqdm import tqdm
import pandas as pd
from rouge_score import rouge_scorer
from groq import Groq, RateLimitError

class BengaliTokenizer:
    def tokenize(self, text):
        return re.findall(r'[\u0980-\u09FF\w]+', text)

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="bengali_test.jsonl")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--groq_api_keys", type=str, default=None, help="Comma-separated Groq API keys")
    parser.add_argument("--keys_file", type=str, default="api keys", help="Path to text file containing API keys line-by-line")
    parser.add_argument("--model", type=str, default="llama-3.3-70b-versatile")
    parser.add_argument("--output_csv", type=str, default="groq_llama70b_1000_results.csv")
    args = parser.parse_args()

    # Parse key pool from argument and/or keys file
    keys = []
    if args.groq_api_keys:
        keys.extend([k.strip() for k in args.groq_api_keys.split(",") if k.strip()])
    
    if os.path.exists(args.keys_file):
        with open(args.keys_file, "r", encoding="utf-8") as kf:
            for line in kf:
                key = line.strip()
                if key and not key.startswith("#") and key not in keys:
                    keys.append(key)

    if not keys:
        raise ValueError("No valid Groq API keys provided or found in keys_file.")
    
    current_key_idx = 0
    client = Groq(api_key=keys[current_key_idx], timeout=30.0, max_retries=3)
    print(f"[+] Loaded {len(keys)} Groq API key(s) in rotation pool.")

    with open(args.data_path, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for i, line in enumerate(f) if i < args.limit]

    print(f"[+] Loaded {len(dataset)} dataset items. Target model: '{args.model}'")

    # Resume logic: Load existing CSV if available
    existing_results = {}
    if os.path.exists(args.output_csv):
        try:
            df_old = pd.read_csv(args.output_csv)
            for _, row in df_old.iterrows():
                gen = str(row.get('generated', ''))
                if gen and gen != 'nan' and gen.strip():
                    existing_results[str(row['id'])] = {
                        'generated': gen,
                        'reference': str(row['reference']),
                        'rouge1': float(row['rouge1']),
                        'rouge2': float(row['rouge2']),
                        'rougeL': float(row['rougeL']),
                    }
            print(f"[+] Resuming from existing CSV: Found {len(existing_results)} already-completed summaries!")
        except Exception as e:
            print(f"[!] Warning reading existing CSV for resume: {e}")

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], tokenizer=BengaliTokenizer())
    
    results = []
    r1_list, r2_list, rl_list = [], [], []

    for item in tqdm(dataset):
        item_id = str(item.get("id", ""))
        ref_summary = item['summary']

        # Check if already completed
        if item_id in existing_results:
            saved = existing_results[item_id]
            gen_summary = saved['generated']
            r1 = saved['rouge1']
            r2 = saved['rouge2']
            rl = saved['rougeL']
        else:
            text = clean_text(item['text'])[:1500]
            prompt = f"নিচের বাংলা সংবাদ নিবন্ধটির একটি নির্ভুল ও সংক্ষিপ্ত সারসংক্ষেপ ৩ বাক্যে বাংলায় লিখুন:\n\n{text}\n\nসারসংক্ষেপ:"
            
            gen_summary = ""
            success = False

            # Try until success or all keys exhausted
            attempts = 0
            max_attempts = len(keys) * 3

            while not success and attempts < max_attempts:
                attempts += 1
                try:
                    completion = client.chat.completions.create(
                        model=args.model,
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

                    gen_summary = full_text.strip()
                    if gen_summary:
                        success = True
                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "rate_limit_exceeded" in err_msg:
                        print(f"\n[!] Key #{current_key_idx+1} hit Rate Limit (429). Rotating key...")
                        current_key_idx = (current_key_idx + 1) % len(keys)
                        client = Groq(api_key=keys[current_key_idx], timeout=30.0, max_retries=3)
                        if attempts % len(keys) == 0:
                            print("[!] All keys currently rate limited. Pausing 30 seconds for quota reset...")
                            time.sleep(30)
                        else:
                            time.sleep(1)
                    else:
                        print(f"\n[!] API Error on item {item_id}: {e}")
                        time.sleep(2)

            if not success:
                print(f"\n[!] Skipped item {item_id} after retries. Will resume later.")
                continue

            # Calculate ROUGE
            scores = scorer.score(ref_summary, gen_summary)
            r1 = scores['rouge1'].fmeasure * 100
            r2 = scores['rouge2'].fmeasure * 100
            rl = scores['rougeL'].fmeasure * 100

        r1_list.append(r1)
        r2_list.append(r2)
        rl_list.append(rl)

        results.append({
            "id": item_id,
            "reference": ref_summary,
            "generated": gen_summary,
            "rouge1": round(r1, 2),
            "rouge2": round(r2, 2),
            "rougeL": round(rl, 2),
        })

        # Save progress after each item
        df = pd.DataFrame(results)
        df.to_csv(args.output_csv, index=False, encoding="utf-8-sig")

    valid_count = len(r1_list)
    avg_r1 = sum(r1_list) / valid_count if valid_count else 0
    avg_r2 = sum(r2_list) / valid_count if valid_count else 0
    avg_rl = sum(rl_list) / valid_count if valid_count else 0

    # print("\n==================================================")
    # print(f"       Llama 3.3 70B Versatile ROUGE Results      ")
    # print("==================================================")
    # print(f"Valid Summaries Completed: {valid_count} / {len(dataset)}")
    # print(f"ROUGE-1 (F1 %): {avg_r1:.2f}%")
    # print(f"ROUGE-2 (F1 %): {avg_r2:.2f}%")
    # print(f"ROUGE-L (F1 %): {avg_rl:.2f}%")
    # print(f"[+] All detailed predictions saved to {args.output_csv}")

if __name__ == "__main__":
    main()
