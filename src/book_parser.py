# src/book_parser.py
import fitz  # PyMuPDF for PDFs
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import pdfplumber
import mobi

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
    """A more robust PDF parser using pdfplumber to analyze layouts."""
    print(f"Parsing PDF with advanced layout analysis: {pdf_path}")
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Filter out text in the top 15% (headers) and bottom 10% (footers) of the page
            main_content = page.filter(lambda obj: obj["top"] > page.height * 0.15 and obj["bottom"] < page.height * 0.90)
            full_text += main_content.extract_text() + " "

    # We can still use our start-finder on this cleaner text
    text_chunks = [full_text] # Simplified for this example
    main_narrative = _find_narrative_start(text_chunks)
    return " ".join(main_narrative)

def _parse_mobi(mobi_path: str) -> str:
    """Helper function to parse MOBI/AZW3 files."""
    print(f"Parsing MOBI file: {mobi_path}")
    content = []
    # The mobi library gives us the content as raw records
    temp_dir, _ = mobi.extract(mobi_path)
    for _, record in mobi.Mobi(temp_dir).read_records():
         # Basic cleaning to remove HTML tags
        cleaned_record = re.sub('<[^<]+?>', '', record)
        content.append(cleaned_record)
    return " ".join(content)

# Master parser function - NO CHANGES NEEDED HERE
def parse_book(file_path: str) -> str:
    print(f"Parsing book: {file_path}")
    file_ext = file_path.lower().split('.')[-1]

    if file_ext == 'pdf':
        return _parse_pdf(file_path)
    elif file_ext == 'epub':
        return _parse_epub(file_path)
    elif file_ext in ['mobi', 'azw3']:
        return _parse_mobi(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")