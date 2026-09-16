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
    
    # 5,000 bootstrap resamples for 95% Confidence Interval
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

def paired_test(data1, data2, B=5000, seed=42):
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
    
    # Normal approximation asymptotic p-value
    z = abs(t_stat)
    p_val_approx = math.erfc(z / math.sqrt(2))
    
    # Bootstrap paired p-value with 5,000 resamples under null hypothesis
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
        'p_val': p_val_approx,
        'boot_p': boot_p
    }

if __name__ == '__main__':
    print("="*80)
    print("STATISTICAL EVALUATION SUITE (5,000 Bootstrap Resamples, Seed=42)")
    print("="*80)

    # 1. Bengali Factuality
    print("\n1. BENGALI FACTUALITY (BanglaSummEval BSE-F1)")
    print("-" * 80)
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
    bn_fact_data = {}
    for m, f in bn_fact_models.items():
        d = load_csv_column(f, 'banglasummeval_f1')
        bn_fact_data[m] = d
        st = calc_stats(list(d.values()))
        print(f"{m:22s} | N={st['n']:4d} | Mean={st['mean']:5.2f}% | SD={st['std']:5.2f} | 95% CI: [{st['boot_low']:5.2f}, {st['boot_high']:5.2f}]")

    print("\n--- Paired Test: Gemini 2.5 Flash vs LLaMA 3.3 70B ---")
    res = paired_test(bn_fact_data['Gemini 2.5 Flash'], bn_fact_data['LLaMA 3.3 70B'])
    if res:
        sig_str = "Statistically significant" if res['boot_p'] < 0.05 else "The difference is not statistically significant"
        print(f"Paired N={res['n']}, Mean Diff={res['mean_diff']:+.2f}%, t={res['t_stat']:.3f}, p={res['p_val']:.4f}, bootstrap_p={res['boot_p']:.4f}")
        print(f">> Finding: {sig_str}")

    # 2. English Factuality
    print("\n" + "="*80)
    print("2. ENGLISH FACTUALITY (SummEval SE-F1)")
    print("-" * 80)
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
    en_fact_data = {}
    for m, f in en_fact_models.items():
        d = load_csv_column(f, 'summeval_f1')
        en_fact_data[m] = d
        st = calc_stats(list(d.values()))
        print(f"{m:22s} | N={st['n']:4d} | Mean={st['mean']:5.2f}% | SD={st['std']:5.2f} | 95% CI: [{st['boot_low']:5.2f}, {st['boot_high']:5.2f}]")

    print("\n--- Paired Test: DeepSeek V4 Flash vs LLaMA 3.3 70B ---")
    res_en = paired_test(en_fact_data['DeepSeek V4 Flash'], en_fact_data['LLaMA 3.3 70B'])
    if res_en:
        sig_str = "Statistically significant" if res_en['boot_p'] < 0.05 else "The difference is not statistically significant"
        print(f"Paired N={res_en['n']}, Mean Diff={res_en['mean_diff']:+.2f}%, t={res_en['t_stat']:.3f}, p={res_en['p_val']:.4f}, bootstrap_p={res_en['boot_p']:.4f}")
        print(f">> Finding: {sig_str}")

    # 3. Bengali ROUGE-1
    print("\n" + "="*80)
    print("3. BENGALI ROUGE-1")
    print("-" * 80)
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
    bn_r1_data = {}
    for m, f in bn_rouge_models.items():
        d = load_csv_column(f, 'rouge1')
        bn_r1_data[m] = d
        st = calc_stats(list(d.values()))
        print(f"{m:22s} | N={st['n']:4d} | Mean={st['mean']:5.2f}% | SD={st['std']:5.2f} | 95% CI: [{st['boot_low']:5.2f}, {st['boot_high']:5.2f}]")

    print("\n--- Paired Test: LLaMA 3.3 70B vs GPT-4o Mini ---")
    res_bn_r1 = paired_test(bn_r1_data['LLaMA 3.3 70B'], bn_r1_data['GPT-4o Mini'])
    if res_bn_r1:
        sig_str = "Statistically significant" if res_bn_r1['boot_p'] < 0.05 else "The difference is not statistically significant"
        print(f"Paired N={res_bn_r1['n']}, Mean Diff={res_bn_r1['mean_diff']:+.2f}%, t={res_bn_r1['t_stat']:.3f}, p={res_bn_r1['p_val']:.4f}, bootstrap_p={res_bn_r1['boot_p']:.4f}")
        print(f">> Finding: {sig_str}")

    print("\n--- Paired Test: LLaMA 3.3 70B vs Gemini 2.5 Flash ---")
    res_bn_r1_gem = paired_test(bn_r1_data['LLaMA 3.3 70B'], bn_r1_data['Gemini 2.5 Flash'])
    if res_bn_r1_gem:
        sig_str = "Statistically significant" if res_bn_r1_gem['boot_p'] < 0.05 else "The difference is not statistically significant"
        print(f"Paired N={res_bn_r1_gem['n']}, Mean Diff={res_bn_r1_gem['mean_diff']:+.2f}%, t={res_bn_r1_gem['t_stat']:.3f}, p={res_bn_r1_gem['p_val']:.4e}, bootstrap_p={res_bn_r1_gem['boot_p']:.4f}")
        print(f">> Finding: {sig_str}")

    # 4. English ROUGE-1
    print("\n" + "="*80)
    print("4. ENGLISH ROUGE-1")
    print("-" * 80)
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
    en_r1_data = {}
    for m, f in en_rouge_models.items():
        d = load_csv_column(f, 'rouge1')
        en_r1_data[m] = d
        st = calc_stats(list(d.values()))
        print(f"{m:22s} | N={st['n']:4d} | Mean={st['mean']:5.2f}% | SD={st['std']:5.2f} | 95% CI: [{st['boot_low']:5.2f}, {st['boot_high']:5.2f}]")

    print("\n--- Paired Test: GPT-5.6 Luna vs Gemini 3.1 Flash Lite ---")
    res_en_r1 = paired_test(en_r1_data['GPT-5.6 Luna'], en_r1_data['Gemini 3.1 Flash Lite'])
    if res_en_r1:
        sig_str = "Statistically significant" if res_en_r1['boot_p'] < 0.05 else "The difference is not statistically significant"
        print(f"Paired N={res_en_r1['n']}, Mean Diff={res_en_r1['mean_diff']:+.2f}%, t={res_en_r1['t_stat']:.3f}, p={res_en_r1['p_val']:.4e}, bootstrap_p={res_en_r1['boot_p']:.4f}")
        print(f">> Finding: {sig_str}")
