import json
import argparse
import time
import os
import re
import pandas as pd
from rouge_score import rouge_scorer
import urllib.request
import urllib.error

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def strip_thinking_tags(text):
    if not text:
        return ""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'<\?xml.*?\?>', '', text, flags=re.DOTALL)
    return text.strip()

def get_bengali_scorer():
    class BengaliTokenizer:
        def tokenize(self, text):
            return re.findall(r'[\u0980-\u09FF\w]+', text)
    return rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], tokenizer=BengaliTokenizer())

def get_english_scorer():
    return rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

def load_openai_keys(keys_file):
    keys = []
    if os.path.exists(keys_file):
        with open(keys_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and (line.startswith('sk-proj-') or (line.startswith('sk-') and not line.startswith('sk-or-v1-'))):
                    keys.append(line)
    return keys

def call_openai_api(prompt, api_key, model="gpt-4o"):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['choices'][0]['message']['content']

def main():
    parser = argparse.ArgumentParser(description="Evaluate OpenAI models on XL-Sum dataset.")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model identifier")
    parser.add_argument("--keys_file", type=str, default=r"E:\sounds\bengali_XLSum_v2.0\api keys", help="Path to API keys file")
    parser.add_argument("--data_path", type=str, default="bengali_test.jsonl", help="Path to jsonl test file")
    parser.add_argument("--limit", type=int, default=1012, help="Number of samples to evaluate")
    parser.add_argument("--output_csv", type=str, default="gpt_4o_bengali_results.csv", help="Output CSV path")
    parser.add_argument("--lang", type=str, default="bengali", choices=["bengali", "english"], help="Language of dataset")
    args = parser.parse_args()

    openai_keys = load_openai_keys(args.keys_file)
    if not openai_keys:
        print("[!] No OpenAI API keys (sk-proj-...) found in keys file!")
        return

    print(f"[+] Loaded {len(openai_keys)} OpenAI API key(s).")
    print(f"[+] Target Model: '{args.model}' | Language: {args.lang}")

    data = []
    with open(args.data_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

    data = data[:args.limit]
    print(f"[+] Loaded {len(data)} dataset items.")

    scorer = get_bengali_scorer() if args.lang == "bengali" else get_english_scorer()

    results = []
    start_idx = 0
    if os.path.exists(args.output_csv):
        existing_df = pd.read_csv(args.output_csv)
        results = existing_df.to_dict('records')
        start_idx = len(results)
        print(f"[+] Resuming from existing CSV: Found {start_idx} already-completed summaries!")

    current_key_idx = 0

    for i in range(start_idx, len(data)):
        item = data[i]
        item_id = item.get('id', f'item-{i}')
        text = clean_text(item.get('text', ''))
        ref_summary = clean_text(item.get('summary', ''))

        if args.lang == "bengali":
            prompt = f"নিচের বাংলা সংবাদ নিবন্ধটির একটি নির্ভুল ও সংক্ষিপ্ত সারসংক্ষেপ ২-৩ বাক্যে লিখুন। অতিরিক্ত কোনো ভূমিকা বা মন্তব্য লিখবেন না:\n\nনিবন্ধ:\n{text}\n\nসারসংক্ষেপ:"
        else:
            prompt = f"Write a concise and accurate 2-3 sentence summary of the following news article. Do not include any intro or conversational filler:\n\nArticle:\n{text}\n\nSummary:"

        gen_summary = ""
        success = False

        while not success:
            for k_idx in range(len(openai_keys)):
                k_key = openai_keys[current_key_idx]

                try:
                    gen_summary = call_openai_api(prompt, api_key=k_key, model=args.model)
                    gen_summary = strip_thinking_tags(clean_text(gen_summary))
                    if gen_summary:
                        success = True
                        current_key_idx = (current_key_idx + 1) % len(openai_keys)
                        time.sleep(1)
                        break
                    else:
                        current_key_idx = (current_key_idx + 1) % len(openai_keys)
                        time.sleep(2)
                except urllib.error.HTTPError as e:
                    print(f"[!] OpenAI HTTP Error {e.code}: {e.reason}")
                    current_key_idx = (current_key_idx + 1) % len(openai_keys)
                    time.sleep(3)
                except Exception as e:
                    print(f"[!] Unexpected error: {e}")
                    current_key_idx = (current_key_idx + 1) % len(openai_keys)
                    time.sleep(3)

            if not success:
                print(f"\n[!] All OpenAI keys failed or rate-limited. Waiting 60 seconds...")
                time.sleep(60)

        scores = scorer.score(ref_summary, gen_summary)
        r1 = round(scores['rouge1'].fmeasure * 100, 2)
        r2 = round(scores['rouge2'].fmeasure * 100, 2)
        rl = round(scores['rougeL'].fmeasure * 100, 2)

        row = {
            'id': item_id,
            'reference': ref_summary,
            'generated': gen_summary,
            'rouge1': r1,
            'rouge2': r2,
            'rougeL': rl
        }
        results.append(row)

        df = pd.DataFrame(results)
        df.to_csv(args.output_csv, index=False, encoding='utf-8-sig')

        print(f"[{i+1}/{len(data)}] ID: {item_id} | R1: {r1}% | R2: {r2}% | RL: {rl}%")

    final_df = pd.DataFrame(results)
    print("\n" + "="*50)
    print(f"  {args.model} ({args.lang.upper()}) Benchmark Results")
    print("="*50)
    print(f"Valid Summaries Completed: {len(final_df)} / {len(data)}")
    print(f"ROUGE-1 (F1 %): {final_df['rouge1'].mean():.2f}%")
    print(f"ROUGE-2 (F1 %): {final_df['rouge2'].mean():.2f}%")
    print(f"ROUGE-L (F1 %): {final_df['rougeL'].mean():.2f}%")

if __name__ == "__main__":
    main()
