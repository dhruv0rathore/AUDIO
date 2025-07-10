from src.book_parser import parse_book
from src.pdf_parser import post_process_text, structure_into_sentences # We can move these later
from src.emotion_classifier import classify_emotions
from src.voice_synthesizer import synthesize_audio

if __name__ == "__main__":
    print("Audiobook Director AI: System Online.")

    # --- Test with either a PDF or an EPUB ---
    # book_path = "my_book.pdf"
    book_path = "my_book.epub" # Make sure you have an EPUB file to test with

    # Step 1: Parse the book, regardless of format
    raw_text = parse_book(book_path)

    # Step 2: Run the same post-processing and structuring
    processed_text = post_process_text(raw_text)

    # Step 3: Structure into sentences
    sentences = structure_into_sentences(processed_text)

    # Step 4: Classify emotions
    classified_sentences = classify_emotions(sentences[:20])


    # --- Verification Step ---
    if classified_sentences:
        print("\n--- First 5 Sentences with Emotion Classification ---")
        for item in classified_sentences[:5]:
            # Print in a nice, readable format
            print(f"  Sentence: \"{item['sentence']}\"")
            print(f"  Emotion: {item['emotion']} (Score: {item['score']:.2f})")
            print("-" * 20)


    print("\n--- Starting Phase 3: Audio Synthesis ---")
    synthesize_audio(classified_sentences, "output_audiobook.wav")