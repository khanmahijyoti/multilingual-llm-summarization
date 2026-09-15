import pandas as pd
from bert_score import score
import sys

df = pd.read_csv('groq_llama70b_1000_results.csv')
valid_refs = df['reference'].tolist()
valid_gens = df['generated'].tolist()

for i in range(50):
    print(f"Testing item {i}...", end="", flush=True)
    P, R, F1 = score([str(valid_gens[i])], [str(valid_refs[i])], model_type='xlm-roberta-base', verbose=False)
    print(f" OK ({F1.item():.4f})")
    sys.stdout.flush()
