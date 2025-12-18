"""Greek-MMLU dataset loader."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Tuple

import datasets

_CITATION = """\
@dataset{greek_mmlu_2025,
  title  = {Greek-MMLU: A Massive Multitask Language Understanding Benchmark for Greek},
  author = {...},
  year   = {2025}
}
"""

_DESCRIPTION = """\
Greek-MMLU is a manually curated multiple-choice benchmark spanning 29 subjects in Modern Greek.
It mirrors the structure of ArabicMMLU and includes fixed dev/test splits (5 dev questions per subject)."""

_HOMEPAGE = "https://huggingface.co/datasets/USERNAME/GreekMMLU"
_LICENSE = "CC-BY-SA-4.0"

_LETTERS = ["A", "B", "C", "D", "E"]


def _load_metadata() -> List[Dict]:
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "data", "metadata.json"), encoding="utf-8") as f:
        return [entry for entry in json.load(f) if entry.get("included")]


_METADATA = _load_metadata()


@dataclass
class GreekMMLUConfig(datasets.BuilderConfig):
    subject_slug: str = ""
    subject_name: str = ""


class GreekMMLU(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        GreekMMLUConfig(
            name=entry["slug"],
            subject_slug=entry["slug"],
            subject_name=entry["subject"],
            version=datasets.Version("1.0.0"),
            description=f"Greek-MMLU subject: {entry['subject']}",
        )
        for entry in _METADATA
    ]
    DEFAULT_CONFIG_NAME = BUILDER_CONFIGS[0].name if BUILDER_CONFIGS else None

    def _info(self) -> datasets.DatasetInfo:
        choices_feature = {letter: datasets.Value("string") for letter in _LETTERS}
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "choices": choices_feature,
                    "answer": datasets.Value("string"),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        base_dir = self.config.data_dir or os.path.join(os.path.dirname(__file__), "data")
        slug = self.config.subject_slug
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(base_dir, "dev", f"{slug}.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(base_dir, "test", f"{slug}.json")},
            ),
        ]

    def _generate_examples(self, filepath: str) -> Iterator[Tuple[str, Dict]]:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        for row in data:
            choices = {letter: row["choices"].get(letter) for letter in _LETTERS}
            yield row["id"], {
                "id": row["id"],
                "question": row["question"],
                "choices": choices,
                "answer": row["answer"],
            }
