import json
import csv

# We want to find representative error samples in Bengali summaries
# Reviewer 2 asked for:
# "representative examples of factual errors, omissions, mistranslations, and stylistic problems"

samples_to_inspect = ['140427_pg_bd_heat_dhaka_ac', 'news-54239981', 'news-39844487']

# Load source documents
sources = {}
with open('bengali_test.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)
        if item.get('id') in samples_to_inspect:
            sources[item['id']] = item

models = [
    ('LLaMA 3.3 70B', 'groq_llama70b_1000_results.csv'),
    ('Gemini 2.5 Flash', 'gemini_2.5_flash_bengali_results.csv'),
    ('Gemini 3.1 Flash Lite', 'gemini_3.1_flash_lite_bengali_results.csv'),
    ('GPT-4o Mini', 'gpt_4o_mini_bengali_results.csv'),
    ('GPT-5.6 Luna', 'gpt_5.6_luna_bengali_results.csv')
]

model_outputs = {s_id: {} for s_id in samples_to_inspect}
for m_name, f_csv in models:
    with open(f_csv, 'r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            s_id = r.get('id')
            if s_id in samples_to_inspect:
                model_outputs[s_id][m_name] = {
                    'generated': r.get('generated', ''),
                    'rouge1': r.get('rouge1', ''),
                    'rouge2': r.get('rouge2', ''),
                    'rougeL': r.get('rougeL', '')
                }

with open('error_samples_out.txt', 'w', encoding='utf-8') as out:
    for s_id in samples_to_inspect:
        out.write(f"====================================================\n")
        out.write(f"SAMPLE ID: {s_id}\n")
        out.write(f"====================================================\n")
        src = sources.get(s_id, {})
        out.write(f"--- SOURCE TEXT ---\n{src.get('text', '')[:600]}...\n\n")
        out.write(f"--- REFERENCE SUMMARY ---\n{src.get('summary', '')}\n\n")
        out.write(f"--- MODEL GENERATIONS ---\n")
        for m_name in models:
            gen_data = model_outputs[s_id].get(m_name[0], {})
            out.write(f"\n[{m_name[0]}] (R1: {gen_data.get('rouge1')}, R2: {gen_data.get('rouge2')}):\n")
            out.write(f"{gen_data.get('generated', '')}\n")
        out.write("\n\n")

print("Saved samples to error_samples_out.txt")
