import os
import json
import re
import time
import sys
import io
import argparse
from tqdm import tqdm
import pandas as pd
from rouge_score import rouge_scorer
import torch

def load_dataset(file_path, limit=1000):
    """Load JSONL dataset up to limit."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            data.append(json.loads(line))
    print(f"[+] Loaded {len(data)} items from {file_path}")
    return data

def clean_text(text):
    """Normalize text spacing."""
    return re.sub(r'\s+', ' ', text).strip()

class BengaliTokenizer:
    def tokenize(self, text):
        return re.findall(r'[\u0980-\u09FF\w]+', text)

def get_rouge_scorer():
    """Returns ROUGE scorer instance with Bengali Unicode tokenization."""
    return rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], tokenizer=BengaliTokenizer())

def run_lead3_baseline(dataset):
    """Lead-3 Baseline: First 3 sentences of the document."""
    predictions = []
    for item in dataset:
        sentences = re.split(r'[।!?\n]', item['text'])
        sentences = [s.strip() for s in sentences if s.strip()]
        summary = "। ".join(sentences[:3]) + ("।" if sentences else "")
        predictions.append(summary)
    return predictions

def run_seq2seq_model(model_name, dataset, device, max_input_length=512, max_output_length=128, batch_size=8):
    """Generate summaries using a Seq2Seq transformer model (BART/T5/mBART)."""
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    print(f"\n[+] Loading Model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name, 
        trust_remote_code=True,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    model.to(device)
    model.eval()

    predictions = []
    
    # Check if model requires a prompt prefix like t5
    prefix = ""
    if "t5" in model_name.lower():
        prefix = "summarize: "

    extra_gen_kwargs = {}
    if "mbart" in model_name.lower():
        tokenizer.src_lang = "bn_IN"
        if hasattr(tokenizer, "lang_code_to_id") and "bn_IN" in tokenizer.lang_code_to_id:
            extra_gen_kwargs["forced_bos_token_id"] = tokenizer.lang_code_to_id["bn_IN"]

    print(f"[+] Generating summaries with batch size {batch_size}...")
    for i in tqdm(range(0, len(dataset), batch_size)):
        batch_texts = [prefix + clean_text(item['text']) for item in dataset[i:i+batch_size]]
        
        inputs = tokenizer(
            batch_texts, 
            max_length=max_input_length, 
            padding=True, 
            truncation=True, 
            return_tensors="pt"
        ).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_length=max_output_length, 
                num_beams=4, 
                early_stopping=True,
                **extra_gen_kwargs
            )
            
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        predictions.extend(decoded)

    # Clean up GPU memory
    del model
    del tokenizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    return predictions

def run_causallm_model(model_name, dataset, device, max_input_length=1024, max_new_tokens=128, batch_size=4):
    """Generate summaries using a Causal LLM (e.g., Qwen / Llama)."""
    from transformers import AutoTokenizer, AutoModelForCausalLM

    print(f"\n[+] Loading Causal LLM: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        trust_remote_code=True, 
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )
    model.eval()

    predictions = []

    print(f"[+] Generating summaries with Causal LLM...")
    for item in tqdm(dataset):
        prompt = (
            f"<|im_start|>system\nYou are a helpful assistant that summarizes Bengali news articles accurately and concisely in Bengali.<|im_end|>\n"
            f"<|im_start|>user\nনিচের বাংলা নিবন্ধটির একটি সংক্ষিপ্ত সারসংক্ষেপ লিখুন:\n\n{clean_text(item['text'])[:1500]}\n\nসারসংক্ষেপ:<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_input_length).to(device)
        
        with torch.no_grad():
            output_ids = model.generate(
                **inputs, 
                max_new_tokens=max_new_tokens, 
                temperature=0.3, 
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id
            )
            
        input_len = inputs['input_ids'].shape[1]
        generated_tokens = output_ids[0][input_len:]
        decoded = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        predictions.append(decoded)

    del model
    del tokenizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return predictions

def run_groq_model(model_name, dataset, api_key=None):
    """Generate summaries using Groq API (e.g. Llama 3.3 70B / Llama 3.1 70B)."""
    from groq import Groq

    print(f"\n[+] Running Groq API Model: {model_name}...")
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY is not set. Please provide --groq_api_key or set GROQ_API_KEY environment variable.")
    
    client = Groq(api_key=key)
    predictions = []

    for item in tqdm(dataset):
        prompt = f"নিচের বাংলা সংবাদ নিবন্ধটির একটি নির্ভুল ও সংক্ষিপ্ত সারসংক্ষেপ ৩ বাক্যে বাংলায় লিখুন:\n\n{clean_text(item['text'])[:1500]}\n\nসারসংক্ষেপ:"
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_completion_tokens=2048,
                top_p=1,
                stream=True,
                stop=None
            )

            full_summary = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_summary += content

            predictions.append(full_summary.strip())
        except Exception as e:
            print(f"[!] Groq API error: {e}")
            predictions.append("")

    return predictions

def evaluate_predictions(dataset, predictions):
    """Compute mean ROUGE-1, ROUGE-2, and ROUGE-L scores."""
    scorer = get_rouge_scorer()
    r1, r2, rl = [], [], []

    for item, pred in zip(dataset, predictions):
        ref = item['summary']
        scores = scorer.score(ref, pred)
        r1.append(scores['rouge1'].fmeasure * 100)
        r2.append(scores['rouge2'].fmeasure * 100)
        rl.append(scores['rougeL'].fmeasure * 100)

    avg_r1 = sum(r1) / len(r1) if r1 else 0
    avg_r2 = sum(r2) / len(r2) if r2 else 0
    avg_rl = sum(rl) / len(rl) if rl else 0

    return avg_r1, avg_r2, avg_rl, r1, r2, rl

def main():
    parser = argparse.ArgumentParser(description="Benchmark 7 Summarization Models on Bengali XL-Sum")
    parser.add_argument("--data_path", type=str, default="bengali_test.jsonl", help="Path to input jsonl file")
    parser.add_argument("--limit", type=int, default=1000, help="Number of items to evaluate")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for inference")
    parser.add_argument("--output_csv", type=str, default="rouge_7_models_comparison.csv", help="Output CSV path")
    parser.add_argument("--groq_api_key", type=str, default=None, help="Groq API Key for running Llama 70B model")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[+] Using device: {device}")
    if torch.cuda.is_available():
        print(f"[+] GPU Name: {torch.cuda.get_device_name(0)}")

    dataset = load_dataset(args.data_path, limit=args.limit)

    # List of verified models to evaluate (including Llama 3.3 70B via Groq)
    model_configs = [
        {"name": "Lead-3 Baseline", "type": "baseline"},
        {"name": "csebuetnlp/mT5_multilingual_XLSum", "type": "seq2seq"},
        {"name": "csebuetnlp/banglat5", "type": "seq2seq"},
        {"name": "csebuetnlp/banglat5_small", "type": "seq2seq"},
        {"name": "google/mt5-base", "type": "seq2seq"},
        {"name": "google/mt5-small", "type": "seq2seq"},
        {"name": "facebook/mbart-large-50", "type": "seq2seq"},
        {"name": "llama-3.3-70b-versatile", "type": "groq"},
    ]

    benchmark_summary = []
    detailed_results = {}

    for config in model_configs:
        model_name = config["name"]
        model_type = config["type"]
        print(f"\n==================================================")
        print(f"       Evaluating Model: {model_name}")
        print(f"==================================================")

        start_time = time.time()
        try:
            if model_type == "baseline":
                predictions = run_lead3_baseline(dataset)
            elif model_type == "seq2seq":
                predictions = run_seq2seq_model(model_name, dataset, device, batch_size=args.batch_size)
            elif model_type == "causal":
                predictions = run_causallm_model(model_name, dataset, device, batch_size=args.batch_size)
            elif model_type == "groq":
                predictions = run_groq_model(model_name, dataset, api_key=args.groq_api_key)
            else:
                continue

            elapsed_time = time.time() - start_time
            avg_r1, avg_r2, avg_rl, r1_list, r2_list, rl_list = evaluate_predictions(dataset, predictions)

            print(f"[*] {model_name} Completed in {elapsed_time:.2f}s")
            print(f"    ROUGE-1: {avg_r1:.2f} | ROUGE-2: {avg_r2:.2f} | ROUGE-L: {avg_rl:.2f}")

            benchmark_summary.append({
                "Model": model_name,
                "Type": model_type,
                "ROUGE-1 (F1 %)": round(avg_r1, 2),
                "ROUGE-2 (F1 %)": round(avg_r2, 2),
                "ROUGE-L (F1 %)": round(avg_rl, 2),
                "Time (s)": round(elapsed_time, 2)
            })

            detailed_results[model_name] = predictions

        except Exception as e:
            import traceback
            print(f"[!] Error running model {model_name}: {e}")
            traceback.print_exc()
            benchmark_summary.append({
                "Model": model_name,
                "Type": model_type,
                "ROUGE-1 (F1 %)": "ERROR",
                "ROUGE-2 (F1 %)": "ERROR",
                "ROUGE-L (F1 %)": "ERROR",
                "Time (s)": "N/A"
            })

    # Save Results
    summary_df = pd.DataFrame(benchmark_summary)
    summary_df.to_csv(args.output_csv, index=False, encoding="utf-8-sig")

    print("\n\n==================================================")
    print("           FINAL BENCHMARK COMPARISON             ")
    print("==================================================")
    print(summary_df.to_string(index=False))
    print(f"\nResults saved to {args.output_csv}")

if __name__ == "__main__":
    main()
