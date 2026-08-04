import os
import json
import time
import argparse
import urllib.request
import urllib.error
import re
import torch
import pandas as pd
from bert_score import score

# Set up device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Global key pools
openrouter_keys = []
gemini_keys = []
openai_keys = []
current_key_idx = 0

def call_gemini_api(prompt, system_prompt, model, api_key, timeout=30):
    full_prompt = f"{system_prompt}\n\nContext/Input:\n{prompt}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.0,  # Greedy
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

def call_openai_api(prompt, system_prompt, model, api_key, timeout=30):
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
    
    # Handle API differences for gpt-5/o1/luna models (no max_tokens, no temperature)
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

def call_openrouter_api(prompt, system_prompt, model, api_key, timeout=30):
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

def call_api_with_rotation(prompt, system_prompt, model, provider, timeout=30):
    global current_key_idx
    if provider == "gemini":
        pool = gemini_keys
    elif provider == "openai":
        pool = openai_keys
    else:
        pool = openrouter_keys
    
    if not pool:
        raise ValueError(f"No keys loaded for provider: {provider}")
        
    attempts = 0
    max_attempts = len(pool)
    
    while attempts < max_attempts:
        api_key = pool[current_key_idx]
        try:
            if provider == "gemini":
                return call_gemini_api(prompt, system_prompt, model, api_key, timeout)
            elif provider == "openai":
                return call_openai_api(prompt, system_prompt, model, api_key, timeout)
            else:
                return call_openrouter_api(prompt, system_prompt, model, api_key, timeout)
        except urllib.error.HTTPError as e:
            print(f"    [!] Key index {current_key_idx} failed with HTTP Error {e.code}: {e.reason}")
            try:
                err_body = e.read().decode('utf-8')
                print(f"        Response Body: {err_body}")
            except Exception:
                pass
            current_key_idx = (current_key_idx + 1) % len(pool)
            print(f"        Rotating to key index {current_key_idx}...")
            time.sleep(1)
        except Exception as e:
            print(f"    [!] Key index {current_key_idx} failed with error: {e}")
            current_key_idx = (current_key_idx + 1) % len(pool)
            time.sleep(1)
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
    P, R, F1 = score(predictions, references, model_type="xlm-roberta-base", device=device, verbose=False)
    return [r.item() * 100 for r in R]

def run_pipeline(source_doc, target_text, model, provider, similarity_threshold=85.0):
    print("\n" + "="*50)
    print(f"[+] Starting BanglaSummEval Pipeline")
    print(f"    Provider: {provider.upper()} | Model: {model}")
    print(f"    Local BERTScore Device: {device}")
    print("="*50)
    
    # ----------------------------------------------------
    # STAGE 1: PRECISION (Factual Consistency of Summary)
    # ----------------------------------------------------
    print("\n--- Evaluating Summary Precision (Factuality) ---")
    print("[1] Extracting Entities from Generated Summary...")
    summary_entities = extract_entities_and_nouns(target_text, model, provider)
    print(f"    Extracted Entities: {', '.join(summary_entities) if summary_entities else 'None'}")
    
    prec_correct = 0
    prec_total = 0
    
    if summary_entities:
        questions_s = []
        for ans in summary_entities:
            print(f"  -> Generating question for answer '{ans}'...")
            q = generate_question(target_text, ans, model, provider)
            questions_s.append((ans, q))
            print(f"     Question: '{q}'")
            
        print("\n[2] Answering generated questions using Source Document...")
        answers_d = []
        for ans, q in questions_s:
            print(f"  -> Answering '{q}' in source...")
            pred_ans = answer_question(source_doc, q, model, provider)
            answers_d.append((ans, q, pred_ans))
            print(f"     Predicted Answer: '{pred_ans}'")
            
        # Compute BERTScore semantic similarities
        preds = [a[2] for a in answers_d]
        refs = [a[0] for a in answers_d]
        similarities = compute_bertscore_recall(preds, refs)
        
        print("\n[3] Calculating Semantic Matches (BERTScore-Recall):")
        for i, (ans, q, pred_ans) in enumerate(answers_d):
            sim = similarities[i]
            matched = sim >= similarity_threshold
            if matched:
                prec_correct += 1
            prec_total += 1
            status = "MATCHED (Consistent)" if matched else "FAILED (Hallucinated/Incorrect)"
            print(f"  -> Target: '{ans}' | Pred: '{pred_ans}' | Recall Sim: {sim:.2f}% | {status}")
            
    precision_score = (prec_correct / prec_total * 100) if prec_total > 0 else 100.0
    print(f"\n=> Precision (Factuality): {precision_score:.2f}% ({prec_correct}/{prec_total})")
    
    # ----------------------------------------------------
    # STAGE 2: RECALL (Content Coverage of Source)
    # ----------------------------------------------------
    print("\n--- Evaluating Source Recall (Content Coverage) ---")
    print("[1] Extracting Main Entities from Source Document...")
    source_snippet = source_doc[:1200]
    source_entities = extract_entities_and_nouns(source_snippet, model, provider)[:6] # Limit to top 6 entities
    print(f"    Extracted Entities: {', '.join(source_entities) if source_entities else 'None'}")
    
    rec_correct = 0
    rec_total = 0
    
    if source_entities:
        questions_d = []
        for ans in source_entities:
            print(f"  -> Generating question for answer '{ans}'...")
            q = generate_question(source_snippet, ans, model, provider)
            questions_d.append((ans, q))
            print(f"     Question: '{q}'")
            
        print("\n[2] Answering generated questions using Summary...")
        answers_s = []
        for ans, q in questions_d:
            print(f"  -> Answering '{q}' in summary...")
            pred_ans = answer_question(target_text, q, model, provider)
            answers_s.append((ans, q, pred_ans))
            print(f"     Predicted Answer: '{pred_ans}'")
            
        # Compute BERTScore semantic similarities
        preds = [a[2] for a in answers_s]
        refs = [a[0] for a in answers_s]
        similarities = compute_bertscore_recall(preds, refs)
        
        print("\n[3] Calculating Semantic Matches (BERTScore-Recall):")
        for i, (ans, q, pred_ans) in enumerate(answers_s):
            sim = similarities[i]
            matched = sim >= similarity_threshold
            if matched:
                rec_correct += 1
            rec_total += 1
            status = "MATCHED (Covered)" if matched else "FAILED (Missing from summary)"
            print(f"  -> Target: '{ans}' | Pred: '{pred_ans}' | Recall Sim: {sim:.2f}% | {status}")
            
    recall_score = (rec_correct / rec_total * 100) if rec_total > 0 else 0.0
    print(f"\n=> Recall (Coverage): {recall_score:.2f}% ({rec_correct}/{rec_total})")
    
    # ----------------------------------------------------
    # STAGE 3: COMBINE F1
    # ----------------------------------------------------
    f1_score = (2 * precision_score * recall_score) / (precision_score + recall_score) if (precision_score + recall_score) > 0 else 0.0
    
    print("\n" + "="*50)
    print(f"BanglaSummEval Final F1: {f1_score:.2f}%")
    print(f"  - Precision (Factual Consistency): {precision_score:.2f}%")
    print(f"  - Recall (Content Coverage): {recall_score:.2f}%")
    print("="*50)
    
    return precision_score, recall_score, f1_score

def main():
    global openrouter_keys, gemini_keys, openai_keys
    parser = argparse.ArgumentParser(description="BanglaSummEval Question-Answering Evaluation Pipeline")
    parser.add_argument("--sample_index", type=int, default=0, help="Index of the test sample to evaluate")
    parser.add_argument("--results_csv", type=str, default="deepseek_v4_flash_bengali_results.csv", help="Path to predictions CSV")
    parser.add_argument("--data_path", type=str, default="bengali_test.jsonl", help="Path to dataset JSONL")
    parser.add_argument("--keys_file", type=str, default="api keys", help="File containing API keys")
    parser.add_argument("--key", type=str, default=None, help="Specific API key to use (bypasses keys file)")
    parser.add_argument("--model", type=str, default="qwen/qwen-2.5-7b-instruct", help="Model name (e.g. qwen/qwen-2.5-7b-instruct, gemini-1.5-flash, gpt-4o-mini)")
    parser.add_argument("--threshold", type=float, default=85.0, help="BERTScore-Recall match threshold")
    args = parser.parse_args()
    
    # Auto-detect provider
    model_lower = args.model.lower()
    if "gemini" in model_lower:
        provider = "gemini"
    elif "gpt-" in model_lower or "luna" in model_lower:
        provider = "openai"
    else:
        provider = "openrouter"
    
    if args.key:
        if provider == "gemini":
            gemini_keys = [args.key]
        elif provider == "openai":
            openai_keys = [args.key]
        else:
            openrouter_keys = [args.key]
        print(f"[+] Using explicitly provided API key for provider {provider.upper()}")
    else:
        # Read API keys from file
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
                        
    print(f"[+] Loaded Key Pool: {len(gemini_keys)} Gemini keys | {len(openai_keys)} OpenAI keys | {len(openrouter_keys)} OpenRouter keys.")
    print(f"[+] Auto-detected provider: {provider.upper()}")
        
    # Read dataset sample
    if not os.path.exists(args.data_path):
        raise FileNotFoundError(f"Dataset file not found: {args.data_path}")
        
    with open(args.data_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx == args.sample_index:
                sample = json.loads(line)
                break
                
    # Read model prediction
    if not os.path.exists(args.results_csv):
        raise FileNotFoundError(f"Results CSV file not found: {args.results_csv}")
        
    df = pd.read_csv(args.results_csv)
    sample_id = str(sample['id'])
    matched_rows = df[df['id'].astype(str) == sample_id]
    
    if matched_rows.empty:
        raise ValueError(f"Could not find summary for sample ID {sample_id} in {args.results_csv}")
        
    generated_summary = matched_rows.iloc[0]['generated']
    reference_summary = matched_rows.iloc[0]['reference']
    source_document = sample['text']
    
    print(f"\n[+] Loaded Sample ID: {sample_id}")
    print(f"[+] Source Document Length: {len(source_document)} characters")
    print(f"[+] Reference Summary: {reference_summary}")
    print(f"[+] Generated Summary: {generated_summary}")
    
    # Run pipeline
    run_pipeline(source_document, generated_summary, args.model, provider, args.threshold)

if __name__ == "__main__":
    main()
