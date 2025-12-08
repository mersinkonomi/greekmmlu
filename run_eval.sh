#!/bin/bash
# chmod +x /datalake/datastore1/yang/el_llm/run_eval.sh

# Configuration
CACHE_DIR="/home/mersin-konomi/cache"
OUTPUT_PATH="/home/mersin-konomi/eval_results"
WORK_DIR="/home/mersin-konomi/model_eval/lm-evaluation-harness"

# Create cache directory if it doesn't exist
mkdir -p "$CACHE_DIR"

# Define models to test (only Meltemi models)
declare -a MODELS=(
    "ilsp/Meltemi-7B-v1"
    # "ilsp/Meltemi-7B-v1.5"
    "ilsp/Meltemi-7B-Instruct-v1.5"
)

# Define tasks with their few-shot settings (only dascim_all)
# Format: "task_name:few_shot_count"
declare -a TASKS=(
    "dascim_all:0"
    "dascim_all:5"
    "dascim_all:25"
)

echo "Starting evaluation for ${#MODELS[@]} model(s)"
echo "Cache directory: $CACHE_DIR"
echo "Output path: $OUTPUT_PATH"
echo "================================================"

# Run evaluation for each model
for MODEL_NAME in "${MODELS[@]}"; do
    echo "Starting evaluation for model: $MODEL_NAME"
    echo "================================================"
    
    # Run evaluation for each task with its specific few-shot setting
    for task_config in "${TASKS[@]}"; do
        # Split task name and few-shot count
        IFS=':' read -r task_name few_shot <<< "$task_config"
        
        echo "Running $task_name with $few_shot few-shot examples..."
        
        # Build and run the command
        # Using single GPU (cuda:0)
        cd "$WORK_DIR"
        CUDA_LAUNCH_BLOCKING=1 python3 -m lm_eval \
            --model hf \
            --model_args "pretrained=$MODEL_NAME,cache_dir=$CACHE_DIR" \
            --tasks "$task_name" \
            --batch_size 1 \
            --trust_remote_code \
            --num_fewshot "$few_shot" \
            --output_path "$OUTPUT_PATH" \
            --device cuda:0 \
            --log_samples
        
        if [ $? -ne 0 ]; then
            echo "Error: Evaluation failed for task $task_name on model $MODEL_NAME"
            exit 1
        fi
        
        echo "Completed $task_name for $MODEL_NAME"
        echo "--------------------------------"
    done
    
    echo "Completed all tasks for model: $MODEL_NAME"
    echo "================================================"
done

echo "All evaluations completed successfully for all models!"

# bash /datalake/datastore1/yang/el_llm/run_eval.sh