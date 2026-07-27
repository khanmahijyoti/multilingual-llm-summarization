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


def call_openrouter_api(prompt, api_key, model, timeout=35):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "LLM Benchmark Evaluation"
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
        choice = res_json['choices'][0]['message']['content']
        if choice is None:
            return ""
        return choice.strip()

def main():
    parser = argparse.ArgumentParser(description="Multi-Model Evaluator via OpenRouter")
    parser.add_argument("--model", type=str, required=True, help="OpenRouter model ID (e.g. qwen/qwen3.7-plus, deepseek/deepseek-v4-flash)")
    parser.add_argument("--data_path", type=str, required=True, help="Path to jsonl dataset file")
    parser.add_argument("--keys_file", type=str, default=r"E:\sounds\bengali_XLSum_v2.0\api keys", help="File containing OpenRouter API keys")
    parser.add_argument("--limit", type=int, default=1012, help="Number of items to evaluate")
    parser.add_argument("--output_csv", type=str, required=True, help="Output CSV file path")
    parser.add_argument("--lang", type=str, default="bengali", choices=["bengali", "english"], help="Language of dataset")
    args = parser.parse_args()

    # Load OpenRouter keys
    openrouter_keys = []
    if os.path.exists(args.keys_file):
        with open(args.keys_file, "r", encoding="utf-8") as kf:
            for line in kf:
                key = line.strip()
                if key and key.startswith("sk-or-v1-"):
                    openrouter_keys.append(key)

    if not openrouter_keys:
        raise ValueError(f"No valid sk-or-v1- OpenRouter keys found in {args.keys_file}")

    print(f"[+] Loaded {len(openrouter_keys)} OpenRouter API key(s) in rotation pool.")
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
                for k_idx, k_key in enumerate(openrouter_keys):
                    try:
                        raw_output = call_openrouter_api(prompt, api_key=k_key, model=args.model)
                        if raw_output:
                            gen_summary = strip_thinking_tags(raw_output)
                            if gen_summary:
                                success = True
                                current_key_idx = (k_idx + 1) % len(openrouter_keys)
                                break
                    except Exception as e:
                        err_msg = str(e)
                        if "402" in err_msg or "Payment Required" in err_msg:
                            continue
                        elif "429" in err_msg or "Rate limit" in err_msg:
                            time.sleep(2)
                            continue
                        else:
                            time.sleep(1)

                if not success:
                    print(f"\n[!] All OpenRouter keys currently return 402 Payment Required. Waiting 15 minutes for 24-hour quota reset...")
                    time.sleep(900)  # Wait 15 minutes before re-checking all keys


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
    print(f"  {args.model} ({args.lang.upper()}) Benchmark Results   ")
    print("==================================================")
    print(f"Valid Summaries Completed: {valid_count} / {len(dataset)}")
    print(f"ROUGE-1 (F1 %): {avg_r1:.2f}%")
    print(f"ROUGE-2 (F1 %): {avg_r2:.2f}%")
    print(f"ROUGE-L (F1 %): {avg_rl:.2f}%")
    print(f"[+] All predictions saved to {args.output_csv}")

if __name__ == "__main__":
    main()
