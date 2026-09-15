import pandas as pd
import numpy as np
import torch
import re
import sacrebleu
from bert_score import score

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
    'LLaMA 3.3 70B': 'english_XLSum_v2.0/groq_llama70b_1012_english_results.csv',
}

bn_files = {
    'LLaMA 3.3 70B': 'groq_llama70b_1000_results.csv',
    'GPT-4o Mini': 'gpt_4o_mini_bengali_results.csv',
    'Gemini 2.5 Flash': 'gemini_2.5_flash_bengali_results.csv',
    'DeepSeek V4 Flash': 'deepseek_v4_flash_bengali_results.csv',
    'Qwen 3.5 Flash': 'qwen_3.5_flash_bengali_results.csv',
    'Gemini 3.1 Flash Lite': 'gemini_3.1_flash_lite_bengali_results.csv',
    'GPT-5.6 Luna': 'gpt_5.6_luna_bengali_results.csv',
    'Qwen 3.6 27B': 'qwen_3.6_27b_bengali_results.csv',
}

def eval_dataset(files, lang, model_type):
    print(f"\n==================== {lang} ({model_type}) ====================")
    rows = []
    for name, path in files.items():
        df = pd.read_csv(path)
        valid_refs = []
        valid_gens = []
        r1_list, r2_list, rl_list = [], [], []
        
        for _, row in df.iterrows():
            gen = str(row.get('generated', ''))
            ref = str(row.get('reference', ''))
            cleaned = clean_reasoning_tags(gen)
            if cleaned.strip() and '作为一个人工智能语言模型' not in cleaned:
                valid_refs.append(ref)
                valid_gens.append(cleaned)
                if 'rouge1' in row and not pd.isna(row['rouge1']):
                    r1_list.append(float(row['rouge1']))
                    r2_list.append(float(row['rouge2']))
                    rl_list.append(float(row['rougeL']))
                    
        bleu = sacrebleu.metrics.BLEU(effective_order=True).corpus_score(valid_gens, [valid_refs]).score
        chrf = sacrebleu.metrics.CHRF().corpus_score(valid_gens, [valid_refs]).score
        
        try:
            P, R, F1 = score(valid_gens, valid_refs, model_type=model_type, device='cuda', batch_size=64, verbose=False)
            bs_p = P.mean().item() * 100
            bs_r = R.mean().item() * 100
            bs_f1 = F1.mean().item() * 100
        except Exception as e:
            print(f"Error for {name}: {e}", flush=True)
            bs_p, bs_r, bs_f1 = 0, 0, 0
        
        avg_r1 = np.mean(r1_list) if r1_list else 0
        avg_r2 = np.mean(r2_list) if r2_list else 0
        avg_rl = np.mean(rl_list) if rl_list else 0
        
        print(f"{name:22s} | N={len(valid_gens):4d} | R-1={avg_r1:5.2f} | R-2={avg_r2:4.2f} | R-L={avg_rl:5.2f} | BLEU={bleu:4.2f} | chrF={chrf:5.2f} | BERT-R={bs_r:5.2f} | BERT-F1={bs_f1:5.2f} | BERT-P={bs_p:5.2f}", flush=True)
        rows.append({
            'Model': name,
            'N': len(valid_gens),
            'R1': avg_r1, 'R2': avg_r2, 'RL': avg_rl,
            'BLEU': bleu, 'chrF': chrf,
            'BERT-R': bs_r, 'BERT-F1': bs_f1, 'BERT-P': bs_p
        })
    df_out = pd.DataFrame(rows)
    df_out.to_csv(f"eval_{lang.lower()}_metrics.csv", index=False)
    return df_out

en_df = eval_dataset(en_files, 'English', 'roberta-base')
bn_df = eval_dataset(bn_files, 'Bengali', 'xlm-roberta-base')
