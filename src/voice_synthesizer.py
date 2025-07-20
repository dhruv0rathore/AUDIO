from bark import SAMPLE_RATE, generate_audio
from pydub import AudioSegment
import numpy as np

def synthesize_with_bark(processed_data: list[dict], output_filename: str):
    """
    Synthesizes audio using the OFFICIAL Bark model.
    """
    print(f"Starting audio synthesis with official Bark...")
    
    VOICE_CAST = {
        "narration": "v2/en_speaker_6",
        "dialogue": "v2/en_speaker_3"
    }
    final_audio = AudioSegment.empty()

    for i, item in enumerate(processed_data):
        voice_preset = VOICE_CAST.get(item['type'], VOICE_CAST["narration"])
        sentence = item['sentence']
        
        # Add a text prompt for a non-speech sound for fun, Bark's specialty
        if item['emotion'] == 'sadness' and np.random.rand() < 0.2: # 20% chance on sad lines
            sentence = "[sighs] " + sentence
            
        print(f"  Chunk {i+1} ({item['type']}): Synthesizing with preset {voice_preset}...")
        
        try:
            # Use the official 'generate_audio' function
            audio_array = generate_audio(sentence, history_prompt=voice_preset, silent=True)
            
            # Convert to a format pydub can handle
            audio_np = (audio_array * 32767).astype(np.int16)
            audio_chunk = AudioSegment(
                data=audio_np.tobytes(),
                sample_width=2, # 16-bit audio
                frame_rate=SAMPLE_RATE,
                channels=1
            )
            final_audio += audio_chunk
            final_audio += AudioSegment.silent(duration=800)
        except Exception as e:
            print(f"    ERROR: Bark failed on chunk {i+1}. Skipping. Error: {e}")
    
    final_audio.export(output_filename, format="wav")
    print(f"Bark audiobook saved as '{output_filename}'")