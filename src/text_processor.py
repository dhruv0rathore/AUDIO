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

# It's good practice to move this function here from pdf_parser.py
def post_process_text(text: str) -> str:
    print("Post-processing text...")
    text = re.sub(r"([a-zA-Z])-\s([a-zA-Z])", r"\1\2", text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text