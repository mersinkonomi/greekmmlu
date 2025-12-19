"""
Utility to regenerate all GreekMMLU YAML configs from metadata.

Usage:
    python _generate_configs.py

This mirrors the ArabicMMLU generator but adapts the subject/group
metadata and the local JSONL split files we ship with the benchmark.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List

import yaml

LOGGER = logging.getLogger(__name__)

CATEGORY_INFO: Dict[str, Dict[str, str]] = {
    "Humanities": {"slug": "humanities", "tag": "greekmmlu_humanities_tasks"},
    "Social Sciences": {"slug": "social_science", "tag": "greekmmlu_social_science_tasks"},
    "STEM": {"slug": "stem", "tag": "greekmmlu_stem_tasks"},
    "Other": {"slug": "other", "tag": "greekmmlu_other_tasks"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate GreekMMLU YAML configs.")
    parser.add_argument(
        "--metadata",
        default="data/metadata.json",
        help="Metadata JSON describing subjects, slugs, and groups.",
    )
    parser.add_argument(
        "--base_yaml",
        default="_default_greekmmlu_template_yaml",
        help="Template YAML that every subject config should include.",
    )
    parser.add_argument(
        "--output_dir",
        default=".",
        help="Directory to write the per-subject YAML files into.",
    )
    return parser.parse_args()


def load_metadata(metadata_path: Path) -> List[Dict]:
    with metadata_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    metadata_path = Path(args.metadata)
    if not metadata_path.is_absolute():
        metadata_path = script_dir / metadata_path

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = (script_dir / output_dir).resolve()
    else:
        output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    subjects = load_metadata(metadata_path)

    for entry in subjects:
        subject = entry["subject"]
        group = entry["group"]
        slug = entry["slug"]
        category = CATEGORY_INFO[group]

        yaml_dict = {
            "include": Path(args.base_yaml).name,
            "task": f"greekmmlu_{slug}",
            "task_alias": subject,
            "dataset_name": "json",
            "dataset_kwargs": {
                "data_files": {
                    "test": f"https://huggingface.co/datasets/mkonomi/greek_mmlu/resolve/main/data/{slug}_test.jsonl",
                    "dev": f"https://huggingface.co/datasets/mkonomi/greek_mmlu/resolve/main/data/{slug}_dev.jsonl",
                }
            },
            "tag": category["tag"],
        }

        file_path = output_dir / f"greekmmlu_{slug}.yaml"
        LOGGER.info("Writing %s", file_path)

        with file_path.open("w", encoding="utf-8") as handle:
            yaml.dump(
                yaml_dict,
                handle,
                sort_keys=False,
                allow_unicode=True,
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
