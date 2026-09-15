import re
import os
import pandas as pd
from rouge_score import rouge_scorer

class IndicTokenizer:
    def tokenize(self, text):
        return re.findall(r'[\u0980-\u09FF\w]+', text.lower())

def strip_think(text):
    if not isinstance(text, str): return ''
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<think>.*', '', text, flags=re.DOTALL|re.IGNORECASE)
    return text.strip()

def rescore(path, lang):
    df = pd.read_csv(path)
    if 'generated' not in df.columns: return
    leaked = df['generated'].str.contains('<think>', na=False, case=False)
    if leaked.sum() == 0: return

    df.loc[leaked, 'generated'] = df.loc[leaked, 'generated'].apply(strip_think)

    if lang == 'english':
        scorer_obj = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    else:
        scorer_obj = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False, tokenizer=IndicTokenizer())

    for idx in df.index[leaked]:
        ref = str(df.at[idx, 'reference'])
        gen = str(df.at[idx, 'generated'])
        if not gen.strip():
            df.at[idx, 'rouge1'] = 0.0
            df.at[idx, 'rouge2'] = 0.0
            df.at[idx, 'rougeL'] = 0.0
            continue
        try:
            s = scorer_obj.score(ref, gen)
            df.at[idx, 'rouge1'] = round(s['rouge1'].fmeasure * 100, 2)
            df.at[idx, 'rouge2'] = round(s['rouge2'].fmeasure * 100, 2)
            df.at[idx, 'rougeL'] = round(s['rougeL'].fmeasure * 100, 2)
        except Exception as e:
            print(f"Error {idx}: {e}")

    df.to_csv(path, index=False, encoding='utf-8-sig')
    r1, r2, rl = df['rouge1'].mean(), df['rouge2'].mean(), df['rougeL'].mean()
    print(f"Updated {path} - R1: {r1:.2f}, R2: {r2:.2f}, RL: {rl:.2f}")

base = os.path.dirname(os.path.abspath(__file__))
rescore(os.path.join(base, 'english_XLSum_v2.0', 'qwen_3.6_27b_english_results.csv'), 'english')
rescore(os.path.join(base, 'qwen_3.6_27b_bengali_results.csv'), 'bengali')
