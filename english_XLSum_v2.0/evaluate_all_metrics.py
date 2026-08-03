import os
import csv
import torch
import sacrebleu
from bert_score import score

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[+] Using device: {device}")

results = []

for folder, lang in [("E:/sounds/english_XLSum_v2.0", "English"), ("E:/sounds/bengali_XLSum_v2.0", "Bengali")]:
    print(f"\nEvaluating folder: {folder} ({lang})")
    
    # Choose BERTScore model
    model_type = "xlm-roberta-base" if lang == "Bengali" else "roberta-base"
    print(f"  Using BERTScore model: {model_type}")
    
    for f in sorted(os.listdir(folder)):
        if f.endswith(".csv") and "results" in f:
            path = os.path.join(folder, f)
            try:
                # Display name
                name = f.replace("_english_results.csv", "").replace("_bengali_results.csv", "").replace("_results.csv", "")
                name = name.replace("groq_llama70b_1012", "Llama 3.3 70B (Groq)").replace("groq_llama70b_1000", "Llama 3.3 70B (Groq)")
                name = name.replace("_", " ").title()
                
                with open(path, "r", encoding="utf-8-sig") as infile:
                    reader = list(csv.DictReader(infile))
                
                ref_list = []
                gen_list = []
                r1_list = []
                r2_list = []
                rl_list = []
                
                for row in reader:
                    if row.get("id") == "id" or not row.get("rouge1"):
                        continue
                    ref_list.append(row["reference"])
                    gen_list.append(row["generated"])
                    r1_list.append(float(row["rouge1"]))
                    r2_list.append(float(row["rouge2"]))
                    rl_list.append(float(row["rougeL"]))
                
                if not ref_list:
                    continue
                
                # Compute BLEU
                bleu_scorer = sacrebleu.metrics.BLEU(effective_order=True)
                bleu_score = bleu_scorer.corpus_score(gen_list, [ref_list]).score
                
                # Compute chrF
                chrf_scorer = sacrebleu.metrics.CHRF()
                chrf_score = chrf_scorer.corpus_score(gen_list, [ref_list]).score
                
                # Compute BERTScore Recall (using GPU if available, with fallback exception handling)
                try:
                    P, R, F1 = score(gen_list, ref_list, model_type=model_type, device=device, verbose=False)
                    bs_rec_val = R.mean().item() * 100
                    bs_rec = f"{bs_rec_val:.2f}"
                except Exception as e:
                    print(f"    [!] Warning: BERTScore-Recall calculation failed for {name}: {e}")
                    bs_rec = "N/A"
                
                avg_r1 = sum(r1_list) / len(r1_list)
                avg_r2 = sum(r2_list) / len(r2_list)
                avg_rl = sum(rl_list) / len(rl_list)
                
                results.append({
                    "Language": lang,
                    "Model": name,
                    "Count": len(ref_list),
                    "R1": avg_r1,
                    "R2": avg_r2,
                    "RL": avg_rl,
                    "BLEU": bleu_score,
                    "chrF": chrf_score,
                    "BERTScore-R": bs_rec
                })
                print(f"    Completed: {name} (Count: {len(ref_list)}) -> R1: {avg_r1:.2f}, BLEU: {bleu_score:.2f}, BERTScore-R: {bs_rec}")
                
            except Exception as e:
                print(f"    Error evaluating {f}: {e}")

# Save final comparison TSV
output_tsv_path = "E:/sounds/english_XLSum_v2.0/final_comparison_results.tsv"
with open(output_tsv_path, "w", encoding="utf-8", newline="") as outfile:
    writer = csv.writer(outfile, delimiter="\t")
    writer.writerow(["Language", "Model", "Count", "ROUGE-1", "ROUGE-2", "ROUGE-L", "BLEU", "chrF", "BERTScore-R"])
    for r in results:
        writer.writerow([
            r["Language"],
            r["Model"],
            r["Count"],
            f"{r['R1']:.2f}",
            f"{r['R2']:.2f}",
            f"{r['RL']:.2f}",
            f"{r['BLEU']:.2f}",
            f"{r['chrF']:.2f}",
            r["BERTScore-R"]
        ])

print(f"\n[+] Successfully saved final comparison TSV to: {output_tsv_path}")
