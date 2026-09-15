import sys
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
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'<think>.*$', '', text, flags=re.DOTALL)
    return text.strip()

def call_gemini_api(prompt, api_key, model="gemini-2.0-flash-lite", timeout=40):
    # Standard Google Gemini REST API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048
        }
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_json = json.loads(response.read().decode('utf-8'))
        candidates = res_json.get('candidates', [])
        if not candidates:
            return ""
        parts = candidates[0].get('content', {}).get('parts', [])
        if not parts:
            return ""
        text = parts[0].get('text', '')
        return strip_thinking_tags(text.strip())

def main():
    parser = argparse.ArgumentParser(description="Multi-Model Evaluator via Gemini API")
    parser.add_argument("--model", type=str, default="gemini-2.0-flash-lite", help="Gemini model ID (e.g. gemini-2.0-flash-lite, gemini-2.5-flash)")
    parser.add_argument("--data_path", type=str, required=True, help="Path to jsonl dataset file")
    parser.add_argument("--keys_file", type=str, default=r"E:\sounds\bengali_XLSum_v2.0\api keys", help="File containing API keys")
    parser.add_argument("--limit", type=int, default=1012, help="Number of items to evaluate")
    parser.add_argument("--output_csv", type=str, required=True, help="Output CSV file path")
    parser.add_argument("--lang", type=str, default="bengali", choices=["bengali", "english"], help="Language of dataset")
    args = parser.parse_args()

    # Load Gemini API keys (keys starting with AQ. or AIzaSy)
    gemini_keys = []
    if os.path.exists(args.keys_file):
        with open(args.keys_file, "r", encoding="utf-8") as kf:
            for line in kf:
                key = line.strip()
                if key and (key.startswith("AQ.") or key.startswith("AIzaSy")):
                    gemini_keys.append(key)

    if not gemini_keys:
        raise ValueError(f"No valid Gemini API keys found in {args.keys_file}")

    print(f"[+] Loaded {len(gemini_keys)} Gemini API key(s) in pool.")
    print(f"[+] Target Model: '{args.model}' | Language: {args.lang}")

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
            if args.lang == "bengali":
                prompt = f"নিচের বাংলা সংবাদ নিবন্ধটির একটি নির্ভুল ও সংক্ষিপ্ত সারসংক্ষেপ ৩ বাক্যে বাংলায় লিখুন:\n\n{text}\n\nসারসংক্ষেপ:"
            else:
                prompt = f"Summarize the following news article concisely in 3 sentences:\n\n{text}\n\nSummary:"

            gen_summary = ""
            success = False

            while not success:
                for k_idx in range(len(gemini_keys)):
                    actual_idx = (current_key_idx + k_idx) % len(gemini_keys)
                    k_key = gemini_keys[actual_idx]

                    try:
                        gen_summary = call_gemini_api(prompt, api_key=k_key, model=args.model)
                        if gen_summary:
                            success = True
                            current_key_idx = (current_key_idx + 1) % len(gemini_keys)
                            time.sleep(4)  # 4-second delay keeps request rate < 15 RPM free tier limit
                            break
                        else:
                            current_key_idx = (current_key_idx + 1) % len(gemini_keys)
                            time.sleep(2)
                    except urllib.error.HTTPError as e:
                        if e.code == 429:
                            current_key_idx = (current_key_idx + 1) % len(gemini_keys)
                            time.sleep(2)
                        else:
                            current_key_idx = (current_key_idx + 1) % len(gemini_keys)
                            time.sleep(3)
                    except Exception as e:
                        current_key_idx = (current_key_idx + 1) % len(gemini_keys)
                        time.sleep(3)

                if not success:
                    print(f"\n[!] Daily Gemini API Quota Limit Reached (429) across all {len(gemini_keys)} keys. Waiting 5 minutes for quota reset...", flush=True)
                    time.sleep(300)  # Wait 5 minutes before re-testing all keys

            scores = scorer.score(ref_summary, gen_summary)
            r1 = scores['rouge1'].fmeasure * 100
            r2 = scores['rouge2'].fmeasure * 100
            rl = scores['rougeL'].fmeasure * 100

            results.append({
                'id': item_id,
                'reference': ref_summary,
                'generated': gen_summary,
                'rouge1': round(r1, 2),
                'rouge2': round(r2, 2),
                'rougeL': round(rl, 2)
            })

            df = pd.DataFrame(results)
            df.to_csv(args.output_csv, index=False, encoding='utf-8-sig')

            print(f"[{i+1}/{len(dataset)}] ID: {item_id} | ROUGE-1: {r1:.2f}% | ROUGE-2: {r2:.2f}% | ROUGE-L: {rl:.2f}%", flush=True)

        r1_list.append(r1)
        r2_list.append(r2)
        rl_list.append(rl)

    valid_count = len(r1_list)
    avg_r1 = sum(r1_list) / valid_count if valid_count else 0
    avg_r2 = sum(r2_list) / valid_count if valid_count else 0
    avg_rl = sum(rl_list) / valid_count if valid_count else 0

    print("\n==================================================")
    print(f"  {args.model} ({args.lang.upper()}) Benchmark Results   ")
    print("==================================================")
    print(f"Valid Summaries Completed: {valid_count} / {len(dataset)}")
    print(f"ROUGE-1 (F1 %): {avg_r1:.2f}%")
    print(f"ROUGE-2 (F1 %): {avg_r2:.2f}%")
    print(f"ROUGE-L (F1 %): {avg_rl:.2f}%")
    print(f"[+] All predictions saved to {args.output_csv}")

if __name__ == "__main__":
    main()
