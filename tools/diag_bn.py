import pandas as pd
import numpy as np
from bert_score import score
import re
import sys

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

df = pd.read_csv('groq_llama70b_1000_results.csv')
valid_refs = []
valid_gens = []

for idx, row in df.iterrows():
    gen = str(row.get('generated', ''))
    ref = str(row.get('reference', ''))
    cleaned = clean_reasoning_tags(gen)
    if cleaned.strip() and '作为一个人工智能语言模型' not in cleaned:
        valid_refs.append(ref)
        valid_gens.append(cleaned)

print(f"Total valid: {len(valid_gens)}")
sys.stdout.flush()

for i in range(0, len(valid_gens), 50):
    batch_g = valid_gens[i:i+50]
    batch_r = valid_refs[i:i+50]
    try:
        P, R, F1 = score(batch_g, batch_r, model_type='xlm-roberta-base', verbose=False)
        print(f"Batch {i}-{i+len(batch_g)} OK: {F1.mean().item():.4f}")
        sys.stdout.flush()
    except Exception as e:
        print(f"Batch {i}-{i+len(batch_g)} FAILED: {e}")
        sys.stdout.flush()
