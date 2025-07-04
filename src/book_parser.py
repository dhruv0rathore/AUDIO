# src/book_parser.py
import fitz  # PyMuPDF for PDFs
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

def _find_narrative_start(content_chunks: list[str]) -> list[str]:
    """
    A universal helper function to find the start of the main narrative.
    It takes a list of text chunks (chapters from EPUB or blocks from PDF)
    and returns only the chunks that are part of the main story.
    """
    # This regex looks for common start words, followed by roman/arabic numerals or number words.
    # It's case-insensitive. Add more keywords here if you find them.
    start_patterns = [
        r'^(chapter|prologue|epilogue|book|part|section|letter|introduction)\s+([1-9][0-9]*|i|v|x|l|c|d|m|one|two|three|four|five|six|seven|eight|nine|ten)',
        r'^\s*(i|v|x|l|c|d|m|[1-9][0-9]*)\s*$' # Catches lines that are ONLY a chapter number
    ]
    
    start_index = 0
    found_start = False
    
    for i, text in enumerate(content_chunks):
        # We only check the first few characters of each chunk to be efficient
        chunk_to_check = text.strip()[:50]
        for pattern in start_patterns:
            if re.search(pattern, chunk_to_check, re.IGNORECASE):
                start_index = i
                found_start = True
                print(f"Found potential start marker in chunk {i+1} using pattern: '{pattern}'")
                break
        if found_start:
            break

    if not found_start:
        print("Warning: No standard start marker found. The output may contain boilerplate.")
        
    return content_chunks[start_index:]

def _parse_epub(epub_path: str) -> str:
    """Helper function to parse EPUB files."""
    print(f"Parsing EPUB file: {epub_path}")
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        # We get the clean text from each chapter first
        chapters.append(soup.get_text(strip=True, separator=' '))
    
    # Use the universal start-finder to trim boilerplate
    main_content_chapters = _find_narrative_start(chapters)
    return " ".join(main_content_chapters)

def _parse_pdf(pdf_path: str) -> str:
    """Helper function to parse PDF files."""
    print(f"Parsing PDF file: {pdf_path}")
    doc = fitz.open(pdf_path)
    # Get all text blocks first
    blocks = [b[4].replace('\n', ' ') for page in doc for b in page.get_text("blocks")]
    doc.close()
    
    # Use the same universal start-finder to trim boilerplate
    main_content_blocks = _find_narrative_start(blocks)
    return " ".join(main_content_blocks)

# Master parser function - NO CHANGES NEEDED HERE
def parse_book(file_path: str) -> str:
    """
    Master parser function. Detects file type and calls the appropriate parser.
    """
    if file_path.lower().endswith('.pdf'):
        return _parse_pdf(file_path)
    elif file_path.lower().endswith('.epub'):
        return _parse_epub(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")