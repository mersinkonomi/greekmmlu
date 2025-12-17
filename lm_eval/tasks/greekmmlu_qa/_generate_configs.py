"""
Generate Greek MMLU task configurations from gmmlu_qa.json dataset.
Creates individual YAML files for each subject and category group files.
"""

import argparse
import json
import logging
import os

import yaml
from tqdm import tqdm


eval_logger = logging.getLogger(__name__)


# Subject to category mapping based on the 'group' field in the dataset
SUBJECTS = {
    # Humanities
    "Art": "humanities",
    "Greek History": "humanities",
    "Greek Literature": "humanities",
    "Greek Mythology": "humanities",
    "Greek Traditions": "humanities",
    "Prehistory": "humanities",
    "World History": "humanities",
    "World Religions": "humanities",
    
    # Social Sciences
    "Accounting": "social_sciences",
    "Economics": "social_sciences",
    "Education": "social_sciences",
    "Geography": "social_sciences",
    "Government and Politics": "social_sciences",
    "Law": "social_sciences",
    "Management": "social_sciences",
    "Modern Greek Language": "social_sciences",
    
    # STEM
    "Agriculture": "stem",
    "Biology": "stem",
    "Chemistry": "stem",
    "Civil Engineering": "stem",
    "Clinical Knowledge": "stem",
    "Computer Networks & Security": "stem",
    "Computer Science": "stem",
    "Electrical Engineering": "stem",
    "Mathematics": "stem",
    "Medicine": "stem",
    "Physics": "stem",
    
    # Other
    "Driving Rules": "other",
    "General Knowledge": "other",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_yaml_path", default="_default_greekmmlu_qa_template_yaml")
    parser.add_argument("--save_prefix_path", default="greekmmlu_qa")
    parser.add_argument("--data_path", default="/home/mersin-konomi/gmmlu_qa.json")
    return parser.parse_args()


def normalize_subject_name(subject):
    """Convert subject name to valid filename."""
    return subject.lower().replace(" ", "_").replace("&", "and")


if __name__ == "__main__":
    args = parse_args()

    # Get filename of base_yaml so we can `"include":` it in our "other" YAMLs
    base_yaml_name = os.path.split(args.base_yaml_path)[-1]

    # Verify all subjects in our mapping
    eval_logger.info(f"Generating configs for {len(SUBJECTS)} subjects")

    ALL_CATEGORIES = []
    for subject, category in tqdm(SUBJECTS.items(), desc="Generating subject configs"):
        if category not in ALL_CATEGORIES:
            ALL_CATEGORIES.append(category)

        normalized_subject = normalize_subject_name(subject)
        # Use HF config name format (with underscores, matching our push_to_hub config_name)
        hf_config_name = subject.replace(" ", "_").replace("&", "and")

        yaml_dict = {
            "include": base_yaml_name,
            "tag": f"greekmmlu_qa_{category}_tasks",
            "task": f"greekmmlu_qa_{normalized_subject}",
            "task_alias": subject,
            "dataset_name": hf_config_name,
        }

        file_save_path = f"{args.save_prefix_path}_{normalized_subject}.yaml"
        eval_logger.info(f"Saving yaml for subset {subject} to {file_save_path}")
        
        with open(file_save_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(
                yaml_dict,
                yaml_file,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
            )

    # Generate category group files
    for category in ALL_CATEGORIES:
        category_subjects = [
            f"greekmmlu_qa_{normalize_subject_name(subj)}"
            for subj, cat in SUBJECTS.items()
            if cat == category
        ]

        file_save_path = f"_greekmmlu_qa_{category}.yaml"
        eval_logger.info(f"Saving category config for {category} to {file_save_path}")
        
        with open(file_save_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(
                {
                    "group": f"greekmmlu_qa_{category}",
                    "task": category_subjects,
                },
                yaml_file,
                indent=4,
                default_flow_style=False,
            )

    # Generate main benchmark file
    greekmmlu_subcategories = [f"greekmmlu_qa_{category}" for category in ALL_CATEGORIES]

    file_save_path = f"{args.save_prefix_path}.yaml"
    eval_logger.info(f"Saving main benchmark config to {file_save_path}")
    
    with open(file_save_path, "w", encoding="utf-8") as yaml_file:
        yaml.dump(
            {
                "group": "greekmmlu_qa",
                "task": greekmmlu_subcategories,
            },
            yaml_file,
            indent=4,
            default_flow_style=False,
        )

    eval_logger.info("✓ Generation complete!")
