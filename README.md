# MULTILINGUAL-LLM-SUMMARIZATION

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Framework: PyTorch](https://img.shields.io/badge/Framework-PyTorch-orange.svg)](https://pytorch.org/)
[![Dataset: XL-Sum](https://img.shields.io/badge/Dataset-XL--Sum-purple.svg)](https://huggingface.co/datasets/csebuetnlp/xlsum)

This repository provides a comprehensive, reproducible zero-shot evaluation framework for Large Language Models (LLMs) on abstractive news summarization across **Bengali** and **English** using the **XL-Sum benchmark dataset** (1,012 test items each).

---

## Project Overview & Methodology

The goal of this benchmark is to establish performance baselines across closed-source frontier models (OpenAI GPT series, Google Gemini) and open-weights models (Meta LLaMA, Alibaba Qwen, DeepSeek).

### Key Evaluation Features:
- **Linguistic & Statistical Metrics**: Evaluates **ROUGE-1, ROUGE-2, ROUGE-L, BLEU, chrF, and BERTScore-Recall**.
- **Recommended Metric Selection** (based on *SummEval* & *BanglaSummEval* literature):
  - **ROUGE-1 / ROUGE-2**: Prioritized over ROUGE-L to reward semantic quality without penalizing structural restructuring.
  - **chrF**: Captures character n-gram overlap, showing strong human correlation (r = 0.588).
  - **BERTScore-Recall**: Assesses factual coverage using `roberta-base` for English and `xlm-roberta-base` for Bengali.
- **LLM-as-a-Judge**: Incorporates G-Eval multi-aspect evaluation (Fluency, Coherence, Relevance, Consistency).
- **Auto-Resume Pipeline**: API evaluation runners incrementally save outputs per sample, avoiding duplicate execution or API quota wastage.

---

## Benchmark Results (1,012 Test Items)

### 1. English Abstractive Summarization Benchmark

| Model Identifier | Engine / Provider | Completed | ROUGE-1 (%) | ROUGE-2 (%) | ROUGE-L (%) | chrF (%) | BERTScore-Recall (%) | SummEval Precision (%) | SummEval Recall (%) | SummEval F1 (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GPT 5.6 Luna** | OpenAI API | 1012 | **24.12%** | 5.87% | **15.96%** | **31.51%** | 89.02% | 65.17% | 58.00% | 58.05% |
| **Gemini 3.1 Flash Lite** | Google AI Studio | 1011 | 22.94% | **5.89%** | 15.32% | 30.39% | **89.25%** | 59.74% | 52.83% | 52.28% |
| **Gemini 2.5 Flash** | Google AI Studio | 1012 | 22.13% | 5.43% | 14.72% | 29.62% | 88.90% | 65.93% | 58.33% | 59.44% |
| **Qwen 3.5 Flash** | OpenRouter | 1012 | 21.99% | 4.93% | 14.48% | 29.46% | 88.77% | 67.04% | 58.17% | 58.52% |
| **DeepSeek V4 Flash** | OpenRouter | 1012 | 21.43% | 5.28% | 14.12% | 29.34% | 88.83% | 69.66% | **63.00%** | **63.45%** |
| **Qwen 3.6 27B Instruct** | OpenRouter | 1012 | 21.31% | 4.81% | 13.89% | 27.17% | 88.81% | 63.12% | 55.83% | 56.58% |
| **GPT-4o Mini** | OpenAI API | 1012 | 21.16% | 5.03% | 13.95% | 28.78% | 88.73% | 65.62% | 59.67% | 59.76% |
| **LLaMA 3.3 70B Versatile** | Groq API | 1012 | 20.38% | 5.71% | 14.00% | 28.72% | 88.87% | **69.68%** | 57.17% | 60.18% |

---

### 2. Bengali Abstractive Summarization Benchmark

| Model Identifier | Engine / Provider | Completed | ROUGE-1 (%) | ROUGE-2 (%) | ROUGE-L (%) | chrF (%) | BERTScore-Recall (%) | BanglaSummEval Precision (%) | BanglaSummEval Recall (%) | BanglaSummEval F1 (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LLaMA 3.3 70B Versatile** | Groq API | 1012 | **16.23%** | **5.29%** | **12.44%** | 33.30% | **87.94%** | **65.78%** | 57.50% | 58.28% |
| **GPT-4o Mini** | OpenAI API | 1012 | 15.63% | 4.53% | 11.83% | **33.74%** | 87.80% | 63.38% | 55.33% | 56.73% |
| **Gemini 2.5 Flash** | Google AI Studio | 1012 | 15.05% | 4.32% | 11.27% | 33.11% | 87.93% | 61.65% | **60.83%** | **58.43%** |
| **DeepSeek V4 Flash** | OpenRouter | 1012 | 15.00% | 4.19% | 11.22% | 33.39% | 87.86% | 64.14% | 56.17% | 57.34% |
| **Qwen 3.5 Flash** | OpenRouter | 1012 | 14.74% | 4.09% | 11.16% | 33.50% | 87.72% | 61.48% | 57.17% | 56.15% |
| **Gemini 3.1 Flash Lite** | Google AI Studio | 1012 | 14.04% | 3.88% | 10.93% | 32.15% | 87.88% | 52.83% | 52.50% | 49.73% |
| **GPT 5.6 Luna** | OpenAI API | 1012 | 14.01% | 3.71% | 10.65% | 32.53% | 87.57% | 58.87% | 56.17% | 54.84% |
| **Qwen 3.6 27B Instruct** | OpenRouter | 1012 | 13.50% | 3.57% | 10.11% | 28.38% | 87.44% | 61.69% | 58.16% | 57.02% |

---

### 3. Statistical Significance & Confidence Intervals

To ensure rigorous evaluation, standard deviations (SD), 95% bootstrap confidence intervals (CI), and paired statistical significance tests (paired $t$-statistic, asymptotic $p$-value, and bootstrap $p$-value with 5,000 paired resamples) are computed consistently across all reported comparisons:

#### Unified Statistical Significance & Comparison Table

| Comparison / Metric | Model A (Mean ± SD [95% CI]) | Model B (Mean ± SD [95% CI]) | Mean Difference (A − B) | Paired Test ($t$) | Paired $p$-value | Bootstrap $p$-value ($B=5,000$) | Finding |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Bengali Factuality (BSE-F1)** | **Gemini 2.5 Flash**<br>58.43% ± 16.77 [55.08, 61.60] ($N=100$) | **LLaMA 3.3 70B**<br>58.28% ± 16.64 [54.92, 61.35] ($N=100$) | +0.15% | $t = 0.098$ | $p = 0.9218$ | $p = 0.9162$ | The difference is not statistically significant |
| **English Factuality (SE-F1)** | **DeepSeek V4 Flash**<br>63.45% ± 15.16 [60.53, 66.48] ($N=100$) | **LLaMA 3.3 70B**<br>60.18% ± 17.11 [56.84, 63.54] ($N=100$) | +3.27% | $t = 2.407$ | $p = 0.0161$ | $p = 0.0130$ | Statistically significant ($p < 0.05$) |
| **Bengali ROUGE-1 (Primary)** | **LLaMA 3.3 70B**<br>16.23% ± 9.05 [15.69, 16.79] ($N=1012$) | **GPT-4o Mini**<br>15.63% ± 8.27 [15.12, 16.13] ($N=1012$) | +0.61% | $t = 2.713$ | $p = 0.0067$ | $p = 0.0070$ | Statistically significant ($p < 0.01$) |
| **Bengali ROUGE-1 (Secondary)** | **LLaMA 3.3 70B**<br>16.23% ± 9.05 [15.69, 16.79] ($N=1012$) | **Gemini 2.5 Flash**<br>15.05% ± 7.86 [14.55, 15.52] ($N=1012$) | +1.19% | $t = 5.364$ | $p < 0.0001$ | $p < 0.0001$ | Statistically significant ($p < 0.0001$) |
| **English ROUGE-1 (Top Pair)** | **GPT-5.6 Luna**<br>24.12% ± 7.61 [23.65, 24.59] ($N=1012$) | **Gemini 3.1 Flash Lite**<br>22.94% ± 6.60 [22.54, 23.35] ($N=1011$) | +1.17% | $t = 6.321$ | $p < 0.0001$ | $p < 0.0001$ | Statistically significant ($p < 0.0001$) |

#### Comparison-by-Comparison Detail

- **Bengali Factuality (BanglaSummEval BSE-F1)**:
  - **Gemini 2.5 Flash**: Mean = 58.43%, SD = 16.77, 95% CI: [55.08, 61.60] ($N = 100$)
  - **LLaMA 3.3 70B**: Mean = 58.28%, SD = 16.64, 95% CI: [54.92, 61.35] ($N = 100$)
  - **Mean Difference**: +0.15% (unrounded: +0.146%)
  - **Paired Test Statistic**: $t = 0.098$ ($N = 100$)
  - **Paired-test $p$-value**: $p = 0.9218$
  - **Bootstrap $p$-value (5,000 resamples)**: $p = 0.9162$
  - **Finding**: The difference is not statistically significant.

- **English Factuality (SummEval SE-F1)**:
  - **DeepSeek V4 Flash**: Mean = 63.45%, SD = 15.16, 95% CI: [60.53, 66.48] ($N = 100$)
  - **LLaMA 3.3 70B**: Mean = 60.18%, SD = 17.11, 95% CI: [56.84, 63.54] ($N = 100$)
  - **Mean Difference**: +3.27% (unrounded: +3.271%)
  - **Paired Test Statistic**: $t = 2.407$ ($N = 100$)
  - **Paired-test $p$-value**: $p = 0.0161$
  - **Bootstrap $p$-value (5,000 resamples)**: $p = 0.0130$
  - **Finding**: Statistically significant ($p < 0.05$).

- **Bengali ROUGE-1 (LLaMA 3.3 70B vs. GPT-4o Mini)**:
  - **LLaMA 3.3 70B**: Mean = 16.23%, SD = 9.05, 95% CI: [15.69, 16.79] ($N = 1012$)
  - **GPT-4o Mini**: Mean = 15.63%, SD = 8.27, 95% CI: [15.12, 16.13] ($N = 1012$)
  - **Mean Difference**: +0.61% (unrounded: +0.608%)
  - **Paired Test Statistic**: $t = 2.713$ ($N = 1012$)
  - **Paired-test $p$-value**: $p = 0.0067$
  - **Bootstrap $p$-value (5,000 resamples)**: $p = 0.0070$
  - **Finding**: Statistically significant ($p < 0.01$).

- **Bengali ROUGE-1 (LLaMA 3.3 70B vs. Gemini 2.5 Flash)**:
  - **LLaMA 3.3 70B**: Mean = 16.23%, SD = 9.05, 95% CI: [15.69, 16.79] ($N = 1012$)
  - **Gemini 2.5 Flash**: Mean = 15.05%, SD = 7.86, 95% CI: [14.55, 15.52] ($N = 1012$)
  - **Mean Difference**: +1.19% (unrounded: +1.187%)
  - **Paired Test Statistic**: $t = 5.364$ ($N = 1012$)
  - **Paired-test $p$-value**: $p < 0.0001$ ($p = 8.12 \times 10^{-8}$)
  - **Bootstrap $p$-value (5,000 resamples)**: $p < 0.0001$ (bootstrap $p = 0.0000$)
  - **Finding**: Statistically significant ($p < 0.0001$).

- **English ROUGE-1 (GPT-5.6 Luna vs. Gemini 3.1 Flash Lite)**:
  - **GPT-5.6 Luna**: Mean = 24.12%, SD = 7.61, 95% CI: [23.65, 24.59] ($N = 1012$)
  - **Gemini 3.1 Flash Lite**: Mean = 22.94%, SD = 6.60, 95% CI: [22.54, 23.35] ($N = 1011$)
  - **Mean Difference**: +1.17% (unrounded: +1.173%)
  - **Paired Test Statistic**: $t = 6.321$ ($N = 1011$)
  - **Paired-test $p$-value**: $p < 0.0001$ ($p = 2.60 \times 10^{-10}$)
  - **Bootstrap $p$-value (5,000 resamples)**: $p < 0.0001$ (bootstrap $p = 0.0000$)
  - **Finding**: Statistically significant ($p < 0.0001$).

To run the full statistical significance suite across all models and metrics:
```bash
python src/evaluation/compute_stats.py
```

---

## Repository Organization

```text
multilingual-llm-summarization/
├── README.md                           # Main publication landing page & benchmark leaderboard
├── LICENSE                             # MIT License
├── requirements.txt                    # Pinned python dependencies
├── .gitignore                          # Excludes credentials, caches, datasets, TeX files
│
├── data/                               # Dataset documentation & schemas
│   └── README.md                       # Instructions to download XL-Sum Bengali/English datasets
│
├── src/                                # Source code
│   ├── evaluation/                     # Metric engines (ROUGE, chrF, BLEU, BERTScore, LLM Judge)
│   │   ├── benchmark_7_models.py
│   │   ├── compute_bn_bertscore.py
│   │   ├── evaluate_all_16_files_judge.py
│   │   └── llm_judge_evaluate.py
│   ├── models/                         # API Providers & Evaluation Wrappers
│   │   ├── evaluate_openai_models.py
│   │   ├── evaluate_gemini_models.py
│   │   ├── evaluate_openrouter_models.py
│   │   └── evaluate_groq_qwen.py
│   └── visualization/                  # Publication visualizers
│       └── generate_paper_plots.py     # Generates radar, factuality, and ROUGE plots
│
├── results/                            # Benchmark Output Datasets
│   ├── bengali/                        # Bengali output CSV files per model
│   └── english/                        # English output CSV files per model
│
├── figures/                            # Publication-ready figures (.pdf and .png)
│
└── tools/                              # Data inspection & diagnostic scripts
    ├── check_anomalies.py
    └── extract_error_samples.py
```

---

## Getting Started

### 1. Installation

Clone the repository and install required packages:

```bash
git clone https://github.com/khanmahijyoti/multilingual-llm-summarization.git
cd multilingual-llm-summarization
pip install -r requirements.txt
```

### 2. Environment Variables

Set your API keys depending on the models you wish to evaluate:

```bash
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
export OPENROUTER_API_KEY="your-openrouter-key"
export GROQ_API_KEY="your-groq-key"
```

### 3. Running Metric Evaluation

To compute all metrics across generated model summaries:

```bash
python src/evaluation/benchmark_7_models.py
```

To generate publication figures:

```bash
python src/visualization/generate_paper_plots.py
```
