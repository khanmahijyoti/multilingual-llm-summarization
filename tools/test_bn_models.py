import pandas as pd
import numpy as np
from bert_score import score
import re
import sys
import warnings
warnings.filterwarnings('ignore')

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
    'LLaMA 3.3 70B': 'groq_llama70b_1000_results.csv',
    'GPT-4o Mini': 'gpt_4o_mini_bengali_results.csv',
    'Gemini 2.5 Flash': 'gemini_2.5_flash_bengali_results.csv',
    'DeepSeek V4 Flash': 'deepseek_v4_flash_bengali_results.csv',
    'Qwen 3.5 Flash': 'qwen_3.5_flash_bengali_results.csv',
    'Gemini 3.1 Flash Lite': 'gemini_3.1_flash_lite_bengali_results.csv',
    'GPT-5.6 Luna': 'gpt_5.6_luna_bengali_results.csv',
    'Qwen 3.6 27B': 'qwen_3.6_27b_bengali_results.csv'
}

for model_name, path in bn_files.items():
    print(f"Testing {model_name} from {path}...")
    sys.stdout.flush()
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.stdout.flush()
        continue
    
    valid_refs = []
    valid_gens = []
    lengths = []
    
    for _, row in df.iterrows():
        gen = str(row.get('generated', ''))
        ref = str(row.get('reference', ''))
        cleaned = clean_reasoning_tags(gen)
        if cleaned.strip() and '作为一个人工智能语言模型' not in cleaned:
            valid_refs.append(ref)
            valid_gens.append(cleaned)
            lengths.append(len(cleaned.split()))
            
    print(f"{model_name}: {len(valid_refs)} valid rows")
    sys.stdout.flush()
    if valid_refs:
        try:
            P, R, F1 = score(valid_gens, valid_refs, model_type='xlm-roberta-base', lang='bn', verbose=False)
            avg_bert_f1 = F1.mean().item() * 100
            avg_bert_r = R.mean().item() * 100
            avg_len = np.mean(lengths)
            print(f"DONE {model_name} | Valid: {len(valid_refs)} | Len: {avg_len:.1f} | BS-R: {avg_bert_r:.2f} | BS-F1: {avg_bert_f1:.2f}")
            sys.stdout.flush()
        except Exception as e:
            print(f"ERROR on {model_name}: {e}")
            import traceback
            traceback.print_exc()
            sys.stdout.flush()
