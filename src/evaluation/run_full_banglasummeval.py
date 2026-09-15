import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import torch
import pandas as pd
from bert_score import score

# Force UTF-8 on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Set up device and GPU lock
device = "cuda" if torch.cuda.is_available() else "cpu"
gpu_lock = threading.Lock()

# Global key pools and locks
openrouter_keys = []
gemini_keys = []
openai_keys = []
key_lock = threading.Lock()
current_key_idx = 0

def call_gemini_api(prompt, system_prompt, model, api_key, timeout=40):
    full_prompt = f"{system_prompt}\n\nContext/Input:\n{prompt}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 512
        }
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_json = json.loads(response.read().decode('utf-8'))
        if 'candidates' not in res_json or not res_json['candidates']:
            if 'error' in res_json:
                raise RuntimeError(f"Gemini API Error: {res_json['error']}")
            raise RuntimeError(f"Unexpected Gemini response structure: {res_json}")
        return res_json['candidates'][0]['content']['parts'][0]['text'].strip()

def call_openai_api(prompt, system_prompt, model, api_key, timeout=40):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    full_prompt = f"{system_prompt}\n\nContext/Input:\n{prompt}"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }
    
    if model.startswith("gpt-5") or model.startswith("o1") or model.startswith("o3") or "luna" in model.lower():
        payload["max_completion_tokens"] = 512
    else:
        payload["max_tokens"] = 512
        payload["temperature"] = 0.0
        
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_json = json.loads(response.read().decode('utf-8'))
        if 'choices' not in res_json:
            if 'error' in res_json:
                raise RuntimeError(f"OpenAI API Error: {res_json['error']['message']}")
            raise RuntimeError(f"Unexpected OpenAI response structure: {res_json}")
        return res_json['choices'][0]['message']['content'].strip()

def call_openrouter_api(prompt, system_prompt, model, api_key, timeout=40):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "BanglaSummEval Factual Consistency Pipeline"
    }
    
    full_prompt = f"{system_prompt}\n\nContext/Input:\n{prompt}"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 512,
        "top_p": 1
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_json = json.loads(response.read().decode('utf-8'))
        if 'choices' not in res_json:
            if 'error' in res_json:
                raise RuntimeError(f"OpenRouter API Error: {res_json['error']['message']}")
            raise RuntimeError(f"Unexpected OpenRouter response structure: {res_json}")
        return res_json['choices'][0]['message']['content'].strip()

def call_api_with_rotation(prompt, system_prompt, model, provider, timeout=40):
    global current_key_idx
    
    with key_lock:
        if provider == "gemini":
            pool = gemini_keys
        elif provider == "openai":
            pool = openai_keys
        else:
            pool = openrouter_keys
            
    if not pool:
        raise ValueError(f"No keys loaded for provider: {provider}")
        
    attempts = 0
    max_attempts = len(pool) * 2
    
    while attempts < max_attempts:
        with key_lock:
            api_key = pool[current_key_idx % len(pool)]
            
        try:
            # Spacing to respect rate limits
            time.sleep(0.1)
            if provider == "gemini":
                return call_gemini_api(prompt, system_prompt, model, api_key, timeout)
            elif provider == "openai":
                return call_openai_api(prompt, system_prompt, model, api_key, timeout)
            else:
                return call_openrouter_api(prompt, system_prompt, model, api_key, timeout)
        except urllib.error.HTTPError as e:
            with key_lock:
                print(f"[!] Key index {current_key_idx % len(pool)} failed (HTTP {e.code}). Rotating...")
                current_key_idx = (current_key_idx + 1) % len(pool)
            time.sleep(2 ** (attempts + 1))
        except Exception as e:
            with key_lock:
                print(f"[!] Key index {current_key_idx % len(pool)} failed (error: {e}). Rotating...")
                current_key_idx = (current_key_idx + 1) % len(pool)
            time.sleep(2)
        attempts += 1
        
    raise RuntimeError(f"All keys in the {provider} pool failed.")

def extract_entities_and_nouns(context, model, provider):
    system_prompt = (
        "You are a model that extracts named entities and nouns from texts provided in Bangla "
        "and provides them as an unnumbered list, separated by commas (no need to mention the total "
        "number of named entities and nouns). Return the output in Bangla language without any additional explanations."
    )
    prompt = f"Context: {context}"
    response = call_api_with_rotation(prompt, system_prompt, model, provider)
    candidates = [c.strip() for c in response.split(",") if c.strip() and len(c.strip()) > 1]
    seen = set()
    cleaned = []
    for c in candidates:
        if c.lower() not in seen:
            seen.add(c.lower())
            cleaned.append(c)
    return cleaned

def generate_question(context, answer, model, provider):
    system_prompt = (
        "Generate a short question based on the context and answer. The question must be such that "
        "when asked in the context, the response is the provided answer. Return the question in Bangla language "
        "without any additional explanations."
    )
    prompt = f"Context: {context}\nAnswer: {answer}"
    return call_api_with_rotation(prompt, system_prompt, model, provider)

def answer_question(context, question, model, provider):
    system_prompt = (
        "Answer the question based on the context and question. Provide only a short answer (one or two words) "
        "in Bangla language without any additional explanation."
    )
    prompt = f"Context: {context}\nQuestion: {question}"
    return call_api_with_rotation(prompt, system_prompt, model, provider)

def compute_bertscore_recall(predictions, references):
    if not predictions or not references:
        return []
    with gpu_lock:
        P, R, F1 = score(predictions, references, model_type="xlm-roberta-base", device=device, verbose=False)
        return [r.item() * 100 for r in R]

def run_pipeline(source_doc, target_text, model, provider, similarity_threshold=85.0):
    summary_entities = extract_entities_and_nouns(target_text, model, provider)
    
    prec_correct = 0
    prec_total = 0
    
    if summary_entities:
        questions_s = []
        for ans in summary_entities:
            q = generate_question(target_text, ans, model, provider)
            questions_s.append((ans, q))
            
        answers_d = []
        for ans, q in questions_s:
            pred_ans = answer_question(source_doc, q, model, provider)
            answers_d.append((ans, q, pred_ans))
            
        preds = [a[2] for a in answers_d]
        refs = [a[0] for a in answers_d]
        similarities = compute_bertscore_recall(preds, refs)
        
        for i, (ans, q, pred_ans) in enumerate(answers_d):
            sim = similarities[i]
            matched = sim >= similarity_threshold
            if matched:
                prec_correct += 1
            prec_total += 1
            
    precision_score = (prec_correct / prec_total * 100) if prec_total > 0 else 100.0
    
    source_snippet = source_doc[:1200]
    source_entities = extract_entities_and_nouns(source_snippet, model, provider)[:6]
    
    rec_correct = 0
    rec_total = 0
    
    if source_entities:
        questions_d = []
        for ans in source_entities:
            q = generate_question(source_snippet, ans, model, provider)
            questions_d.append((ans, q))
            
        answers_s = []
        for ans, q in questions_d:
            pred_ans = answer_question(target_text, q, model, provider)
            answers_s.append((ans, q, pred_ans))
            
        preds = [a[2] for a in answers_s]
        refs = [a[0] for a in answers_s]
        similarities = compute_bertscore_recall(preds, refs)
        
        for i, (ans, q, pred_ans) in enumerate(answers_s):
            sim = similarities[i]
            matched = sim >= similarity_threshold
            if matched:
                rec_correct += 1
            rec_total += 1
            
    recall_score = (rec_correct / rec_total * 100) if rec_total > 0 else 0.0
    f1_score = (2 * precision_score * recall_score) / (precision_score + recall_score) if (precision_score + recall_score) > 0 else 0.0
    
    return precision_score, recall_score, f1_score

def evaluate_single_sample(sample, df_preds, model, provider, threshold):
    sample_id = str(sample['id'])
    matched_rows = df_preds[df_preds['id'].astype(str) == sample_id]
    if matched_rows.empty:
        return None
        
    generated_summary = matched_rows.iloc[0]['generated']
    source_document = sample['text']
    
    try:
        prec, rec, f1 = run_pipeline(source_document, generated_summary, model, provider, threshold)
        return {
            "id": sample_id,
            "precision": prec,
            "recall": rec,
            "banglasummeval_f1": f1
        }
    except Exception as e:
        print(f"[-] Error on Sample ID {sample_id}: {e}")
        return None

def process_model(model_name, csv_file, dataset, model, provider, threshold, workers):
    # Differentiate output filenames by the judge model name (to keep Claude and GPT results separate!)
    judge_slug = model.split("/")[-1].replace("-", "_").lower()
    output_csv = f"banglasummeval_{judge_slug}_{csv_file.replace('_bengali_results.csv', '').replace('_results.csv', '')}_results.csv"
    
    results = []
    completed_ids = set()
    
    # Resume Logic
    if os.path.exists(output_csv):
        try:
            df_old = pd.read_csv(output_csv)
            for _, row in df_old.iterrows():
                completed_ids.add(str(row['id']))
                results.append(row.to_dict())
            print(f"[+] Model {model_name}: Resuming. {len(completed_ids)} completed.")
        except Exception:
            pass
            
    df_preds = pd.read_csv(csv_file)
    
    # Filter pending samples
    pending_samples = [s for s in dataset if str(s['id']) not in completed_ids]
    if not pending_samples:
        print(f"[+] Model {model_name} is already fully evaluated.")
        return
        
    print(f"[+] Evaluating {len(pending_samples)} samples for {model_name} using {workers} concurrent workers...")
    
    csv_write_lock = threading.Lock()
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(evaluate_single_sample, sample, df_preds, model, provider, threshold): sample for sample in pending_samples}
        
        count = 0
        for future in as_completed(futures):
            res = future.result()
            if res:
                with csv_write_lock:
                    results.append(res)
                    pd.DataFrame(results).to_csv(output_csv, index=False)
                count += 1
                if count % 10 == 0:
                    print(f"    -> Progress [{model_name}]: {count}/{len(pending_samples)} completed.")

def main():
    global openrouter_keys, gemini_keys, openai_keys
    parser = argparse.ArgumentParser(description="Run full BanglaSummEval benchmarks concurrently")
    parser.add_argument("--keys_file", type=str, default="api keys", help="File containing API keys")
    parser.add_argument("--key", type=str, default=None, help="Specific API key")
    parser.add_argument("--model", type=str, default="gpt-4o", help="Judge model")
    parser.add_argument("--threshold", type=float, default=85.0, help="Semantic match threshold")
    parser.add_argument("--workers", type=int, default=15, help="Number of parallel worker threads")
    parser.add_argument("--data_path", type=str, default="bengali_test.jsonl", help="Dataset path")
    parser.add_argument("--limit", type=int, default=1012, help="Limit dataset size per model")
    args = parser.parse_args()
    
    # Auto-detect provider
    model_lower = args.model.lower()
    if "gemini" in model_lower:
        provider = "gemini"
    elif "gpt-" in model_lower or "luna" in model_lower:
        provider = "openai"
    else:
        provider = "openrouter"
        
    # Load keys
    if args.key:
        if provider == "gemini":
            gemini_keys = [args.key]
        elif provider == "openai":
            openai_keys = [args.key]
        else:
            openrouter_keys = [args.key]
        print(f"[+] Using explicitly provided API key for provider {provider.upper()}")
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
                        
    print(f"[+] Loaded Key Pool: {len(gemini_keys)} Gemini | {len(openai_keys)} OpenAI | {len(openrouter_keys)} OpenRouter")
    print(f"[+] Starting BanglaSummEval Pipeline for all 8 models (Limit: {args.limit} samples)")
    print(f"[+] Judge Model: {args.model} | Provider: {provider.upper()}")
    print(f"[+] Concurrent Workers: {args.workers} | Match Threshold: {args.threshold}%")
    
    # Load dataset
    dataset = []
    with open(args.data_path, "r", encoding="utf-8") as f:
        for line in f:
            dataset.append(json.loads(line))
            
    # Apply limit
    dataset = dataset[:args.limit]
    print(f"[+] Loaded {len(dataset)} dataset samples for evaluation.")
            
    # List of models
    model_configs = [
        ("Deepseek V4 Flash", "deepseek_v4_flash_bengali_results.csv"),
        ("Gemini 2.5 Flash", "gemini_2.5_flash_bengali_results.csv"),
        ("Gemini 3.1 Flash Lite", "gemini_3.1_flash_lite_bengali_results.csv"),
        ("Gpt 4O Mini", "gpt_4o_mini_bengali_results.csv"),
        ("Gpt 5.6 Luna", "gpt_5.6_luna_bengali_results.csv"),
        ("Llama 3.3 70B (Groq)", "groq_llama70b_1000_results.csv"),
        ("Qwen 3.5 Flash", "qwen_3.5_flash_bengali_results.csv"),
        ("Qwen 3.6 27B", "qwen_3.6_27b_bengali_results.csv"),
    ]
    
    for model_name, csv_file in model_configs:
        if not os.path.exists(csv_file):
            print(f"[!] Warning: Predictions CSV {csv_file} not found. Skipping.")
            continue
            
        print(f"\n" + "="*70)
        print(f"[+] Processing Model: {model_name}")
        print("="*70)
        
        process_model(model_name, csv_file, dataset, args.model, provider, args.threshold, args.workers)

if __name__ == "__main__":
    main()
