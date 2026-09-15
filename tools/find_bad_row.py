import pandas as pd
from bert_score import score
import sys, traceback

df = pd.read_csv('groq_llama70b_1000_results.csv')

for idx, row in df.iterrows():
    ref = str(row.get('reference', ''))
    gen = str(row.get('generated', ''))
    try:
        P, R, F1 = score([gen], [ref], model_type='xlm-roberta-base', device='cpu', verbose=False)
    except Exception as e:
        print(f"FAILED ROW {idx}: {e}")
        traceback.print_exc()
        sys.stdout.flush()
        break
    if (idx + 1) % 10 == 0:
        print(f"Checked {idx + 1} rows OK")
        sys.stdout.flush()
