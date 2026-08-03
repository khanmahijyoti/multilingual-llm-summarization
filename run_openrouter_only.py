import os
import json
import time
import argparse
import urllib.request
import urllib.error
import pandas as pd
from tqdm import tqdm
import re
from rouge_score import rouge_scorer

# Custom Bengali Unicode Tokenizer for ROUGE Scorer
class BengaliTokenizer:
    def tokenize(self, text):
        return re.findall(r'[\u0980-\u09FF\w]+', text)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def call_openrouter_api(prompt, api_key, model="meta-llama/llama-3.3-70b-instruct", timeout=30):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "Bengali Dataset Summarization Evaluation"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2048,
        "top_p": 1
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_json = json.loads(response.read().decode('utf-8'))
        return res_json['choices'][0]['message']['content'].strip()

def main():
    parser = argparse.ArgumentParser(description="Evaluate Bengali News Summarization using OpenRouter Llama 3.3 70B")
    parser.add_argument("--data_path", type=str, default="bengali_test.jsonl", help="Path to Bengali XLSum test jsonl file")
    parser.add_argument("--keys_file", type=str, default="api keys", help="File containing OpenRouter API keys")
    parser.add_argument("--model", type=str, default="meta-llama/llama-3.3-70b-instruct", help="OpenRouter model identifier")
    parser.add_argument("--limit", type=int, default=1000, help="Maximum number of items to evaluate")
    parser.add_argument("--output_csv", type=str, default="groq_llama70b_1000_results.csv", help="CSV file to load/save predictions")
    args = parser.parse_args()

    # Parse OpenRouter keys (sk-or-v1-) from keys file
    keys = []
    if os.path.exists(args.keys_file):
        with open(args.keys_file, "r", encoding="utf-8") as kf:
            for line in kf:
                key = line.strip()
                if key.startswith("sk-or-v1-") and key not in keys:
                    keys.append(key)

    if not keys:
        raise ValueError("No valid OpenRouter API keys (sk-or-v1-...) found in keys_file.")
    
    current_key_idx = 0
    print(f"[+] Loaded {len(keys)} OpenRouter API key(s) in rotation pool.")

    with open(args.data_path, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for i, line in enumerate(f) if i < args.limit]

    print(f"[+] Loaded {len(dataset)} dataset items. Target model: '{args.model}'")

    # Resume logic: Load existing CSV if available
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
            print(f"[!] Warning: Could not read existing CSV: {e}")

    # Setup custom ROUGE scorer
    bengali_tokenizer = BengaliTokenizer()
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], tokenizer=bengali_tokenizer)

    r1_list, r2_list, rl_list = [], [], []

    for item in tqdm(dataset, desc=f"Evaluating {args.model}"):
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
            prompt = f"নিচের বাংলা সংবাদ নিবন্ধটির একটি নির্ভুল ও সংক্ষিপ্ত সারসংক্ষেপ ৩ বাক্যে বাংলায় লিখুন:\n\n{text}\n\nসারসংক্ষেপ:"
            
            gen_summary = ""
            success = False
            attempts = 0
            max_attempts = len(keys) * 3

            while not success and attempts < max_attempts:
                attempts += 1
                try:
                    gen_summary = call_openrouter_api(
                        prompt=prompt,
                        api_key=keys[current_key_idx],
                        model=args.model,
                        timeout=30
                    )
                    if gen_summary:
                        success = True
                except urllib.error.HTTPError as e:
                    err_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
                    if e.code in [429, 402] or "rate limit" in err_body.lower() or "credits" in err_body.lower():
                        print(f"\n[!] Key #{current_key_idx+1} hit rate limit / quota issue ({e.code}). Rotating key...")
                        current_key_idx = (current_key_idx + 1) % len(keys)
                        if attempts % len(keys) == 0:
                            print("[!] All keys currently rate limited. Pausing 15 seconds for quota reset...")
                            time.sleep(15)
                        else:
                            time.sleep(1)
                    else:
                        print(f"\n[!] HTTP Error {e.code} on item {item_id}: {err_body[:200]}")
                        time.sleep(2)
                except Exception as e:
                    print(f"\n[!] API Error on item {item_id}: {e}")
                    current_key_idx = (current_key_idx + 1) % len(keys)
                    time.sleep(2)

            if not success:
                print(f"\n[!] Skipped item {item_id} after retries. Will resume later.")
                continue

            # Calculate ROUGE
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

            # Save incremental progress
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
    print(f"   OpenRouter Llama 3.3 70B ROUGE Results        ")
    print("==================================================")
    print(f"Valid Summaries Completed: {valid_count} / {len(dataset)}")
    print(f"ROUGE-1 (F1 %): {avg_r1:.2f}%")
    print(f"ROUGE-2 (F1 %): {avg_r2:.2f}%")
    print(f"ROUGE-L (F1 %): {avg_rl:.2f}%")
    print(f"[+] All detailed predictions saved to {args.output_csv}")

if __name__ == "__main__":
    main()
