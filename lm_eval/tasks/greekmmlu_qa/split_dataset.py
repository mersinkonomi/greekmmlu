"""
Split gmmlu_qa.json into separate files by subject for lm-evaluation-harness.
"""

import json
import os
from collections import defaultdict

# Read the main dataset
input_file = "/home/mersin-konomi/gmmlu_qa.json"
output_dir = "/home/mersin-konomi/model_eval/lm-evaluation-harness/lm_eval/tasks/greekmmlu_qa/data"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Group questions by subject
subjects_data = defaultdict(list)

print("Reading dataset...")
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        doc = json.loads(line)
        subject = doc['subject']
        subjects_data[subject].append(doc)

# Write separate files for each subject
print(f"\\nSplitting into {len(subjects_data)} subject files...")
for subject, docs in subjects_data.items():
    # Normalize subject name for filename
    filename = subject.lower().replace(" ", "_").replace("&", "and") + ".jsonl"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\\n')
    
    print(f"  {subject}: {len(docs)} questions -> {filename}")

print(f"\\n✓ Split complete! Files saved to {output_dir}")
