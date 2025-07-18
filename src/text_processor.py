# src/text_processor.py
import re

def tag_sentence_types(sentences: list[str]) -> list[dict]:
    """Tags each sentence as either 'narration' or 'dialogue'."""
    print("Tagging sentence types...")
    structured_data = []
    for sentence in sentences:
        # Simple rule: if a sentence is wrapped in quotes, it's dialogue.
        if sentence.strip().startswith('"') and sentence.strip().endswith('"'):
            sentence_type = "dialogue"
            sentence_content = sentence.strip()[1:-1] # Remove the quotes
        else:
            sentence_type = "narration"
            sentence_content = sentence
        
        structured_data.append({"sentence": sentence_content, "type": sentence_type})
    return structured_data

def post_process_text(text: str) -> str:
    # Fix words broken by hyphenation
    text = re.sub(r"([a-zA-Z])-\s([a-zA-Z])", r"\1\2", text)
    
    # --- NEW: Convert long dashes to commas for a natural pause ---
    text = re.sub(r"—|–|--", ", ", text)

    # Collapse multiple whitespace characters
    text = re.sub(r'\s+', ' ', text).strip()
    return text