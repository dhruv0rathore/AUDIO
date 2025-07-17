from TTS.api import TTS
import torch
from pydub import AudioSegment
import os

# Use CUDA if available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

#print("Loading TTS model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
tts_model = TTS("tts_models/en/vctk/vits").to(device)

# Replace your old synthesizer function with this one

def synthesize_multi_voice_audio(tts_model, processed_data: list[dict], output_filename: str):
    """
    Synthesizes audio using different built-in speakers for narration and dialogue.
    """
    print(f"Starting multi-speaker audio synthesis with VITS...")
    
    # --- NEW: Create a Voice Cast using speaker IDs ---
    # Pick any two different speaker IDs from the list you just printed
    VOICE_CAST = {
        "narration": "p227",  # A standard male voice
        "dialogue": "p232"   # A different male voice
    }

    final_audio = AudioSegment.empty()
    for i, item in enumerate(processed_data):
        temp_filename = f"temp_chunk_{i}.wav"
        
        # --- NEW: Speaker Selection Logic ---
        speaker_id = VOICE_CAST.get(item['type'], VOICE_CAST["narration"])
        print(f"  Chunk {i+1} ({item['type']}): Synthesizing with speaker {speaker_id}...")
            
        # --- THE FIX: Use the 'speaker' argument, not 'speaker_wav' ---
        tts_model.tts_to_file(
            text=item['sentence'],
            file_path=temp_filename,
            speaker=speaker_id # Use the selected speaker ID
        )
        
        audio_chunk = AudioSegment.from_wav(temp_filename)
        final_audio += audio_chunk
        os.remove(temp_filename)

    print("Exporting final audiobook...")
    final_audio.export(output_filename, format="wav")
    print(f"Multi-voice audiobook saved as '{output_filename}'")