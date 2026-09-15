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

en_files = {
    'GPT-5.6 Luna': 'english_XLSum_v2.0/gpt_5.6_luna_english_results.csv',
    'Gemini 3.1 Flash Lite': 'english_XLSum_v2.0/gemini_3.1_flash_lite_english_results.csv',
    'Gemini 2.5 Flash': 'english_XLSum_v2.0/gemini_2.5_flash_english_results.csv',
    'Qwen 3.5 Flash': 'english_XLSum_v2.0/qwen_3.5_flash_english_results.csv',
    'Qwen 3.6 27B': 'english_XLSum_v2.0/qwen_3.6_27b_english_results.csv',
    'DeepSeek V4 Flash': 'english_XLSum_v2.0/deepseek_v4_flash_english_results.csv',
    'GPT-4o Mini': 'english_XLSum_v2.0/gpt_4o_mini_english_results.csv',
    'LLaMA 3.3 70B': 'english_XLSum_v2.0/groq_llama70b_1012_english_results.csv'
}

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

def process_language(lang_files, lang):
    model_type = 'roberta-base' if lang == 'english' else 'bert-base-multilingual-cased'
    lang_code = 'en' if lang == 'english' else 'bn'
    
    print(f"\n{'='*40}\nProcessing {lang.upper()} ({model_type})\n{'='*40}")
    sys.stdout.flush()
    
    for model_name, path in lang_files.items():
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            print(f"Skipping {model_name}: {path} not found.")
            sys.stdout.flush()
            continue
            
        valid_refs = []
        valid_gens = []
        lengths = []
        
        for _, row in df.iterrows():
            gen = str(row.get('generated', ''))
            ref = str(row.get('reference', ''))
            cleaned = clean_reasoning_tags(gen)
            
            # Filter empty strings and DeepSeek explicit refusals
            if cleaned.strip() and ref.strip() and cleaned.strip() != 'nan' and ref.strip() != 'nan' and '作为一个人工智能语言模型' not in cleaned:
                valid_refs.append(ref)
                valid_gens.append(cleaned)
                lengths.append(len(cleaned.split()))
                
        if valid_refs:
            avg_len = np.mean(lengths)
            try:
                P, R, F1 = score(valid_gens, valid_refs, model_type=model_type, batch_size=16, device='cpu', verbose=False)
                avg_bert_f1 = F1.mean().item() * 100
                avg_bert_r = R.mean().item() * 100
                print(f"{model_name:<25} | Valid: {len(valid_refs):<4} | Len: {avg_len:5.1f} | BS-R: {avg_bert_r:5.2f} | BS-F1: {avg_bert_f1:5.2f}")
            except Exception as err:
                print(f"{model_name:<25} | Valid: {len(valid_refs):<4} | Len: {avg_len:5.1f} | ERROR: {err}")
            sys.stdout.flush()

if __name__ == '__main__':
    import sys, traceback
    try:
        process_language(en_files, 'english')
        process_language(bn_files, 'bengali')
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        traceback.print_exc()
        sys.stderr.flush()


