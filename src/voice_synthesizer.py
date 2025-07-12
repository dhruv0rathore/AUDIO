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

def synthesize_multi_voice_audio(processed_data: list[dict], output_filename: str):
    """Synthesizes audio using different voices for narration and dialogue."""
    print(f"Starting multi-voice audio synthesis...")
    
    narrator_wav = "narrator_voice.wav"
    character_wav = "character_voice.wav"
    
    if not os.path.exists(narrator_wav) or not os.path.exists(character_wav):
        raise FileNotFoundError("Make sure 'narrator_voice.wav' and 'character_voice.wav' are uploaded to the session.")

    final_audio = AudioSegment.empty()
    for i, item in enumerate(processed_data):
        temp_filename = f"temp_chunk_{i}.wav"
        
        speaker_ref = narrator_wav if item['type'] == 'narration' else character_wav
        print(f"  Chunk {i+1} ({item['type']}): Synthesizing...")
            
        tts_model.tts_to_file(
            text=item['sentence'],
            file_path=temp_filename,
            speaker_wav=speaker_ref,
            language="en"
        )
        
        audio_chunk = AudioSegment.from_wav(temp_filename)
        final_audio += audio_chunk
        os.remove(temp_filename)

    print("Exporting final audiobook...")
    final_audio.export(output_filename, format="wav")
    print(f"Multi-voice audiobook saved as '{output_filename}'")