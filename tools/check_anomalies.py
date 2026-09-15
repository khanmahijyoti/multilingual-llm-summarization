import pandas as pd
import re

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

bn_files = [
    'deepseek_v4_flash_bengali_results.csv',
    'gemini_2.5_flash_bengali_results.csv',
    'gemini_3.1_flash_lite_bengali_results.csv',
    'gpt_4o_mini_bengali_results.csv',
    'gpt_5.6_luna_bengali_results.csv',
    'groq_llama70b_1000_results.csv',
    'qwen_3.5_flash_bengali_results.csv',
    'qwen_3.6_27b_bengali_results.csv'
]
en_files = [
    'english_XLSum_v2.0/deepseek_v4_flash_english_results.csv',
    'english_XLSum_v2.0/gemini_2.5_flash_english_results.csv',
    'english_XLSum_v2.0/gemini_3.1_flash_lite_english_results.csv',
    'english_XLSum_v2.0/gpt_4o_mini_english_results.csv',
    'english_XLSum_v2.0/gpt_5.6_luna_english_results.csv',
    'english_XLSum_v2.0/groq_llama70b_1012_english_results.csv',
    'english_XLSum_v2.0/qwen_3.5_flash_english_results.csv',
    'english_XLSum_v2.0/qwen_3.6_27b_english_results.csv'
]

with open('one_word_anomalies.txt', 'w', encoding='utf-8') as f_out:
    for name, files in [('EN', en_files), ('BN', bn_files)]:
        for f in files:
            df = pd.read_csv(f)
            for _, row in df.iterrows():
                cleaned = clean_reasoning_tags(str(row.get('generated', '')))
                if cleaned.strip():
                    words = cleaned.split()
                    if len(words) == 1:
                        f_out.write(f"{name} {f.split('/')[-1]} : {repr(cleaned)}\n")
