import pandas as pd
import sys

print("Step 1: Reading CSV...")
sys.stdout.flush()
df = pd.read_csv('groq_llama70b_1000_results.csv')
ref = str(df['reference'].iloc[0])
gen = str(df['generated'].iloc[0])

print("Step 2: Importing bert_score...")
sys.stdout.flush()
from bert_score import BERTScorer

print("Step 3: Creating BERTScorer without lang / baseline...")
sys.stdout.flush()
try:
    scorer = BERTScorer(model_type='xlm-roberta-base', rescale_with_baseline=False)
    print("Scorer created successfully!")
except Exception as e:
    print("Scorer init failed:", e)
sys.stdout.flush()

print("Step 4: Scoring item 0...")
sys.stdout.flush()
try:
    P, R, F1 = scorer.score([gen], [ref])
    print("Score success! F1:", F1.item(), "R:", R.item())
except Exception as e:
    print("Scoring failed:", e)
sys.stdout.flush()
