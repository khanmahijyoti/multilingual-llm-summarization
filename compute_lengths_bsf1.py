import pandas as pd
import numpy as np
from bert_score import score
import re
import os
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
    'DeepSeek V4 Flash': 'english_XLSum_v2.0/deepseek_v4_flash_english_results.csv',
    'Gemini 2.5 Flash': 'english_XLSum_v2.0/gemini_2.5_flash_english_results.csv',
    'Gemini 3.1 Flash Lite': 'english_XLSum_v2.0/gemini_3.1_flash_lite_english_results.csv',
    'GPT-4o Mini': 'english_XLSum_v2.0/gpt_4o_mini_english_results.csv',
    'GPT-5.6 Luna': 'english_XLSum_v2.0/gpt_5.6_luna_english_results.csv',
    'LLaMA 3.3 70B': 'english_XLSum_v2.0/groq_llama70b_1012_english_results.csv',
    'Qwen 3.5 Flash': 'english_XLSum_v2.0/qwen_3.5_flash_english_results.csv',
    'Qwen 3.6 27B': 'english_XLSum_v2.0/qwen_3.6_27b_english_results.csv'
}

bn_files = {
    'DeepSeek V4 Flash': 'deepseek_v4_flash_bengali_results.csv',
    'Gemini 2.5 Flash': 'gemini_2.5_flash_bengali_results.csv',
    'Gemini 3.1 Flash Lite': 'gemini_3.1_flash_lite_bengali_results.csv',
    'GPT-4o Mini': 'gpt_4o_mini_bengali_results.csv',
    'GPT-5.6 Luna': 'gpt_5.6_luna_bengali_results.csv',
    'LLaMA 3.3 70B': 'groq_llama70b_1000_results.csv',
    'Qwen 3.5 Flash': 'qwen_3.5_flash_bengali_results.csv',
    'Qwen 3.6 27B': 'qwen_3.6_27b_bengali_results.csv'
}

def process_language(lang_files, lang):
    results = {}
    model_type = 'roberta-base' if lang == 'english' else 'xlm-roberta-base'
    lang_code = lang[:2]
    
    for model_name, f in lang_files.items():
        df = pd.read_csv(f)
        valid_refs = []
        valid_gens = []
        lengths = []
        
        for _, row in df.iterrows():
            gen = str(row.get('generated', ''))
            ref = str(row.get('reference', ''))
            cleaned = clean_reasoning_tags(gen)
            
            # exclude deepseek refusal
            if cleaned.strip() and '作为一个人工智能语言模型' not in cleaned:
                valid_refs.append(ref)
                valid_gens.append(cleaned)
                lengths.append(len(cleaned.split()))
        
        if len(valid_refs) > 0:
            avg_len = np.mean(lengths)
            P, R, F1 = score(valid_gens, valid_refs, model_type=model_type, lang=lang_code, verbose=False)
            avg_bert_f1 = F1.mean().item() * 100
            avg_bert_r = R.mean().item() * 100
            
            results[model_name] = {
                'len': avg_len,
                'bs_f1': avg_bert_f1,
                'bs_r': avg_bert_r
            }
            print(f"{lang} {model_name}: len={avg_len:.1f}, bs_f1={avg_bert_f1:.2f}, bs_r={avg_bert_r:.2f}")
    return results

print("Processing English...")
en_results = process_language(en_files, 'english')
print("Processing Bengali...")
bn_results = process_language(bn_files, 'bengali')
