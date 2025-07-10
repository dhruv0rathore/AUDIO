from TTS.api import TTS
import torch
from pydub import AudioSegment
import os

# Use CUDA if available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize the TTS model
# This will download the model files on the first run
print("Loading TTS model...")
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)

def synthesize_audio(classified_sentences: list[dict], output_filename: str = "final_audiobook.wav"):
    """
    Synthesizes audio from a list of sentences and saves it to a single file.
    """
    print(f"Starting audio synthesis for {len(classified_sentences)} sentences...")
    temp_files = []

    # For now, we will generate all audio in the same voice.
    # The next step would be to use the 'emotion' tag to change the speaker or style.
    for i, item in enumerate(classified_sentences):
        sentence = item['sentence']
        temp_filename = f"temp_chunk_{i}.wav"

        # Generate audio for the sentence and save to a temporary file
        print(f"  Synthesizing chunk {i+1}/{len(classified_sentences)}...")
        tts.tts_to_file(text=sentence, file_path=temp_filename)
        temp_files.append(temp_filename)

    # Stitch all the temporary audio files together
    print("Stitching audio chunks into final audiobook...")
    combined_audio = AudioSegment.empty()
    for file in temp_files:
        chunk = AudioSegment.from_wav(file)
        combined_audio += chunk

    # Export the final combined audio
    combined_audio.export(output_filename, format="wav")
    print(f"Final audiobook saved as '{output_filename}'")

    # Clean up temporary files
    print("Cleaning up temporary files...")
    for file in temp_files:
        os.remove(file)

    print("Audio synthesis complete.")