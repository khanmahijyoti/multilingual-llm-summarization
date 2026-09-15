"""
LLM-as-a-Judge Evaluation Script
=================================
Uses GPT-4o-mini to evaluate summaries on 5 criteria (1-5 scale):
  - Relevance, Completeness, Redundancy, Coherence, Hallucinations

Reads CSV files with columns: id, reference, generated, rouge1, rouge2, rougeL
Outputs: judge scores per row, per file, and a combined comparison.

Usage:
  python llm_judge_evaluate.py --lang bengali
  python llm_judge_evaluate.py --lang english
  python llm_judge_evaluate.py --lang both
"""

import sys
import os
import csv
import json
import time
import argparse
import urllib.request
import urllib.error
import glob
import traceback

# Force console output to use UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# ─── CONFIG ───────────────────────────────────────────────────────────────
JUDGE_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.0
MAX_TOKENS = 300

# Load OpenAI keys from the api keys file
def load_openai_keys():
    keys = []
    keys_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api keys")
    if os.path.exists(keys_file):
        with open(keys_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("sk-") and not line.startswith("sk-or-"):
                    keys.append(line)
    if not keys:
        raise ValueError("No OpenAI API keys found in 'api keys' file")
    print(f"Loaded {len(keys)} OpenAI keys")
    return keys

openai_keys = []
current_key_idx = 0

# ─── JUDGE PROMPT ─────────────────────────────────────────────────────────

JUDGE_SYSTEM_PROMPT = """You are an expert summary evaluator. Given a source text (reference) and a generated summary, evaluate the summary on these 5 criteria using a 1-5 scale.

Criteria:
1. Relevance (1-5): Does the summary capture the key information from the source? 
   1=completely irrelevant, 5=perfectly captures the core message
2. Completeness (1-5): Does the summary include all important facts from the source?
   1=missing most key facts, 5=all important facts present
3. Redundancy (1-5): Does the summary avoid unnecessary repetition and filler?
   1=very redundant, 5=concise with no redundancy
4. Coherence (1-5): Is the summary logically structured and easy to read?
   1=incoherent, 5=perfectly structured and clear
5. Hallucinations (1-5): Does the summary avoid fabricating information not in the source?
   1=contains major fabrications, 5=completely faithful to source

You MUST respond with ONLY a valid JSON object in this exact format, nothing else:
{"relevance": X, "completeness": X, "redundancy": X, "coherence": X, "hallucinations": X}

Replace X with integer scores from 1 to 5. No explanations, no markdown, no extra text."""

JUDGE_USER_TEMPLATE = """Source Text:
{reference}

Generated Summary:
{generated}

Rate the generated summary against the source text."""

# ─── API CALL ─────────────────────────────────────────────────────────────

def call_openai_api(prompt, system_prompt, api_key, timeout=60):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": JUDGE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_json = json.loads(response.read().decode('utf-8'))
        if 'choices' not in res_json:
            if 'error' in res_json:
                raise RuntimeError(f"API Error: {res_json['error']['message']}")
            raise RuntimeError(f"Unexpected response: {res_json}")
        return res_json['choices'][0]['message']['content'].strip()


def call_with_rotation(prompt, system_prompt, max_retries=5):
    global current_key_idx
    
    for attempt in range(max_retries):
        api_key = openai_keys[current_key_idx]
        try:
            return call_openai_api(prompt, system_prompt, api_key)
        except urllib.error.HTTPError as e:
            err_code = e.code
            try:
                err_body = e.read().decode('utf-8')
            except Exception:
                err_body = ""
            
            if err_code == 429:
                # Rate limited - rotate key
                current_key_idx = (current_key_idx + 1) % len(openai_keys)
                wait = min(2 ** attempt, 30)
                print(f"      Rate limited, rotating to key {current_key_idx}, waiting {wait}s...")
                time.sleep(wait)
            elif err_code == 401:
                # Invalid key - skip it
                print(f"      Key {current_key_idx} invalid, rotating...")
                current_key_idx = (current_key_idx + 1) % len(openai_keys)
                time.sleep(1)
            else:
                print(f"      HTTP {err_code}: {err_body[:200]}")
                time.sleep(2)
        except urllib.error.URLError as e:
            print(f"      Network error: {e}, retrying in {2 ** attempt}s...")
            time.sleep(min(2 ** attempt, 30))
        except Exception as e:
            print(f"      Error: {e}, retrying...")
            time.sleep(2)
    
    raise RuntimeError(f"All {max_retries} attempts failed")


def parse_judge_response(response_text):
    """Parse the JSON response from the judge, handling common malformations."""
    text = response_text.strip()
    
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (``` markers)
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    
    try:
        scores = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from the response
        import re
        match = re.search(r'\{[^}]+\}', text)
        if match:
            try:
                scores = json.loads(match.group())
            except json.JSONDecodeError:
                return None
        else:
            return None
    
    # Validate all keys present and values in range
    required = ["relevance", "completeness", "redundancy", "coherence", "hallucinations"]
    for key in required:
        if key not in scores:
            return None
        val = scores[key]
        if not isinstance(val, (int, float)) or val < 1 or val > 5:
            scores[key] = max(1, min(5, int(round(val)))) if isinstance(val, (int, float)) else 3
    
    return scores


def judge_single(reference, generated):
    """Judge a single reference-summary pair. Returns dict of scores."""
    prompt = JUDGE_USER_TEMPLATE.format(reference=reference, generated=generated)
    
    for attempt in range(3):
        response = call_with_rotation(prompt, JUDGE_SYSTEM_PROMPT)
        scores = parse_judge_response(response)
        if scores:
            return scores
        print(f"      Failed to parse response (attempt {attempt+1}): {response[:100]}")
        time.sleep(1)
    
    # Fallback - return None to indicate failure
    return None


# ─── FILE PROCESSING ──────────────────────────────────────────────────────

def get_csv_files(lang):
    """Get list of summary CSV files to process."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = []
    
    if lang in ("bengali", "both"):
        bengali_dir = base_dir
        patterns = [
            "deepseek_v4_flash_bengali_results.csv",
            "gemini_2.5_flash_bengali_results.csv",
            "gemini_3.1_flash_lite_bengali_results.csv",
            "gpt_4o_mini_bengali_results.csv",
            "gpt_5.6_luna_bengali_results.csv",
            "groq_llama70b_1000_results.csv",
            "qwen_3.5_flash_bengali_results.csv",
            "qwen_3.6_27b_bengali_results.csv",
        ]
        for p in patterns:
            full = os.path.join(bengali_dir, p)
            if os.path.exists(full):
                files.append(("bengali", full))
    
    if lang in ("english", "both"):
        english_dir = os.path.join(base_dir, "english_XLSum_v2.0")
        patterns = [
            "deepseek_v4_flash_english_results.csv",
            "gemini_2.5_flash_english_results.csv",
            "gemini_3.1_flash_lite_english_results.csv",
            "gpt_4o_mini_english_results.csv",
            "gpt_5.6_luna_english_results.csv",
            "groq_llama70b_1012_english_results.csv",
            "qwen_3.5_flash_english_results.csv",
            "qwen_3.6_27b_english_results.csv",
        ]
        for p in patterns:
            full = os.path.join(english_dir, p)
            if os.path.exists(full):
                files.append(("english", full))
    
    return files


def get_output_path(input_path):
    """Generate output filename for judge results."""
    dirname = os.path.dirname(input_path)
    basename = os.path.basename(input_path)
    name, ext = os.path.splitext(basename)
    return os.path.join(dirname, f"{name}_judge_scores{ext}")


def count_existing_rows(output_path):
    """Count how many rows have already been processed (for resume)."""
    if not os.path.exists(output_path):
        return 0
    count = 0
    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for _ in reader:
            count += 1
    return count


def process_file(lang, input_path):
    """Process a single CSV file with LLM judge."""
    output_path = get_output_path(input_path)
    model_name = os.path.basename(input_path).replace("_results.csv", "").replace(f"_{lang}", "")
    
    # Read input
    rows = []
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    
    total = len(rows)
    
    # Check for resume
    already_done = count_existing_rows(output_path)
    if already_done >= total:
        print(f"  ✅ Already complete ({already_done}/{total})")
        return output_path
    
    if already_done > 0:
        print(f"  ⏩ Resuming from row {already_done + 1}/{total}")
    
    # Open output file for writing/appending
    write_header = (already_done == 0)
    out_fields = ["id", "reference", "generated", "rouge1", "rouge2", "rougeL",
                   "judge_relevance", "judge_completeness", "judge_redundancy",
                   "judge_coherence", "judge_hallucinations", "judge_avg"]
    
    mode = 'w' if write_header else 'a'
    outf = open(output_path, mode, newline='', encoding='utf-8')
    writer = csv.DictWriter(outf, fieldnames=out_fields)
    if write_header:
        writer.writeheader()
    
    successes = 0
    failures = 0
    start_time = time.time()
    
    try:
        for i, row in enumerate(rows):
            if i < already_done:
                continue
            
            row_id = row.get('id', row.get('\ufeffid', str(i)))
            reference = row.get('reference', '')
            generated = row.get('generated', '')
            
            if not reference or not generated:
                print(f"  [{i+1}/{total}] Skipping empty row {row_id}")
                failures += 1
                continue
            
            # Truncate very long texts to save tokens
            ref_truncated = reference[:2000] if len(reference) > 2000 else reference
            gen_truncated = generated[:2000] if len(generated) > 2000 else generated
            
            try:
                scores = judge_single(ref_truncated, gen_truncated)
            except Exception as e:
                print(f"  [{i+1}/{total}] ❌ Error judging {row_id}: {e}")
                scores = None
                failures += 1
            
            if scores:
                avg = sum(scores.values()) / len(scores)
                out_row = {
                    "id": row_id,
                    "reference": reference,
                    "generated": generated,
                    "rouge1": row.get('rouge1', ''),
                    "rouge2": row.get('rouge2', ''),
                    "rougeL": row.get('rougeL', ''),
                    "judge_relevance": scores["relevance"],
                    "judge_completeness": scores["completeness"],
                    "judge_redundancy": scores["redundancy"],
                    "judge_coherence": scores["coherence"],
                    "judge_hallucinations": scores["hallucinations"],
                    "judge_avg": round(avg, 2),
                }
                writer.writerow(out_row)
                outf.flush()
                successes += 1
                
                if (i + 1) % 50 == 0:
                    elapsed = time.time() - start_time
                    rate = (i + 1 - already_done) / elapsed * 60
                    remaining = (total - i - 1) / (rate / 60) if rate > 0 else 0
                    print(f"  [{i+1}/{total}] ✅ avg={avg:.1f} | {rate:.0f} rows/min | ~{remaining/60:.1f}h remaining")
            else:
                # Write row with empty scores so we don't re-process
                out_row = {
                    "id": row_id,
                    "reference": reference,
                    "generated": generated,
                    "rouge1": row.get('rouge1', ''),
                    "rouge2": row.get('rouge2', ''),
                    "rougeL": row.get('rougeL', ''),
                    "judge_relevance": "",
                    "judge_completeness": "",
                    "judge_redundancy": "",
                    "judge_coherence": "",
                    "judge_hallucinations": "",
                    "judge_avg": "",
                }
                writer.writerow(out_row)
                outf.flush()
                failures += 1
            
            # Small delay to avoid rate limits
            time.sleep(0.1)
    
    finally:
        outf.close()
    
    elapsed = time.time() - start_time
    print(f"  ✅ Done: {successes} scored, {failures} failed in {elapsed/60:.1f}min")
    print(f"     Output: {output_path}")
    return output_path


def generate_comparison(output_files, lang):
    """Generate a comparison TSV across all models."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    comparison_path = os.path.join(base_dir, f"llm_judge_{lang}_comparison.tsv")
    
    results = []
    
    for path in output_files:
        model_name = os.path.basename(path).replace("_judge_scores.csv", "").replace("_results", "")
        
        scores = {"relevance": [], "completeness": [], "redundancy": [], 
                   "coherence": [], "hallucinations": [], "avg": []}
        
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for key in scores:
                    val = row.get(f"judge_{key}", "")
                    if val:
                        try:
                            scores[key].append(float(val))
                        except ValueError:
                            pass
        
        if scores["avg"]:
            results.append({
                "model": model_name,
                "relevance": sum(scores["relevance"]) / len(scores["relevance"]) if scores["relevance"] else 0,
                "completeness": sum(scores["completeness"]) / len(scores["completeness"]) if scores["completeness"] else 0,
                "redundancy": sum(scores["redundancy"]) / len(scores["redundancy"]) if scores["redundancy"] else 0,
                "coherence": sum(scores["coherence"]) / len(scores["coherence"]) if scores["coherence"] else 0,
                "hallucinations": sum(scores["hallucinations"]) / len(scores["hallucinations"]) if scores["hallucinations"] else 0,
                "avg": sum(scores["avg"]) / len(scores["avg"]) if scores["avg"] else 0,
                "n": len(scores["avg"]),
            })
    
    # Sort by average score descending
    results.sort(key=lambda x: x["avg"], reverse=True)
    
    with open(comparison_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["model", "relevance", "completeness", "redundancy", 
                                                 "coherence", "hallucinations", "avg", "n"],
                                 delimiter='\t')
        writer.writeheader()
        for r in results:
            writer.writerow({
                "model": r["model"],
                "relevance": f"{r['relevance']:.2f}",
                "completeness": f"{r['completeness']:.2f}",
                "redundancy": f"{r['redundancy']:.2f}",
                "coherence": f"{r['coherence']:.2f}",
                "hallucinations": f"{r['hallucinations']:.2f}",
                "avg": f"{r['avg']:.2f}",
                "n": r["n"],
            })
    
    print(f"\n{'='*70}")
    print(f"COMPARISON RESULTS ({lang.upper()})")
    print(f"{'='*70}")
    print(f"{'Model':<40} {'Rel':>5} {'Comp':>5} {'Red':>5} {'Coh':>5} {'Hall':>5} {'AVG':>5}")
    print("-" * 70)
    for r in results:
        print(f"{r['model']:<40} {r['relevance']:>5.2f} {r['completeness']:>5.2f} "
              f"{r['redundancy']:>5.2f} {r['coherence']:>5.2f} {r['hallucinations']:>5.2f} {r['avg']:>5.2f}")
    print(f"\nSaved to: {comparison_path}")
    return comparison_path


# ─── MAIN ─────────────────────────────────────────────────────────────────

def main():
    global openai_keys
    
    parser = argparse.ArgumentParser(description="LLM-as-a-Judge evaluation")
    parser.add_argument("--lang", choices=["bengali", "english", "both"], default="both",
                        help="Which language CSVs to evaluate")
    args = parser.parse_args()
    
    print("=" * 60)
    print("LLM-as-a-Judge Evaluation")
    print(f"Judge Model: {JUDGE_MODEL}")
    print(f"Language: {args.lang}")
    print("=" * 60)
    
    # Load keys
    openai_keys = load_openai_keys()
    
    # Get files
    files = get_csv_files(args.lang)
    if not files:
        print("No CSV files found!")
        return
    
    print(f"\nFound {len(files)} CSV files to process:")
    for lang, path in files:
        print(f"  [{lang}] {os.path.basename(path)}")
    print()
    
    # Process each file
    output_files_by_lang = {}
    total_start = time.time()
    
    for idx, (lang, path) in enumerate(files):
        print(f"\n[{idx+1}/{len(files)}] Processing: {os.path.basename(path)} ({lang})")
        print("-" * 50)
        
        try:
            output_path = process_file(lang, path)
            if lang not in output_files_by_lang:
                output_files_by_lang[lang] = []
            output_files_by_lang[lang].append(output_path)
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            traceback.print_exc()
    
    # Generate comparisons
    for lang, output_files in output_files_by_lang.items():
        if output_files:
            generate_comparison(output_files, lang)
    
    # Combined comparison if both languages
    if len(output_files_by_lang) > 1:
        all_files = []
        for files_list in output_files_by_lang.values():
            all_files.extend(files_list)
        generate_comparison(all_files, "combined")
    
    total_elapsed = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"TOTAL TIME: {total_elapsed/60:.1f} minutes ({total_elapsed/3600:.1f} hours)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
