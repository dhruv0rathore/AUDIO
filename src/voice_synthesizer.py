# --- PART 3: UPGRADED & HARDENED BARK AUDIO SYNTHESIS ---
from transformers import AutoProcessor, AutoModel
import scipy.io.wavfile
import torch
import numpy as np
import re
from pydub import AudioSegment

print("Loading Bark model (memory-optimized)...")
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Bark processor and model in float16 for memory efficiency
bark_processor = AutoProcessor.from_pretrained("suno/bark")
bark_model = AutoModel.from_pretrained("suno/bark", torch_dtype=torch.float16).to(device)

# --- NEW: Helper function to split long sentences ---
def split_long_sentence(sentence, max_length=150):
    """Splits a long sentence into smaller chunks based on punctuation."""
    chunks = []
    # Split by common punctuation that indicates a natural pause
    parts = re.split(r'([,;.!?—])', sentence)
    current_chunk = ""
    for part in parts:
        if len(current_chunk) + len(part) < max_length:
            current_chunk += part
        else:
            chunks.append(current_chunk.strip())
            current_chunk = part.strip()
    if current_chunk:
        chunks.append(current_chunk.strip())
    return [chunk for chunk in chunks if chunk]


def synthesize_with_bark(processed_data: list[dict], output_filename: str):
    """
    Synthesizes audio using the Bark model with improved stability.
    """
    print(f"Starting audio synthesis with Bark...")
    
    VOICE_CAST = {
        "narration": "v2/en_speaker_6",
        "dialogue": "v2/en_speaker_3"
    }

    final_audio = AudioSegment.empty()
    for i, item in enumerate(processed_data):
        original_sentence = item['sentence']
        sentence_type = item.get('type', 'narration')
        voice_preset = VOICE_CAST.get(sentence_type, VOICE_CAST["narration"])
        
        # Split the sentence if it's too long
        sentence_chunks = split_long_sentence(original_sentence)

        print(f"  Chunk {i+1} ({sentence_type}): Processing {len(sentence_chunks)} sub-chunk(s)...")

        for j, chunk in enumerate(sentence_chunks):
            try:
                inputs = bark_processor(chunk, voice_preset=voice_preset, return_tensors="pt").to(device)
                # Bark generation is slow
                audio_array = bark_model.generate(**inputs, do_sample=True, fine_temperature=0.4, coarse_temperature=0.8)
                
                audio_np = audio_array.cpu().numpy().squeeze()
                sample_rate = bark_model.generation_config.sample_rate
                
                # We need to ensure the audio data is in the correct format for pydub
                audio_np = (audio_np * 32767).astype(np.int16)
                
                # Create audio segment directly in memory
                audio_chunk = AudioSegment(
                    audio_np.tobytes(), 
                    frame_rate=sample_rate,
                    sample_width=audio_np.dtype.itemsize, 
                    channels=1
                )
                final_audio += audio_chunk

            except Exception as e:
                print(f"    ERROR: Bark failed to generate audio for chunk '{chunk}'. Skipping. Error: {e}")
                continue # Skip to the next chunk if one fails

        final_audio += AudioSegment.silent(duration=800) # Add pause after the full sentence

    print("Exporting final Bark audiobook...")
    final_audio.export(output_filename, format="wav")
    print(f"Bark audiobook saved as '{output_filename}'")