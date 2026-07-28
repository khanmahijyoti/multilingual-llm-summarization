# XL-Sum LLM Evaluation Benchmark: Project Comprehensive Documentation

**Repository Name:** `xlsum-llm-eval`  
**GitHub Remote:** `https://github.com/khanmahijyoti/xlsum-llm-eval.git`  
**Active Branch:** `gpt-eval-results`  
**Last Updated:** July 28, 2026  

---

## 1. Executive Summary & Objective

This project provides a comprehensive, reproducible zero-shot evaluation framework for Large Language Models (LLMs) on abstractive news summarization across **Bengali** and **English** using the **XL-Sum benchmark dataset** (1,012 test items each).

The goal of this evaluation is to establish cross-lingual performance baselines across closed-source frontier models (OpenAI GPT series, Google Gemini) and open-weights models (Meta LLaMA, Alibaba Qwen, DeepSeek).

---

## 2. Complete Benchmark Results

Evaluation metrics computed are **ROUGE-1**, **ROUGE-2**, and **ROUGE-L** (F1 %).  
* **Bengali Tokenizer:** Regex Indic tokenization (`[\u0980-\u09FF\w]+`).
* **English Tokenizer:** Porter Stemmer with standard English word boundaries.

### 2.1 Bengali XL-Sum Test Set (1,012 Items)

| Model Identifier | Provider / Engine | Completed Items | ROUGE-1 (%) | ROUGE-2 (%) | ROUGE-L (%) | Result CSV File |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Groq LLaMA 3.3 70B Versatile** | Groq API | **1,012 / 1,012** | **16.23%** | **5.29%** | **12.44%** | `groq_llama70b_1000_results.csv` |
| **GPT-4o Mini** | OpenAI API | **1,012 / 1,012** | **15.63%** | **4.53%** | **11.83%** | `gpt_4o_mini_bengali_results.csv` |
| **GPT-5.6 Luna** | OpenAI API | **1,012 / 1,012** | **14.01%** | **3.71%** | **10.65%** | `gpt_5.6_luna_bengali_results.csv` |
| **Gemini 3.1 Flash Lite** | Google AI Studio | **1,012 / 1,012** | **13.87%** | **3.83%** | **10.80%** | `gemini_3.1_flash_lite_bengali_results.csv` |
| **Qwen 3.6 27B Instruct** | OpenRouter | **1,012 / 1,012** | **13.50%** | **3.57%** | **10.11%** | `qwen_3.6_27b_bengali_results.csv` |
| *DeepSeek V4 Flash* | OpenRouter | *813 / 1,012* | *14.88%* | *4.22%* | *11.06%* | `deepseek_v4_flash_bengali_results.csv` |
| *Qwen 3.5 Flash* | OpenRouter | *381 / 1,012* | *14.67%* | *4.11%* | *11.03%* | `qwen_3.5_flash_bengali_results.csv` |

### 2.2 English XL-Sum Test Set (1,012 Items)

| Model Identifier | Provider / Engine | Completed Items | ROUGE-1 (%) | ROUGE-2 (%) | ROUGE-L (%) | Result CSV File |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **GPT-5.6 Luna** | OpenAI API | **1,012 / 1,012** | **24.12%** | **5.87%** | **15.96%** | `gpt_5.6_luna_english_results.csv` |
| **DeepSeek V4 Flash** | OpenRouter | **1,012 / 1,012** | **21.43%** | **5.28%** | **14.12%** | `deepseek_v4_flash_english_results.csv` |
| **Qwen 3.6 27B Instruct** | OpenRouter | **1,012 / 1,012** | **21.31%** | **4.81%** | **13.89%** | `qwen_3.6_27b_english_results.csv` |
| **GPT-4o Mini** | OpenAI API | **1,012 / 1,012** | **21.16%** | **5.03%** | **13.95%** | `gpt_4o_mini_english_results.csv` |
| **Groq LLaMA 3.3 70B Versatile** | Groq API | **1,012 / 1,012** | **20.38%** | **5.71%** | **14.00%** | `groq_llama70b_1012_english_results.csv` |
| *Qwen 3.5 Flash* | OpenRouter | *762 / 1,012* | *22.09%* | *4.97%* | *14.59%* | `qwen_3.5_flash_english_results.csv` |
| *Gemini 3.1 Flash Lite* | Google AI Studio | *371 / 1,012* | *23.04%* | *6.08%* | *15.65%* | `gemini_3.1_flash_lite_english_results.csv` |

---

## 3. Evaluation Scripts & Software Architecture

The evaluation codebase consists of modular, CLI-configurable Python scripts located in `E:\sounds\bengali_XLSum_v2.0`:

1. **`evaluate_openai_models.py`**
   * Handles OpenAI API calls (`gpt-4o-mini`, `gpt-5.6-luna`).
   * Validates API keys at startup, prioritizing active funded keys.
   * Dynamically adjusts payload parameters (omits fixed `temperature: 0.3` for models requiring default temperature 1.0 like `gpt-5.6-luna`).
   * Supports `--lang` parameter (`bengali` or `english`).

2. **`evaluate_gemini_models.py`**
   * Handles Google AI Studio Gemini models (`gemini-3.1-flash-lite`, `gemini-2.5-flash`).
   * Features automatic API key rotation pool across 7 keys with rate limit backoff.

3. **`evaluate_openrouter_models.py`**
   * Handles OpenRouter models (`deepseek/deepseek-v4-flash`, `qwen/qwen3.6-27b-instruct`, `qwen/qwen3.5-flash-02-23`).
   * Strips reasoning/thinking tags (`<think>...</think>`) before computing ROUGE metrics.

4. **`evaluate_groq_qwen.py`**
   * Handles Groq API models (`llama-3.3-70b-versatile`).

5. **`benchmark_7_models.py`**
   * Master aggregator script containing Lead-3 baseline generator, Seq2Seq HuggingFace transformer runner (mT5/mBART), and Markdown/LaTeX table formatters.

---

## 4. Key Features Implemented

* **Auto-Resume Logic:** All evaluation scripts read existing output CSV files upon launch. If an item ID has already been summarized, it skips API execution and retains the score, ensuring zero duplicated work or API credit wastage.
* **Live CSV Output:** Results are saved incrementally after every single prediction.
* **Security & Git Hygiene:** Sensitive `api keys` file is strictly ignored in `.gitignore` along with environment and cache directories.
* **Git Repository Remote:** Repository renamed to `xlsum-llm-eval` and pushed to branch `gpt-eval-results`.

---

## 5. Ongoing Tasks & Auto-Resume Status

Background tasks continuously process remaining items whenever free API quotas reset:

1. **DeepSeek V4 Flash (Bengali):** 813 / 1,012 completed (`deepseek_v4_flash_bengali_results.csv`).
2. **Qwen 3.5 Flash (English):** 762 / 1,012 completed (`qwen_3.5_flash_english_results.csv`).
3. **Qwen 3.5 Flash (Bengali):** 381 / 1,012 completed (`qwen_3.5_flash_bengali_results.csv`).
4. **Gemini 3.1 Flash Lite (English):** 371 / 1,012 completed (`gemini_3.1_flash_lite_english_results.csv`).
