import csv
import math
import random
import os

def load_csv_column(filepath, col_name, id_col='id'):
    data = {}
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found")
        return data
    with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row.get(id_col, '').strip()
            if not item_id:
                for k in row.keys():
                    if k and k.strip().lstrip('\ufeff') == id_col:
                        item_id = row[k].strip()
                        break
            val_str = row.get(col_name, '').strip()
            if not val_str:
                for k in row.keys():
                    if k and k.strip().lstrip('\ufeff').lower() == col_name.lower():
                        val_str = row[k].strip()
                        break
            if not item_id or not val_str:
                continue
            try:
                val = float(val_str)
                data[item_id] = val
            except ValueError:
                continue
    return data

def calc_stats(values, B=5000, seed=42):
    n = len(values)
    if n == 0:
        return {'mean': 0, 'std': 0, 'se': 0, 'boot_low': 0, 'boot_high': 0, 'n': 0}
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0
    std = math.sqrt(var)
    se = std / math.sqrt(n)
    
    # 5,000 bootstrap resamples
    random.seed(seed)
    val_list = list(values)
    boot_means = []
    for _ in range(B):
        sample = [val_list[random.randint(0, n - 1)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    boot_low = boot_means[int(0.025 * B)]
    boot_high = boot_means[int(0.975 * B)]

    return {
        'mean': mean,
        'std': std,
        'se': se,
        'boot_low': boot_low,
        'boot_high': boot_high,
        'n': n
    }

def paired_comparison(data1, data2, B=5000, seed=42):
    common_ids = sorted(list(set(data1.keys()) & set(data2.keys())))
    n = len(common_ids)
    if n < 2:
        return None
    diffs = [data1[k] - data2[k] for k in common_ids]
    mean_diff = sum(diffs) / n
    var_diff = sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)
    std_diff = math.sqrt(var_diff)
    se_diff = std_diff / math.sqrt(n)
    t_stat = mean_diff / se_diff if se_diff > 0 else 0
    
    # Standard normal / large-sample asymptotic two-tailed p-value
    # (or Student-t with df = n-1)
    z = abs(t_stat)
    p_val = math.erfc(z / math.sqrt(2))
    
    # Bootstrap paired p-value with B=5,000 resamples under null hypothesis
    random.seed(seed)
    count_exceed = 0
    for _ in range(B):
        sample_sum = 0
        for d in diffs:
            if random.random() < 0.5:
                sample_sum += (d - mean_diff)
            else:
                sample_sum -= (d - mean_diff)
        b_mean = sample_sum / n
        if abs(b_mean) >= abs(mean_diff):
            count_exceed += 1
    boot_p = count_exceed / B

    return {
        'n': n,
        'mean_diff': mean_diff,
        'std_diff': std_diff,
        'se_diff': se_diff,
        't_stat': t_stat,
        'p_val': p_val,
        'boot_p': boot_p
    }

# Load datasets
bn_fact_models = {
    'Gemini 2.5 Flash': os.path.join('results', 'bengali', 'banglasummeval_gemini_2.5_flash_results.csv'),
    'LLaMA 3.3 70B': os.path.join('results', 'bengali', 'banglasummeval_groq_llama70b_1000_results.csv'),
    'DeepSeek V4 Flash': os.path.join('results', 'bengali', 'banglasummeval_deepseek_v4_flash_results.csv'),
    'GPT-4o Mini': os.path.join('results', 'bengali', 'banglasummeval_gpt_4o_mini_results.csv'),
    'Qwen 3.6 27B': os.path.join('results', 'bengali', 'banglasummeval_qwen_3.6_27b_results.csv'),
    'Qwen 3.5 Flash': os.path.join('results', 'bengali', 'banglasummeval_qwen_3.5_flash_results.csv'),
    'GPT-5.6 Luna': os.path.join('results', 'bengali', 'banglasummeval_gpt_5.6_luna_results.csv'),
    'Gemini 3.1 Flash Lite': os.path.join('results', 'bengali', 'banglasummeval_gemini_3.1_flash_lite_results.csv'),
}
bn_fact_data = {m: load_csv_column(f, 'banglasummeval_f1') for m, f in bn_fact_models.items()}

en_fact_models = {
    'DeepSeek V4 Flash': os.path.join('results', 'english', 'summeval_gpt_4o_deepseek_v4_flash_english_results.csv'),
    'LLaMA 3.3 70B': os.path.join('results', 'english', 'summeval_gpt_4o_groq_llama70b_1012_english_results.csv'),
    'GPT-4o Mini': os.path.join('results', 'english', 'summeval_gpt_4o_gpt_4o_mini_english_results.csv'),
    'Gemini 2.5 Flash': os.path.join('results', 'english', 'summeval_gpt_4o_gemini_2.5_flash_english_results.csv'),
    'Qwen 3.5 Flash': os.path.join('results', 'english', 'summeval_gpt_4o_qwen_3.5_flash_english_results.csv'),
    'GPT-5.6 Luna': os.path.join('results', 'english', 'summeval_gpt_4o_gpt_5.6_luna_english_results.csv'),
    'Qwen 3.6 27B': os.path.join('results', 'english', 'summeval_gpt_4o_qwen_3.6_27b_english_results.csv'),
    'Gemini 3.1 Flash Lite': os.path.join('results', 'english', 'summeval_gpt_4o_gemini_3.1_flash_lite_english_results.csv'),
}
en_fact_data = {m: load_csv_column(f, 'summeval_f1') for m, f in en_fact_models.items()}

bn_rouge_models = {
    'LLaMA 3.3 70B': os.path.join('results', 'bengali', 'groq_llama70b_1000_results.csv'),
    'GPT-4o Mini': os.path.join('results', 'bengali', 'gpt_4o_mini_bengali_results.csv'),
    'Gemini 2.5 Flash': os.path.join('results', 'bengali', 'gemini_2.5_flash_bengali_results.csv'),
    'DeepSeek V4 Flash': os.path.join('results', 'bengali', 'deepseek_v4_flash_bengali_results.csv'),
    'Qwen 3.5 Flash': os.path.join('results', 'bengali', 'qwen_3.5_flash_bengali_results.csv'),
    'Gemini 3.1 Flash Lite': os.path.join('results', 'bengali', 'gemini_3.1_flash_lite_bengali_results.csv'),
    'GPT-5.6 Luna': os.path.join('results', 'bengali', 'gpt_5.6_luna_bengali_results.csv'),
    'Qwen 3.6 27B': os.path.join('results', 'bengali', 'qwen_3.6_27b_bengali_results.csv'),
}
bn_r1_data = {m: load_csv_column(f, 'rouge1') for m, f in bn_rouge_models.items()}

en_rouge_dir = os.path.join('results', 'english')
en_rouge_models = {
    'GPT-5.6 Luna': os.path.join(en_rouge_dir, 'gpt_5.6_luna_english_results.csv'),
    'Gemini 3.1 Flash Lite': os.path.join(en_rouge_dir, 'gemini_3.1_flash_lite_english_results.csv'),
    'Gemini 2.5 Flash': os.path.join(en_rouge_dir, 'gemini_2.5_flash_english_results.csv'),
    'Qwen 3.5 Flash': os.path.join(en_rouge_dir, 'qwen_3.5_flash_english_results.csv'),
    'Qwen 3.6 27B': os.path.join(en_rouge_dir, 'qwen_3.6_27b_english_results.csv'),
    'DeepSeek V4 Flash': os.path.join(en_rouge_dir, 'deepseek_v4_flash_english_results.csv'),
    'GPT-4o Mini': os.path.join(en_rouge_dir, 'gpt_4o_mini_english_results.csv'),
    'LLaMA 3.3 70B': os.path.join(en_rouge_dir, 'groq_llama70b_1012_english_results.csv'),
}
en_r1_data = {m: load_csv_column(f, 'rouge1') for m, f in en_rouge_models.items()}

comparisons = [
    ("Bengali Factuality (BSE-F1)", "Gemini 2.5 Flash", bn_fact_data['Gemini 2.5 Flash'], "LLaMA 3.3 70B", bn_fact_data['LLaMA 3.3 70B']),
    ("English Factuality (SE-F1)", "DeepSeek V4 Flash", en_fact_data['DeepSeek V4 Flash'], "LLaMA 3.3 70B", en_fact_data['LLaMA 3.3 70B']),
    ("Bengali ROUGE-1", "LLaMA 3.3 70B", bn_r1_data['LLaMA 3.3 70B'], "GPT-4o Mini", bn_r1_data['GPT-4o Mini']),
    ("Bengali ROUGE-1", "LLaMA 3.3 70B", bn_r1_data['LLaMA 3.3 70B'], "Gemini 2.5 Flash", bn_r1_data['Gemini 2.5 Flash']),
    ("English ROUGE-1", "GPT-5.6 Luna", en_r1_data['GPT-5.6 Luna'], "Gemini 3.1 Flash Lite", en_r1_data['Gemini 3.1 Flash Lite']),
]

print("\n### FULL CONSISTENT STATISTICAL SUMMARY ###\n")
for comp_name, m1_name, d1, m2_name, d2 in comparisons:
    st1 = calc_stats(list(d1.values()), B=5000)
    st2 = calc_stats(list(d2.values()), B=5000)
    res = paired_comparison(d1, d2, B=5000)
    
    is_sig = res['boot_p'] < 0.05
    sig_text = "Statistically significant" if is_sig else "The difference is not statistically significant"
    
    print(f"Comparison: {comp_name} — {m1_name} vs. {m2_name}")
    print(f"  - {m1_name}: Mean = {st1['mean']:.2f}%, SD = {st1['std']:.2f}, 95% CI: [{st1['boot_low']:.2f}, {st1['boot_high']:.2f}] (N = {st1['n']})")
    print(f"  - {m2_name}: Mean = {st2['mean']:.2f}%, SD = {st2['std']:.2f}, 95% CI: [{st2['boot_low']:.2f}, {st2['boot_high']:.2f}] (N = {st2['n']})")
    print(f"  - Mean Difference: {res['mean_diff']:+.2f}%")
    print(f"  - Paired Test Statistic: t = {res['t_stat']:.3f} (N = {res['n']})")
    if res['p_val'] < 0.0001:
        p_str = f"p < 0.0001 (p = {res['p_val']:.2e})"
    else:
        p_str = f"p = {res['p_val']:.4f}"
    if res['boot_p'] < 0.0001:
        boot_p_str = f"p < 0.0001 (bootstrap p = {res['boot_p']:.4f})"
    else:
        boot_p_str = f"bootstrap p = {res['boot_p']:.4f}"
    print(f"  - Paired-test p-value: {p_str}")
    print(f"  - Bootstrap p-value (5,000 resamples): {boot_p_str}")
    print(f"  - Result: {sig_text}")
    print()
