# XL-Sum LLM Evaluation Benchmark 

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Framework: PyTorch](https://img.shields.io/badge/Framework-PyTorch-orange.svg)](https://pytorch.org/)
[![Dataset: XL-Sum](https://img.shields.io/badge/Dataset-XL--Sum-purple.svg)](https://huggingface.co/datasets/csebuetnlp/xlsum)

This repository provides a comprehensive, reproducible zero-shot evaluation framework for Large Language Models (LLMs) on abstractive news summarization across **Bengali** and **English** using the **XL-Sum benchmark dataset** (1,012 test items each).

---

##  Project Overview & Methodology

The goal of this benchmark is to establish performance baselines across closed-source frontier models (OpenAI GPT series, Google Gemini) and open-weights models (Meta LLaMA, Alibaba Qwen, DeepSeek).

### Key Evaluation Features:
- **Linguistic & Statistical Metrics**: Evaluates **ROUGE-1, ROUGE-2, ROUGE-L, BLEU, chrF, and BERTScore-Recall**.
- **Recommended Metric Selection** (based on *SummEval* & *BanglaSummEval* literature):
  - **ROUGE-1 / ROUGE-2**: Prioritized over ROUGE-L to reward semantic quality without penalizing structural restructuring.
  - **chrF**: Captures character n-gram overlap, showing strong human correlation ($r = 0.588$).
  - **BERTScore-Recall**: Assesses factual coverage using `roberta-base` for English and `xlm-roberta-base` for Bengali.
- **LLM-as-a-Judge**: Incorporates G-Eval multi-aspect evaluation (Fluency, Coherence, Relevance, Consistency).
- **Auto-Resume Pipeline**: API evaluation runners incrementally save outputs per sample, avoiding duplicate execution or API quota wastage.

---

##  Benchmark Results (1,012 Test Items)

### 1. English Abstractive Summarization Benchmark

| Model Identifier | Engine / Provider | Completed | ROUGE-1 (%) | ROUGE-2 (%) | ROUGE-L (%) | chrF (%) | BERTScore-Recall (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GPT 5.6 Luna** | OpenAI API | 1012 | **24.12%** | 5.87% | **15.96%** | **31.51%** | 89.02% |
| **Gemini 3.1 Flash Lite** | Google AI Studio | 1011 | 22.94% | **5.89%** | 15.32% | 30.39% | **89.25%** |
| **Gemini 2.5 Flash** | Google AI Studio | 1012 | 22.13% | 5.43% | 14.72% | 29.62% | 88.90% |
| **Qwen 3.5 Flash** | OpenRouter | 1012 | 21.99% | 4.93% | 14.48% | 29.46% | 88.77% |
| **DeepSeek V4 Flash** | OpenRouter | 1012 | 21.43% | 5.28% | 14.12% | 29.34% | 88.83% |
| **Qwen 3.6 27B Instruct** | OpenRouter | 1012 | 21.31% | 4.81% | 13.89% | 27.17% | 88.81% |
| **GPT-4o Mini** | OpenAI API | 1012 | 21.16% | 5.03% | 13.95% | 28.78% | 88.73% |
| **LLaMA 3.3 70B Versatile** | Groq API | 1012 | 20.38% | 5.71% | 14.00% | 28.72% | 88.87% |

---

### 2. Bengali Abstractive Summarization Benchmark

| Model Identifier | Engine / Provider | Completed | ROUGE-1 (%) | ROUGE-2 (%) | ROUGE-L (%) | chrF (%) | BERTScore-Recall (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **LLaMA 3.3 70B Versatile** | Groq API | 1012 | **16.23%** | **5.29%** | **12.44%** | 33.30% | **87.94%** |
| **GPT-4o Mini** | OpenAI API | 1012 | 15.63% | 4.53% | 11.83% | **33.74%** | 87.80% |
| **Gemini 2.5 Flash** | Google AI Studio | 1012 | 15.05% | 4.32% | 11.27% | 33.11% | 87.93% |
| **DeepSeek V4 Flash** | OpenRouter | 1012 | 15.00% | 4.19% | 11.22% | 33.39% | 87.86% |
| **Qwen 3.5 Flash** | OpenRouter | 1012 | 14.74% | 4.09% | 11.16% | 33.50% | 87.72% |
| **Gemini 3.1 Flash Lite** | Google AI Studio | 1012 | 14.04% | 3.88% | 10.93% | 32.15% | 87.88% |
| **GPT 5.6 Luna** | OpenAI API | 1012 | 14.01% | 3.71% | 10.65% | 32.53% | 87.57% |
| **Qwen 3.6 27B Instruct** | OpenRouter | 1012 | 13.50% | 3.57% | 10.11% | 28.38% | 87.44% |

---

### 3. Statistical Significance & Confidence Intervals

To ensure rigorous evaluation, standard deviations (SD), 95% bootstrap confidence intervals (CI), and paired statistical significance tests ($p$-values with 5,000 bootstrap resamples) are computed across model pairs:

- **Bengali Factuality (BanglaSummEval BSE-F1)**:
  - **Gemini 2.5 Flash**: Mean = $58.43\%$, SD = $16.77$, 95% CI: [$55.08, 61.50$]
  - **LLaMA 3.3 70B**: Mean = $58.28\%$, SD = $16.64$, 95% CI: [$54.79, 61.22$]
  - **Paired Significance Test**: The difference of $+0.15\%$ between Gemini 2.5 Flash ($58.43\%$) and LLaMA 3.3 70B ($58.28\%$) is **not statistically significant** ($t = 0.098$, $p = 0.9218$, bootstrap $p = 0.9162$). Both models perform equivalently.
- **English Factuality (SummEval SE-F1)**:
  - **DeepSeek V4 Flash**: Mean = $63.45\%$, SD = $15.16$, 95% CI: [$60.55, 66.50$]
  - **LLaMA 3.3 70B**: Mean = $60.18\%$, SD = $17.11$, 95% CI: [$56.83, 63.68$]
  - **Paired Significance Test**: DeepSeek V4 Flash significantly outperforms LLaMA 3.3 70B ($+3.27\%$, $t = 2.407$, $p = 0.0161^*$).
- **Bengali ROUGE-1 (1,012 items)**:
  - **LLaMA 3.3 70B** ($16.23\%$, 95% CI: [$15.68, 16.78$]) vs. **GPT-4o Mini** ($15.63\%$, 95% CI: [$15.15, 16.13$]): Statistically significant difference ($+0.61\%$, $p = 0.0067^{**}$).

To run the full statistical significance suite across all models and metrics:
```bash
python src/evaluation/compute_stats.py
```

---

##  Repository Organization

```text
xlsum-llm-eval/
├── README.md                           # Main publication landing page & benchmark leaderboard
├── LICENSE                             # MIT License
├── CITATION.cff                        # GitHub interactive citation metadata
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
│   ├── english/                        # English output CSV files per model
│   └── summaries/                      # Aggregated master CSV/TSV tables
│
├── figures/                            # Publication-ready figures (.pdf and .png)
│
└── tools/                              # Data inspection & diagnostic scripts
    ├── check_anomalies.py
    └── extract_error_samples.py
```

---

## 🚀 Getting Started

### 1. Installation

Clone the repository and install required packages:

```bash
git clone https://github.com/khanmahijyoti/xlsum-llm-eval.git
cd xlsum-llm-eval
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

---


