from __future__ import annotations

from typing import Dict, List

PROMPT = "This is a {subject} question{level_note}. Select the correct answer.\n\nQuestion: {question}\n{choices}\n\nAnswer:"

LEVEL_DISPLAY = {
    "Primary School": "primary school",
    "Secondary School": "secondary school",
    "University": "university level",
    "Professional": "professional level",
    "NA": "",
}

CHOICE_PREFIX = ["A.", "B.", "C.", "D.", "E."]


def _format_level(level: str | None) -> str:
    if not level:
        return ""
    friendly = LEVEL_DISPLAY.get(level, level.lower())
    return "" if not friendly else f" for {friendly}"


def doc_to_text(doc: Dict) -> str:
    subject = doc.get("subject", "Unknown")
    level_note = _format_level(doc.get("level"))
    question = doc.get("question", "").strip()
    if doc.get("context"):
        question = f"{doc['context'].strip()}\n\n{question}"

    choices_lines: List[str] = []
    for idx, choice in enumerate(doc.get("choices", [])):
        prefix = CHOICE_PREFIX[idx] if idx < len(CHOICE_PREFIX) else f"{chr(65 + idx)}."
        choices_lines.append(f"{prefix} {choice}")

    choices_block = "\n".join(choices_lines)
    return PROMPT.format(subject=subject, level_note=level_note, question=question, choices=choices_block)


def doc_to_choice(doc: Dict) -> List[str]:
    return [prefix.split(".")[0] for prefix in CHOICE_PREFIX[: len(doc.get("choices", []))]]


def doc_to_target(doc: Dict) -> str:
    answer_idx = doc.get("answer", 0)
    return doc_to_choice(doc)[answer_idx]
