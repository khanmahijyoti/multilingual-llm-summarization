import os
import sys
import re
import pandas as pd
import numpy as np
import torch
from bert_score import BERTScorer

# Set environment
os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def clean_reasoning_tags(text):
    if pd.isna(text): return ''
    text = str(text)
    if not re.search(r'<(?:think|thinking|reasoning)>|</(?:think|thinking|reasoning)>|\[(?:analysis|reasoning)\]', text, re.IGNORECASE):
        return text
    text = re.sub(r'<(think|thinking|reasoning)>.*?</\1>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'^(\s*</(?:think|thinking|reasoning)>\s*)+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^(\s*\[(?:analysis|reasoning)\]\s*)+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<(think|thinking|reasoning)>.*', '', text, flags=re.DOTALL|re.IGNORECASE)
    return text.strip()

bn_files = {
    'GPT-5.6 Luna': 'gpt_5.6_luna_bengali_results.csv',
    'Gemini 3.1 Flash Lite': 'gemini_3.1_flash_lite_bengali_results.csv',
    'Gemini 2.5 Flash': 'gemini_2.5_flash_bengali_results.csv',
    'Qwen 3.5 Flash': 'qwen_3.5_flash_bengali_results.csv',
    'Qwen 3.6 27B': 'qwen_3.6_27b_bengali_results.csv',
    'DeepSeek V4 Flash': 'deepseek_v4_flash_bengali_results.csv',
    'GPT-4o Mini': 'gpt_4o_mini_bengali_results.csv',
    'LLaMA 3.3 70B': 'groq_llama70b_1000_results.csv',
}

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}", flush=True)

scorer = BERTScorer(model_type='xlm-roberta-base', device=device)

results = []
for name, path in bn_files.items():
    df = pd.read_csv(path)
    valid_refs = []
    valid_gens = []
    for _, row in df.iterrows():
        gen = str(row.get('generated', ''))
        ref = str(row.get('reference', ''))
        cleaned = clean_reasoning_tags(gen)
        if cleaned.strip() and '作为一个人工智能语言模型' not in cleaned:
            valid_refs.append(ref)
            valid_gens.append(cleaned)
    
    print(f"Evaluating {name} ({len(valid_gens)} items)...", flush=True)
    P, R, F1 = scorer.score(valid_gens, valid_refs, batch_size=32)
    
    mean_p = P.mean().item() * 100
    mean_r = R.mean().item() * 100
    mean_f1 = F1.mean().item() * 100
    print(f"{name:22s} | P={mean_p:5.2f} | R={mean_r:5.2f} | F1={mean_f1:5.2f}", flush=True)
    results.append({
        'Model': name,
        'N': len(valid_gens),
        'BERT-P': mean_p,
        'BERT-R': mean_r,
        'BERT-F1': mean_f1
    })

res_df = pd.DataFrame(results)
res_df.to_csv('eval_bengali_bertscore.csv', index=False)
print("Finished Bengali BERTScore evaluation!", flush=True)
