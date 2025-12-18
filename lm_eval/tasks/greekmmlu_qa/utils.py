"""
Greek MMLU utility functions for formatting questions and choices.
"""

PROMPT = "Ερώτηση: {}\n{}\n\nΑπάντηση:"

# Greek choice labels
LABELS = ["Α.", "Β.", "Γ.", "Δ.", "Ε."]


def doc_to_text(doc):
    """
    Format the question with choices for Greek MMLU.
    
    Args:
        doc: Dictionary with 'question' and 'choices' fields
        
    Returns:
        Formatted question string
    """
    question = doc["question"]
    choices = doc["choices"]
    
    # Format choices with Greek labels
    formatted_choices = []
    for i, choice in enumerate(choices):
        formatted_choices.append(f"{LABELS[i]} {choice}")
    
    choices_text = "\n".join(formatted_choices)
    
    return PROMPT.format(question, choices_text)


def doc_to_choice(doc):
    """
    Extract choice labels based on number of choices.
    
    Args:
        doc: Dictionary with 'choices' field
        
    Returns:
        List of choice labels (e.g., ['Α', 'Β', 'Γ', 'Δ'])
    """
    num_choices = len(doc["choices"])
    return [LABELS[i][0] for i in range(num_choices)]


def filter_by_subject(dataset, subject):
    """
    Filter dataset to only include documents matching the specified subject.
    
    Args:
        dataset: HuggingFace dataset
        subject: Subject name to filter by
        
    Returns:
        Filtered dataset
    """
    return dataset.filter(lambda doc: doc.get("subject") == subject)
