
from src.book_parser import parse_book
from src.text_processor import post_process_text, tag_sentence_types
from src.pdf_parser import structure_into_sentences
from src.emotion_classifier import classify_emotions
from src.voice_synthesizer import synthesize_multi_voice_audio, tts_model

if __name__ == "__main__":
    print("Audiobook Director AI: System Online.")
    book_path = "my_book.epub"

    # --- Phase 1: Parsing, Cleaning, and Structuring ---
    raw_text = parse_book(book_path)
    processed_text = post_process_text(raw_text)
    sentences = structure_into_sentences(processed_text)
    
    # NEW: Tag sentences as narration or dialogue
    typed_data = tag_sentence_types(sentences)

    # --- Phase 2: AI Classification ---
    # We now pass the structured data to the classifier
    final_data = classify_emotions(typed_data)
    
    # Process first 20 for a quick test
    data_to_synthesize = final_data[:20]

    # --- Verification Step ---
    print("\n--- First 5 Processed Sentences ---")
    for item in data_to_synthesize[:5]:
        print(f"  Type: {item['type']}")
        print(f"  Sentence: \"{item['sentence']}\"")
        print(f"  Emotion: {item['emotion']} (Score: {item['score']:.2f})")
        print("-" * 20)

    print("\n--- Starting Phase 3: Audio Synthesis ---")
synthesize_multi_voice_audio(tts_model, data_to_synthesize, "output_multivoice_audiobook.wav")

print("\n--- Project Complete ---")