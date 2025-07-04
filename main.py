from src.book_parser import parse_book
from src.pdf_parser import post_process_text, structure_into_sentences # We can move these later

if __name__ == "__main__":
    print("Audiobook Director AI: System Online.")

    # --- Test with either a PDF or an EPUB ---
    # book_path = "my_book.pdf"
    book_path = "my_book.epub" # Make sure you have an EPUB file to test with

    # Step 1: Parse the book, regardless of format
    raw_text = parse_book(book_path)

    # Step 2: Run the same post-processing and structuring
    processed_text = post_process_text(raw_text)
    sentences = structure_into_sentences(processed_text)

    # --- Verification Step ---
    if sentences:
        print("\n--- First 10 sentences ---")
        for i, sentence in enumerate(sentences[:10]):
            print(f"{i+1}: {sentence}")
    else:
        print("No sentences were extracted.")