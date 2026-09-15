import csv
import math
import random
import os

def load_csv_column(filepath, col_name, id_col='id'):
    data = {}
    if not os.path.exists(filepath):
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
                data[item_id] = float(val_str)
            except ValueError:
                continue
    return data

def calc_stats(values, B=1000):
    n = len(values)
    if n == 0:
        return {'mean': 0, 'std': 0, 'se': 0, 'boot_low': 0, 'boot_high': 0, 'n': 0}
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0
    std = math.sqrt(var)
    se = std / math.sqrt(n)
    
    random.seed(42)
    boot_means = []
    val_list = list(values)
    for _ in range(B):
        sample = [val_list[random.randint(0, n - 1)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    boot_low = boot_means[int(0.025 * B)]
    boot_high = boot_means[int(0.975 * B)]

    return {'mean': mean, 'std': std, 'se': se, 'boot_low': boot_low, 'boot_high': boot_high, 'n': n}

def paired_test(data1, data2):
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
    z = abs(t_stat)
    p_val = math.erfc(z / math.sqrt(2))
    return {'n': n, 'mean_diff': mean_diff, 'std_diff': std_diff, 'se_diff': se_diff, 't_stat': t_stat, 'p_val': p_val}

print("Running all metric summaries...")
# Print summary for all ROUGE and Factuality metrics
