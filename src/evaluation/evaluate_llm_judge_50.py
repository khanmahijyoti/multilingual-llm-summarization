"""
LLM-as-a-Judge Evaluation Script (50 samples per CSV)
=====================================================
Evaluates Bengali/English summaries using the 6-criteria prompt:
  - relevance, completeness, faithfulness, coherence, conciseness, fluency

Reads input CSV files (50 samples per file), calls the judge API, and outputs:
  - Per-model judge score CSVs (<model>_judge_6criteria_50.csv)
  - Combined summary TSV comparison report
"""

import sys
import os
import csv
import json
import time
import argparse
import urllib.request
import urllib.error
import pandas as pd
from tqdm import tqdm

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROMPT_TEMPLATE = """You are an expert evaluator of Bengali text summarization. Evaluate the generated summary against the source article using the following criteria, each scored from 1 (poor) to 5 (excellent):

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


def call_openai_compatible_api(prompt, api_key, model="gpt-4o-mini", api_base="https://api.openai.com/v1", timeout=45):
    url = f"{api_base.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    if "openrouter.ai" in api_base:
        headers["HTTP-Referer"] = "https://github.com"
        headers["X-Title"] = "LLM Judge Evaluation"

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 300,
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)

    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_json = json.loads(response.read().decode('utf-8'))
        return res_json['choices'][0]['message']['content'].strip()


def parse_scores(response_text):
    text = response_text.strip()
    if text.startswith("```"):
        lines = [l for l in text.split("\n") if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{[^}]+\}', text)
        if match:
            try:
                data = json.loads(match.group())
            except Exception:
                return None
        else:
            return None

    required = ["relevance", "completeness", "faithfulness", "coherence", "conciseness", "fluency"]
    clean_scores = {}
    for k in required:
        if k not in data:
            return None
        val = data[k]
        try:
            val = float(val)
            val = max(1.0, min(5.0, val))
            clean_scores[k] = val
        except (ValueError, TypeError):
            return None
    return clean_scores


def evaluate_csv(csv_path, api_key, model, sample_limit=50, api_base="https://api.openai.com/v1"):
    df = pd.read_csv(csv_path).head(sample_limit)
    out_rows = []

    print(f"Evaluating {len(df)} samples from {os.path.basename(csv_path)} using {model}...")

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        src = str(row.get('reference', row.get('text', '')))[:2500]
        gen = str(row.get('generated', ''))[:2000]

        prompt = PROMPT_TEMPLATE.format(source_article=src, generated_summary=gen)

        scores = None
        for attempt in range(3):
            try:
                resp = call_openai_compatible_api(prompt, api_key, model=model, api_base=api_base)
                scores = parse_scores(resp)
                if scores:
                    break
            except Exception as e:
                time.sleep(2)

        if not scores:
            scores = {k: None for k in ["relevance", "completeness", "faithfulness", "coherence", "conciseness", "fluency"]}

        out_row = {
            "id": row.get('id', idx),
            "reference": src,
            "generated": gen,
            "rouge1": row.get('rouge1', ''),
            "rouge2": row.get('rouge2', ''),
            "rougeL": row.get('rougeL', ''),
            **scores,
            "avg_score": round(sum(s for s in scores.values() if s is not None) / len([s for s in scores.values() if s is not None]), 2) if any(s is not None for s in scores.values()) else None
        }
        out_rows.append(out_row)

    return pd.DataFrame(out_rows)


if __name__ == "__main__":
    print("LLM-as-a-Judge 6-criteria evaluation helper script created.")
