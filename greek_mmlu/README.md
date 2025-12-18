---
pretty_name: Greek-MMLU
language:
  - el
tags:
  - evaluation
  - mmlu
  - greek
task_categories:
  - other
license: cc-by-sa-4.0
---

# Greek-MMLU

## Abstract
Greek-MMLU is a Massive Multitask Language Understanding benchmark covering 29 school and professional subjects written entirely in Modern Greek. It mirrors ArabicMMLU’s structure and provides dev/test splits that enable reproducible evaluation of multilingual language models.

## Motivation
- Extend the MMLU family to a manually curated Greek benchmark.
- Provide a community resource for evaluating Greek-centric and cross-lingual models.
- Ensure compatibility with `lm-eval-harness` and Hugging Face Datasets for transparent academic benchmarking.

## Dataset Construction
The underlying multiple-choice questions were aggregated from official Greek public exam resources (citizenship exams, government licensing exams, vocational certifications, etc.). Each entry contains a context (optional), a question, 3–5 answer choices, and a verified correct answer. Subjects span Humanities, Social Sciences, STEM, and professional “Other” domains.

## Manual Quality Control
The benchmark was manually validated prior to packaging:
- Answer keys were cross-checked against the original exam sources.
- Ambiguous or incorrect MCQs were removed manually.
- Duplicate questions were removed manually based on literal comparison.
- Greek text was normalized by hand for punctuation and diacritics.

No automated semantic deduplication, MinHash/LSH, or LLM-based validation was used.

## Dev/Test Split Policy
- Exactly **5 MCQs per subject** are assigned to the dev split.
- Dev questions were sampled deterministically with a fixed random seed (1337) to ensure reproducibility.
- All remaining MCQs per subject populate the test split.
- Dev and test sets are disjoint. Subjects with fewer than 5 MCQs are excluded entirely (only “Philosophy” was excluded).

## Subjects and Statistics

| Subject | Dev | Test | Total |
| --- | --- | --- | --- |
| Accounting | 5 | 185 | 190 |
| Agriculture | 5 | 533 | 538 |
| Art | 5 | 855 | 860 |
| Biology | 5 | 82 | 87 |
| Chemistry | 5 | 81 | 86 |
| Civil Engineering | 5 | 1,038 | 1,043 |
| Clinical Knowledge | 5 | 617 | 622 |
| Computer Networks & Security | 5 | 63 | 68 |
| Computer Science | 5 | 452 | 457 |
| Driving Rules | 5 | 2,240 | 2,245 |
| Economics | 5 | 287 | 292 |
| Education | 5 | 299 | 304 |
| Electrical Engineering | 5 | 684 | 689 |
| General Knowledge | 5 | 130 | 135 |
| Geography | 5 | 553 | 558 |
| Government and Politics | 5 | 360 | 365 |
| Greek History | 5 | 847 | 852 |
| Greek Literature | 5 | 14 | 19 |
| Greek Mythology | 5 | 321 | 326 |
| Greek Traditions | 5 | 507 | 512 |
| Law | 5 | 1,208 | 1,213 |
| Management | 5 | 896 | 901 |
| Mathematics | 5 | 1,504 | 1,509 |
| Medicine | 5 | 468 | 473 |
| Modern Greek Language | 5 | 3,190 | 3,195 |
| Physics | 5 | 2,082 | 2,087 |
| Prehistory | 5 | 63 | 68 |
| World History | 5 | 20 | 25 |
| World Religions | 5 | 155 | 160 |

Totals (included subjects): **Dev = 145**, **Test = 19,734**.  
Excluded subject: Philosophy (only 2 MCQs available, below the minimum threshold).

## JSON Format
Each subject file (under `data/dev/` or `data/test/`) is a JSON list of entries following:

```json
{
  "id": "physics_00012",
  "question": "Ποια είναι η μονάδα μέτρησης της δύναμης στο SI;",
  "choices": {
    "A": "Joule",
    "B": "Newton",
    "C": "Watt",
    "D": "Pascal"
  },
  "answer": "B"
}
```

## Evaluation Usage
### `lm-eval-harness`
```bash
pip install -e .
lm_eval --model hf --model_args pretrained=<model_name> \
        --tasks greekmmlu --device cuda:0
```
The included task YAMLs follow ArabicMMLU conventions and can be copied into `lm_eval/tasks/`.

### Hugging Face Datasets
```python
from datasets import load_dataset
ds = load_dataset("USERNAME/GreekMMLU", "physics")
```
This loads the dev/test splits for the `physics` subject.

## License
CC BY-SA 4.0

## Citation
```
@dataset{greek_mmlu_2025,
  title  = {Greek-MMLU: A Massive Multitask Language Understanding Benchmark for Greek},
  author = {...},
  year   = {2025}
}
```
