import pandas as pd
from bert_score import score
import sys

df = pd.read_csv('groq_llama70b_1000_results.csv')
refs = df['reference'].tolist()
gens = df['generated'].tolist()

print(f"Loaded {len(refs)} rows from groq_llama70b_1000_results.csv")
sys.stdout.flush()

for start in range(0, 10):
    print(f"Scoring item {start}...", end="", flush=True)
    P, R, F1 = score([gens[start]], [refs[start]], model_type='xlm-roberta-base', num_layers=9, device='cpu', verbose=False)
    print(f" OK! F1: {F1.item():.4f}")
    sys.stdout.flush()
