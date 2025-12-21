"""
Greek MMLU utility functions for formatting questions and choices.
"""

PROMPT = "Αυτό είναι μια ερώτηση {}. Επίλεξε τη σωστή απάντηση!\n\nΕρώτηση: {}\n{}\n\n Απάντηση:"


# subjects_gr
subjects_gr = {
    "Economics": "Οικονομικών",
    "Education": "Παιδαγωγικής",
    "Medicine": "Ιατρικής",
    "Electrical Engineering": "Ηλεκτρολόγων Μηχανικών",
    "Greek Mythology": "Ελληνικής Μυθολογίας",
    "Computer Networks & Security": "Δικτύων Υπολογιστών και Ασφάλειας",
    "Law": "Νομικής",
    "Physics": "Φυσικής",
    "Government and Politics": "Διακυβέρνησης και Πολιτικής",
    "Art": "Τέχνης",
    "Greek Literature": "Νεοελληνικής Λογοτεχνίας",
    "World History": "Παγκόσμιας Ιστορίας",
    "General Knowledge": "Γενικών Γνώσεων",
    "World Religions": "Παγκόσμιων Θρησκειών",
    "Mathematics": "Μαθηματικών",
    "Clinical Knowledge": "Κλινικών Γνώσεων",
    "Driving Rules": "Κανόνων Οδικής Κυκλοφορίας",
    "Biology": "Βιολογίας",
    "Civil Engineering": "Πολιτικών Μηχανικών",
    "Computer Science": "Επιστήμης Υπολογιστών",
    "Geography": "Γεωγραφίας",
    "Chemistry": "Χημείας",
    "Prehistory": "Προϊστορίας",
    "Agriculture": "Γεωργίας",
    "Modern Greek Language": "Νεοελληνικής Γλώσσας",
    "Accounting": "Λογιστικής",
    "Greek History": "Ελληνικής Ιστορίας",
    "Management": "Διοίκησης Επιχειρήσεων",
    "Greek Traditions": "Ελληνικών Παραδόσεων",
}



# Greek choice labels
LABELS = ["Α.", "Β.", "Γ.", "Δ."]


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
    subject = doc["subject"]
    
    # Convert English subject to Greek
    subject_gr = subjects_gr.get(subject, subject)
    
    # Format choices with Greek labels
    formatted_choices = []
    for i, choice in enumerate(choices):
        formatted_choices.append(f"{LABELS[i]} {choice}")
    
    choices_text = "\n".join(formatted_choices)
    
    return PROMPT.format(subject_gr, question, choices_text)


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


def doc_to_target(doc):
    """
    Return the correct answer letter for exact_match comparison.
    
    Args:
        doc: Dictionary with 'answer' field (0-indexed)
        
    Returns:
        The correct answer letter (e.g., 'Α', 'Β', 'Γ', 'Δ')
    """
    return LABELS[doc["answer"]][0]


def process_results(doc, results):
    """
    Process results for generate_until format (API compatibility).
    
    Args:
        doc: Dictionary with document data including 'answer' field
        results: List containing the model's generated response
        
    Returns:
        Dictionary with accuracy metric
    """
    # Get the model's prediction and clean it
    pred = results[0].strip().upper()
    
    # Extract just the letter (Α, Β, Γ, Δ) from the prediction
    # Handle cases like "Α.", "Α ", "α", etc.
    if pred and pred[0] in ["Α", "Β", "Γ", "Δ", "A", "B", "C", "D"]:
        pred_letter = pred[0]
        # Map English to Greek if needed
        if pred_letter in ["A", "B", "C", "D"]:
            mapping = {"A": "Α", "B": "Β", "C": "Γ", "D": "Δ"}
            pred_letter = mapping[pred_letter]
    else:
        pred_letter = ""
    
    # Get the correct answer
    gold = LABELS[doc["answer"]][0]  # "Α", "Β", "Γ", or "Δ"
    
    # Return accuracy
    return {"acc": 1.0 if pred_letter == gold else 0.0}
