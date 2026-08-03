# XL-Sum LLM Evaluation Benchmark 📊

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Framework](https://img.shields.io/badge/Framework-PyTorch-orange.svg)](https://pytorch.org/)

This repository provides a comprehensive, reproducible, and standardized zero-shot evaluation framework for Large Language Models (LLMs) on abstractive news summarization across **English** and **Bengali** using the **XL-Sum benchmark dataset** (1,012 test items each).

---

## 1. Project Objective & Methodology

The goal of this project is to benchmark the summarization capabilities of leading closed-source frontier models and open-weights models. The evaluation pipelines are designed around linguistic research recommendations for news summarization:
* **Linguistic Metrics**: Rather than relying only on traditional lexically-constrained metrics (like BLEU), the evaluation pipeline implements **ROUGE-1, ROUGE-2, ROUGE-L, BLEU, chrF, and BERTScore-Recall**.
* **Metrics Selection Insights (from SummEval & BanglaSummEval)**:
  * **ROUGE-2 and ROUGE-1** are prioritized over ROUGE-L, as ROUGE-L penalizes semantic restructuring.
  * **chrF** is used as it correlates much better with human judgments of summary relevance (Pearson's $r = 0.588$) compared to BLEU ($r = 0.073$).
  * **BERTScore-Recall** is used to evaluate factual coverage, using **`roberta-base`** for English (recommended by *SummEval*) and **`xlm-roberta-base`** for Bengali (recommended by *BanglaSummEval*).

---

## 2. Complete Benchmark Results (1,012 Items Each)

The following tables show the final benchmark scores calculated across **8 LLMs** on the full test sets:

### 2.1 English Summarization Benchmark

| Model | Count | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU | chrF | BERTScore-R |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GPT 5.6 Luna** | 1012 | **24.12%** | 5.87% | **15.96%** | 2.06% | **31.51%** | 89.02% |
| **Gemini 3.1 Flash Lite** | 1011 | 22.94% | **5.89%** | 15.32% | **2.14%** | 30.39% | **89.25%** |
| **Gemini 2.5 Flash** | 1012 | 22.13% | 5.43% | 14.72% | 1.90% | 29.62% | 88.90% |
| **Qwen 3.5 Flash** | 1012 | 21.99% | 4.93% | 14.48% | 1.66% | 29.46% | 88.77% |
| **Deepseek V4 Flash** | 1012 | 21.43% | 5.28% | 14.12% | 1.82% | 29.34% | 88.83% |
| **Qwen 3.6 27B** | 1012 | 21.31% | 4.81% | 13.89% | 1.44% | 27.17% | 88.81% |
| **GPT 4o Mini** | 1012 | 21.16% | 5.03% | 13.95% | 1.70% | 28.78% | 88.73% |
| **Llama 3.3 70B (Groq)** | 1012 | 20.38% | 5.71% | 14.00% | 1.94% | 28.72% | 88.87% |

---

### 2.2 Bengali Summarization Benchmark

| Model | Count | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU | chrF | BERTScore-R |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Llama 3.3 70B (Groq)** | 1012 | **16.23%** | **5.29%** | **12.44%** | **1.90%** | 33.30% | **87.94%** |
| **GPT 4o Mini** | 1012 | 15.63% | 4.53% | 11.83% | 1.74% | **33.74%** | 87.80% |
| **Gemini 2.5 Flash** | 1012 | 15.05% | 4.32% | 11.27% | 1.64% | 33.11% | 87.93% |
| **Deepseek V4 Flash** | 1012 | 15.00% | 4.19% | 11.22% | 1.62% | 33.39% | 87.86% |
| **Qwen 3.5 Flash** | 1012 | 14.74% | 4.09% | 11.16% | 1.56% | 33.50% | 87.72% |
| **Gemini 3.1 Flash Lite** | 1012 | 14.04% | 3.88% | 10.93% | 1.42% | 32.15% | 87.88% |
| **GPT 5.6 Luna** | 1012 | 14.01% | 3.71% | 10.65% | 1.27% | 32.53% | 87.57% |
| **Qwen 3.6 27B** | 1012 | 13.50% | 3.57% | 10.11% | 0.98% | 28.38% | 87.44% |

---

## 3. Repository Directory Structure

```text
xlsum-llm-eval/
│
├── english_XLSum_v2.0/                # English-specific files
│   ├── deepseek_v4_flash_english_results.csv
│   ├── gemini_2.5_flash_english_results.csv
│   ├── gemini_3.1_flash_lite_english_results.csv
│   ├── gpt_4o_mini_english_results.csv
│   ├── gpt_5.6_luna_english_results.csv
│   ├── groq_llama70b_1012_english_results.csv
│   ├── qwen_3.5_flash_english_results.csv
│   ├── qwen_3.6_27b_english_results.csv
│   │
│   ├── run_combined_llm_english.py     # Prompt-generation and summarizer
│   ├── evaluate_all_metrics.py         # The evaluation script
│   ├── final_comparison_results.tsv    # Extracted TSV sheet results
│   ├── SummEval-pdf.md                 # Summary metric literature reference
│   └── BanglaSummEval-pdf.md           # Bengali metric literature reference
│
├── deepseek_v4_flash_bengali_results.csv # Bengali evaluation output CSVs
├── gemini_2.5_flash_bengali_results.csv
├── gemini_3.1_flash_lite_bengali_results.csv
├── gpt_4o_mini_bengali_results.csv
├── gpt_5.6_luna_bengali_results.csv
├── groq_llama70b_1000_results.csv
├── qwen_3.5_flash_bengali_results.csv
├── qwen_3.6_27b_bengali_results.csv
│
├── run_combined_llm.py                 # Multi-LLM API runner for Bengali
├── evaluate_gemini_models.py           # Gemini evaluation wrapper
├── evaluate_groq_qwen.py               # Groq LLaMA evaluation wrapper
├── evaluate_openai_models.py           # OpenAI evaluation wrapper
├── evaluate_openrouter_models.py       # OpenRouter (Qwen/Deepseek) wrapper
├── .gitignore                          # Ignores cached folders, API keys, and datasets
└── README.md                           # Comprehensive documentation
```

---

## 4. Getting Started

### 4.1 Prerequisites
Create and activate the environment, then install dependencies:
```bash
pip install sacrebleu bert-score rouge-score torch transformers
```

### 4.2 How to Run the Evaluation
To calculate all evaluation metrics across the results, run:
```bash
python english_XLSum_v2.0/evaluate_all_metrics.py
```
This script will:
1. Parse the text fields and ROUGE parameters in each language's result CSV.
2. Evaluate corpus BLEU and chrF.
3. Compute semantic token alignment using **BERTScore-Recall** on a GPU (using `roberta-base` for English and `xlm-roberta-base` for Bengali).
4. Save the compiled results in `english_XLSum_v2.0/final_comparison_results.tsv`.