import re
import os
import glob
import pandas as pd
from rouge_score import rouge_scorer

class IndicTokenizer:
    def tokenize(self, text):
        return re.findall(r'[\u0980-\u09FF\w]+', text.lower())

def clean_reasoning_tags(text):
    if not isinstance(text, str):
        return text
    
    # Check if there's any tag
    if not re.search(r'<(?:think|thinking|reasoning)>|</(?:think|thinking|reasoning)>|\[(?:analysis|reasoning)\]', text, re.IGNORECASE):
        return text

    # Strip full blocks
    text = re.sub(r'<(think|thinking|reasoning)>.*?</\1>', '', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Strip unmatched closing tags at the very beginning (like Qwen 3.5 did)
    text = re.sub(r'^(\s*</(?:think|thinking|reasoning)>\s*)+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^(\s*\[(?:analysis|reasoning)\]\s*)+', '', text, flags=re.IGNORECASE)
    
    # Strip unclosed tags trailing at the end (or making up the whole string)
    text = re.sub(r'<(think|thinking|reasoning)>.*', '', text, flags=re.DOTALL|re.IGNORECASE)
    
    return text.strip()

def rescore_all_files():
    base = os.path.dirname(os.path.abspath(__file__))
    en_files = glob.glob(os.path.join(base, 'english_XLSum_v2.0', '*_results.csv'))
    bn_files = [f for f in glob.glob(os.path.join(base, '*_bengali_results.csv')) if 'judge' not in f]
    
    en_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    bn_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False, tokenizer=IndicTokenizer())

    changes_made = []

    for path, is_en in [(f, True) for f in en_files] + [(f, False) for f in bn_files]:
        try:
            df = pd.read_csv(path)
        except Exception as e:
            continue
            
        if 'generated' not in df.columns:
            continue
            
        scorer = en_scorer if is_en else bn_scorer
        model_name = os.path.basename(path).replace('_english_results.csv', '').replace('_bengali_results.csv', '')
        
        orig_r1 = df['rouge1'].mean()
        
        modified_count = 0
        for idx in df.index:
            orig_text = str(df.at[idx, 'generated'])
            new_text = clean_reasoning_tags(orig_text)
            
            if new_text != orig_text:
                modified_count += 1
                df.at[idx, 'generated'] = new_text
                
                ref = str(df.at[idx, 'reference'])
                if not new_text.strip():
                    df.at[idx, 'rouge1'] = 0.0
                    df.at[idx, 'rouge2'] = 0.0
                    df.at[idx, 'rougeL'] = 0.0
                else:
                    try:
                        s = scorer.score(ref, new_text)
                        df.at[idx, 'rouge1'] = round(s['rouge1'].fmeasure * 100, 2)
                        df.at[idx, 'rouge2'] = round(s['rouge2'].fmeasure * 100, 2)
                        df.at[idx, 'rougeL'] = round(s['rougeL'].fmeasure * 100, 2)
                    except Exception as e:
                        pass
        
        if modified_count > 0:
            df.to_csv(path, index=False, encoding='utf-8-sig')
            new_r1 = df['rouge1'].mean()
            changes_made.append({
                'model': model_name,
                'lang': 'English' if is_en else 'Bengali',
                'affected_rows': modified_count,
                'r1_before': orig_r1,
                'r1_after': new_r1,
                'r2_after': df['rouge2'].mean(),
                'rl_after': df['rougeL'].mean()
            })
            
    return changes_made

if __name__ == '__main__':
    changes = rescore_all_files()
    if not changes:
        print("No remaining leaked tags found.")
    else:
        print("Found and cleaned leaked tags in:")
        for c in changes:
            print(f"  {c['lang']} {c['model']}: {c['affected_rows']} rows. R1 {c['r1_before']:.2f} -> {c['r1_after']:.2f} (R2={c['r2_after']:.2f}, RL={c['rl_after']:.2f})")
