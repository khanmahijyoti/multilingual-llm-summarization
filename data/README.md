# XL-Sum Dataset Guide

This project evaluates model performance on the **XL-Sum benchmark dataset** ([Hasan et al., 2021](https://arxiv.org/abs/2106.13853)), covering abstractive summarization across 44 languages.

## Downloading XL-Sum Data

Due to licensing and file size constraints, raw dataset split files (`bengali_train.jsonl`, `bengali_val.jsonl`, `bengali_test.jsonl`) are ignored by Git.

### 1. Download via Hugging Face Datasets (Recommended)

```python
from datasets import load_dataset

# Load Bengali XL-Sum test set
bengali_test = load_dataset("csebuetnlp/xlsum", "bengali", split="test")

# Load English XL-Sum test set
english_test = load_dataset("csebuetnlp/xlsum", "english", split="test")
```

### 2. Manual JSONL Placement

If using JSONL split files locally, place them in the `data/` directory with the following structure:
```text
data/
├── bengali_test.jsonl
├── bengali_val.jsonl
└── english_test.jsonl
```

Each record in `jsonl` format contains:
- `id`: Unique article identifier string
- `url`: Article URL
- `title`: Article header title
- `summary`: Reference ground-truth summary
- `text`: Main article body content text
