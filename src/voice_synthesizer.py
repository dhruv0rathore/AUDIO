# --- PART 3: NEW BARK AUDIO SYNTHESIS ---
from transformers import AutoProcessor, AutoModel
import scipy.io.wavfile

print("Loading Bark model...")
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Bark processor and model
bark_processor = AutoProcessor.from_pretrained("suno/bark")
bark_model = AutoModel.from_pretrained("suno/bark").to(device)

def synthesize_with_bark(processed_data: list[dict], output_filename: str):
    """
    Synthesizes audio using the Bark model with different voice presets.
    """
    print(f"Starting audio synthesis with Bark...")

    # --- Bark Voice Cast ---
    # We choose different built-in presets for different roles
    VOICE_CAST = {
        "narration": "v2/en_speaker_6", # A good male narrator voice
        "dialogue": "v2/en_speaker_3"  # A different female voice for dialogue
    }

    final_audio = AudioSegment.empty()
    for i, item in enumerate(processed_data):
        sentence = item['sentence']
        sentence_type = item.get('type', 'narration')

        # Select the voice preset
        voice_preset = VOICE_CAST.get(sentence_type, VOICE_CAST["narration"])

        print(f"  Chunk {i+1} ({sentence_type}): Synthesizing with preset {voice_preset}...")

        # Process the text and generate audio
        inputs = bark_processor(sentence, voice_preset=voice_preset, return_tensors="pt").to(device)
        # NOTE: Bark generation is slow. This next line will take time.
        audio_array = bark_model.generate(**inputs, do_sample=True, fine_temperature=0.4, coarse_temperature=0.8)

        # Get the audio data and sample rate
        audio_np = audio_array.cpu().numpy().squeeze()
        sample_rate = bark_model.generation_config.sample_rate

        # Save to a temporary file
        temp_filename = f"temp_chunk_{i}.wav"
        scipy.io.wavfile.write(temp_filename, rate=sample_rate, data=audio_np)

        # Stitch the audio
        audio_chunk = AudioSegment.from_wav(temp_filename)
        final_audio += audio_chunk
        final_audio += AudioSegment.silent(duration=800)
        os.remove(temp_filename)

    print("Exporting final Bark audiobook...")
    final_audio.export(output_filename, format="wav")
    print(f"Bark audiobook saved as '{output_filename}'")