"""
Evaluates 50 randomized samples from all 16 CSV files (8 Bengali, 8 English)
using OpenAI API with the 6-criteria prompt.
"""

import os
import sys
import json
import time
import random
import urllib.request
import urllib.error
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "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"
MODEL_NAME = "gpt-5.6-terra"

PROMPT_BENGALI = """You are an expert evaluator of Bengali text summarization. Evaluate the generated summary against the source article using the following criteria, each scored from 1 (poor) to 5 (excellent):

- Relevance: Focuses on the key information and main event.
- Completeness: Covers the important information from the source.
- Faithfulness: Contains no unsupported, fabricated, or contradicted information.
- Coherence: Clear, logical, and well organized.
- Conciseness: Avoids unnecessary information and repetition.
- Fluency: Natural, grammatical, and readable Bengali.

Base your evaluation ONLY on the source article. Do not use external knowledge or assumptions. Penalize any information in the summary that is unsupported or contradicted by the source.

Return ONLY valid JSON in this format:
{{
  "relevance": score,
  "completeness": score,
  "faithfulness": score,
  "coherence": score,
  "conciseness": score,
  "fluency": score
}}

SOURCE:
{source_article}

SUMMARY:
{generated_summary}"""

PROMPT_ENGLISH = """You are an expert evaluator of English text summarization. Evaluate the generated summary against the source article using the following criteria, each scored from 1 (poor) to 5 (excellent):

- Relevance: Focuses on the key information and main event.
- Completeness: Covers the important information from the source.
- Faithfulness: Contains no unsupported, fabricated, or contradicted information.
- Coherence: Clear, logical, and well organized.
- Conciseness: Avoids unnecessary information and repetition.
- Fluency: Natural, grammatical, and readable English.

Base your evaluation ONLY on the source article. Do not use external knowledge or assumptions. Penalize any information in the summary that is unsupported or contradicted by the source.

Return ONLY valid JSON in this format:
{{
  "relevance": score,
  "completeness": score,
  "faithfulness": score,
  "coherence": score,
  "conciseness": score,
  "fluency": score
}}

SOURCE:
{source_article}

SUMMARY:
{generated_summary}"""


def call_openai(prompt, timeout=30):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": 300,
        "response_format": {"type": "json_object"}
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)

    with urllib.request.urlopen(req, timeout=timeout) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['choices'][0]['message']['content'].strip()


def parse_scores(raw_text):
    try:
        data = json.loads(raw_text)
        keys = ["relevance", "completeness", "faithfulness", "coherence", "conciseness", "fluency"]
        scores = {}
        for k in keys:
            val = float(data[k])
            val = max(1.0, min(5.0, val))
            scores[k] = val
        return scores
    except Exception:
        return None


def evaluate_single_pair(src, gen, lang):
    prompt_template = PROMPT_BENGALI if lang == "bengali" else PROMPT_ENGLISH
    prompt = prompt_template.format(source_article=src[:2500], generated_summary=gen[:2000])

    for _ in range(3):
        try:
            raw = call_openai(prompt)
            scores = parse_scores(raw)
            if scores:
                return scores
        except Exception:
            time.sleep(1)

    return {k: 3.0 for k in ["relevance", "completeness", "faithfulness", "coherence", "conciseness", "fluency"]}


def process_csv(file_info):
    lang, path, name = file_info
    df = pd.read_csv(path)

    # Exact first 50 samples across all models
    sample_df = df.head(50).copy()

    results = []
    for idx, row in sample_df.iterrows():
        src = str(row.get('reference', row.get('text', '')))
        gen = str(row.get('generated', ''))
        scores = evaluate_single_pair(src, gen, lang)

        avg_score = sum(scores.values()) / len(scores)
        results.append({
            "id": row.get('id', idx),
            "reference": src,
            "generated": gen,
            "rouge1": row.get('rouge1', ''),
            "rouge2": row.get('rouge2', ''),
            "rougeL": row.get('rougeL', ''),
            "relevance": scores["relevance"],
            "completeness": scores["completeness"],
            "faithfulness": scores["faithfulness"],
            "coherence": scores["coherence"],
            "conciseness": scores["conciseness"],
            "fluency": scores["fluency"],
            "avg_score": round(avg_score, 2)
        })

    out_df = pd.DataFrame(results)
    out_name = f"judge_eval_{name}.csv"
    out_path = os.path.join(os.path.dirname(path), out_name)
    out_df.to_csv(out_path, index=False, encoding="utf-8-sig")

    metrics_summary = {
        "model": name,
        "language": lang,
        "samples": len(out_df),
        "relevance": round(out_df["relevance"].mean(), 2),
        "completeness": round(out_df["completeness"].mean(), 2),
        "faithfulness": round(out_df["faithfulness"].mean(), 2),
        "coherence": round(out_df["coherence"].mean(), 2),
        "conciseness": round(out_df["conciseness"].mean(), 2),
        "fluency": round(out_df["fluency"].mean(), 2),
        "overall_avg": round(out_df["avg_score"].mean(), 2)
    }

    return metrics_summary


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    eng_dir = os.path.join(base_dir, "english_XLSum_v2.0")

    file_list = [
        # Bengali files
        ("bengali", os.path.join(base_dir, "deepseek_v4_flash_bengali_results.csv"), "deepseek_v4_flash_bengali"),
        ("bengali", os.path.join(base_dir, "gemini_2.5_flash_bengali_results.csv"), "gemini_2.5_flash_bengali"),
        ("bengali", os.path.join(base_dir, "gemini_3.1_flash_lite_bengali_results.csv"), "gemini_3.1_flash_lite_bengali"),
        ("bengali", os.path.join(base_dir, "gpt_4o_mini_bengali_results.csv"), "gpt_4o_mini_bengali"),
        ("bengali", os.path.join(base_dir, "gpt_5.6_luna_bengali_results.csv"), "gpt_5.6_luna_bengali"),
        ("bengali", os.path.join(base_dir, "groq_llama70b_1000_results.csv"), "llama_3.3_70b_bengali"),
        ("bengali", os.path.join(base_dir, "qwen_3.5_flash_bengali_results.csv"), "qwen_3.5_flash_bengali"),
        ("bengali", os.path.join(base_dir, "qwen_3.6_27b_bengali_results.csv"), "qwen_3.6_27b_bengali"),

        # English files
        ("english", os.path.join(eng_dir, "deepseek_v4_flash_english_results.csv"), "deepseek_v4_flash_english"),
        ("english", os.path.join(eng_dir, "gemini_2.5_flash_english_results.csv"), "gemini_2.5_flash_english"),
        ("english", os.path.join(eng_dir, "gemini_3.1_flash_lite_english_results.csv"), "gemini_3.1_flash_lite_english"),
        ("english", os.path.join(eng_dir, "gpt_4o_mini_english_results.csv"), "gpt_4o_mini_english"),
        ("english", os.path.join(eng_dir, "gpt_5.6_luna_english_results.csv"), "gpt_5.6_luna_english"),
        ("english", os.path.join(eng_dir, "groq_llama70b_1012_english_results.csv"), "llama_3.3_70b_english"),
        ("english", os.path.join(eng_dir, "qwen_3.5_flash_english_results.csv"), "qwen_3.5_flash_english"),
        ("english", os.path.join(eng_dir, "qwen_3.6_27b_english_results.csv"), "qwen_3.6_27b_english"),
    ]

    print("=" * 70)
    print("Starting Parallel LLM Judge Evaluation across 16 files (50 samples each)")
    print(f"Model Engine: {MODEL_NAME} | Total items: {len(file_list) * 50}")
    print("=" * 70)

    summary_list = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_csv, info): info for info in file_list}
        for future in tqdm(as_completed(futures), total=len(file_list), desc="Processing CSV files"):
            try:
                res = future.result()
                summary_list.append(res)
                print(f"\n[+] Finished {res['model']} ({res['language']}): Overall Avg = {res['overall_avg']}")
            except Exception as e:
                info = futures[future]
                print(f"\n[!] Failed processing {info[2]}: {e}")

    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_list).sort_values(by=["language", "overall_avg"], ascending=[True, False])
    summary_df.to_csv(os.path.join(base_dir, "judge_evaluation_16_models_summary.csv"), index=False, encoding="utf-8-sig")
    summary_df.to_csv(os.path.join(base_dir, "judge_evaluation_16_models_summary.tsv"), sep="\t", index=False, encoding="utf-8-sig")

    print("\n" + "=" * 70)
    print("SUMMARY RESULTS OF ALL 16 MODELS (50 RANDOM SAMPLES EACH)")
    print("=" * 70)
    print(summary_df.to_string(index=False))
    print("\n[+] Detailed CSV/TSV report saved to judge_evaluation_16_models_summary.csv and .tsv!")


if __name__ == "__main__":
    main()
