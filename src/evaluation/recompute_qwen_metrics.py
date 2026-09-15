import pandas as pd
import sacrebleu
from bert_score import score
from rouge_score import rouge_scorer
import re
import os
import warnings
warnings.filterwarnings('ignore')

class IndicTokenizer:
    def tokenize(self, text):
        return re.findall(r'[\u0980-\u09FF\w]+', text.lower())

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

def compute_all_metrics(csv_path, lang):
    df = pd.read_csv(csv_path)
    
    valid_refs = []
    valid_gens = []

    for idx, row in df.iterrows():
        gen = str(row['generated'])
        ref = str(row['reference'])
        cleaned = clean_reasoning_tags(gen)
        if cleaned:
            valid_refs.append(ref)
            valid_gens.append(cleaned)

    # ROUGE
    if lang == 'english':
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    else:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False, tokenizer=IndicTokenizer())
    
    r1_sum, r2_sum, rl_sum = 0, 0, 0
    for r, g in zip(valid_refs, valid_gens):
        s = scorer.score(r, g)
        r1_sum += s['rouge1'].fmeasure * 100
        r2_sum += s['rouge2'].fmeasure * 100
        rl_sum += s['rougeL'].fmeasure * 100
        
    avg_r1 = r1_sum / len(valid_refs)
    avg_r2 = r2_sum / len(valid_refs)
    avg_rl = rl_sum / len(valid_refs)
    
    # BLEU & chrF
    if lang == 'english':
        bleu = sacrebleu.corpus_bleu(valid_gens, [valid_refs]).score
        chrf = sacrebleu.corpus_chrf(valid_gens, [valid_refs]).score
    else:
        bleu = sacrebleu.corpus_bleu(valid_gens, [valid_refs], tokenize='none').score
        chrf = sacrebleu.corpus_chrf(valid_gens, [valid_refs]).score
        
    # BERTScore
    model_type = 'roberta-base' if lang == 'english' else 'xlm-roberta-base'
    P, R, F1 = score(valid_gens, valid_refs, model_type=model_type, lang=lang[:2], verbose=False)
    
    avg_bert_r = R.mean().item() * 100
    
    print(f"\n--- {lang.upper()} ---")
    print(f"Valid Count: {len(valid_refs)}")
    print(f"R1: {avg_r1:.2f}  R2: {avg_r2:.2f}  RL: {avg_rl:.2f}")
    print(f"BLEU: {bleu:.2f}  chrF: {chrf:.2f}  BERTScore-R: {avg_bert_r:.2f}")

base = os.path.dirname(os.path.abspath(__file__))
compute_all_metrics(os.path.join(base, 'english_XLSum_v2.0', 'qwen_3.6_27b_english_results.csv'), 'english')
compute_all_metrics(os.path.join(base, 'qwen_3.6_27b_bengali_results.csv'), 'bengali')
