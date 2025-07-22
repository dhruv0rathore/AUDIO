from bark import SAMPLE_RATE, generate_audio
from pydub import AudioSegment
import numpy as np

def synthesize_with_emotion_prompts(processed_data: list[dict], output_filename: str):
    """
    Synthesizes audio using Bark by prepending emotion tags as performance prompts.
    """
    print(f"Starting audio synthesis with Bark and emotional prompts...")

    # We can use one consistent, high-quality voice preset for the entire book
    base_voice_preset = "v2/en_speaker_6" 

    final_audio = AudioSegment.empty()
    for i, item in enumerate(processed_data):
        sentence = item['sentence']
        emotion = item.get('emotion', 'neutral').lower() # Get emotion, default to neutral

        # --- The New Prompting Logic ---
        # We only add a prompt if the emotion is not neutral
        if emotion != 'neutral':
            text_to_generate = f"[{emotion}] {sentence}"
        else:
            text_to_generate = sentence

        print(f"  Chunk {i+1} (Prompt: [{emotion}]): Synthesizing...")

        try:
            # Generate audio using the new text prompt
            audio_array = generate_audio(text_to_generate, history_prompt=base_voice_preset, silent=True)

            # Convert to a format pydub can handle
            audio_np = (audio_array * 32767).astype(np.int16)
            audio_chunk = AudioSegment(
                data=audio_np.tobytes(),
                sample_width=2,
                frame_rate=SAMPLE_RATE,
                channels=1
            )
            final_audio += audio_chunk
            final_audio += AudioSegment.silent(duration=800)
        except Exception as e:
            print(f"    ERROR: Bark failed on chunk {i+1}. Skipping. Error: {e}")

    final_audio.export(output_filename, format="wav")
    print(f"Bark audiobook saved as '{output_filename}'")