# GreekMMLU Assets

This repo hosts the two building blocks used to publish the Greek-MMLU benchmark:

- `greek_mmlu/`: complete Hugging Face dataset folder (dev/test JSONs, metadata, README, loader script).
- `lm_eval/tasks/greekmmlu/`: task configs patterned after ArabicMMLU so `lm-evaluation-harness` can evaluate the dataset.

## Hugging Face dataset

To (re)publish the dataset:

```bash
cd greekmmlu/greek_mmlu
hf upload <username>/GreekMMLU . --repo-type dataset --commit-message \"Upload Greek-MMLU\"
```

Checklist before pushing:

1. Each subject keeps **exactly 5** dev questions (see `data/dev/*.json`).
2. No question overlap between dev/test JSON files.
3. Files validate with `python -m json.tool data/dev/<subject>.json`.

## lm-eval-harness integration

Copy `lm_eval/tasks/greekmmlu` into an `lm-evaluation-harness` checkout and register the configs (mirrors `lm_eval/tasks/arabicmmlu`). Example usage once copied:

```bash
python -m lm_eval --model hf-causal --tasks greekmmlu_mathematics
```

## License & citation

Dataset license: CC-BY-SA-4.0. Cite as:

```
@dataset{greek_mmlu_2025,
  title  = {Greek-MMLU: A Massive Multitask Language Understanding Benchmark for Greek},
  author = {...},
  year   = {2025}
}
```
