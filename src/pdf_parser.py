import fitz  # PyMuPDF
import re

def is_likely_main_content(block_text: str) -> bool:
    """
    A helper function to determine if a text block is likely main content.
    This uses a set of generalized heuristics.
    """
    # Rule 1: Check the word count. Metadata is often short.
    if len(block_text.split()) < 10:
        return False

    # Rule 2: Check for a high ratio of digits or special characters.
    # This helps filter out things like "arXiv:2506.22919v1 [cs.AI]".
    alnum_count = len([char for char in block_text if char.isalnum()])
    total_count = len(block_text)
    if total_count > 0 and (alnum_count / total_count) < 0.6:
        return False
        
    # Rule 3: Main content usually starts with a capital letter.
    if not block_text[0].isupper():
        return False

    # Rule 4: Main content usually ends with punctuation.
    if block_text.strip()[-1] not in ".?!":
        return False

    # If it passes all checks, it's likely main content.
    return True

def extract_text_from_book(pdf_path: str) -> str:
    """
    Extracts text by using a content-aware filter to keep only main body text,
    then sorting the blocks to maintain reading order.
    """
    print(f"Starting GENERALIZED text extraction from '{pdf_path}'...")
    doc = fitz.open(pdf_path)
    
    main_content_blocks = []
    for page in doc:
        page_blocks = page.get_text("blocks")
        for b in page_blocks:
            block_text = b[4].strip()
            # Use our intelligent filter to decide whether to keep the block
            if is_likely_main_content(block_text):
                main_content_blocks.append(block_text.replace('\n', ' '))

    doc.close()
    
    # Join the clean, main content blocks into a single string
    full_text = " ".join(main_content_blocks)
    
    print("Generalized text extraction complete.")
    return full_text

def post_process_text(text: str) -> str:
    """
    Performs final cleanup on the joined text, like fixing hyphenation.
    """
    print("Post-processing text...")
    text = re.sub(r"([a-zA-Z])-\s([a-zA-Z])", r"\1\2", text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def structure_into_sentences(text: str) -> list[str]:
    """
    Splits the final, clean text into a list of sentences.
    """
    # A delayed import to avoid issues if nltk isn't installed for some reason
    from nltk.tokenize import sent_tokenize
    print("Structuring text into sentences...")
    sentences = sent_tokenize(text)
    print(f"Successfully structured text into {len(sentences)} sentences.")
    return sentences