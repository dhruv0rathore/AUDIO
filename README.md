# 🎧 AUDIO

**Transform any book into an emotionally expressive audiobook**

AUDIO is an end-to-end pipeline that reads an EPUB (or PDF), understands the emotional tone of every sentence, and synthesizes natural, expressive speech using [Bark](https://github.com/suno-ai/bark) — Suno's open-source text-to-audio model. The result is not a flat, monotone text-to-speech dump. It's a *directed performance*, where the AI acts as both the narrator and the director.

---

## ✨ What Makes This Different

Traditional TTS reads text. **AUDIO *interprets* it.**

| Feature | Traditional TTS | AUDIO |
|---|---|---|
| Emotional awareness | ❌ None | ✅ 28 emotion classes per sentence |
| Dialogue detection | ❌ None | ✅ Narration vs. dialogue tagging |
| Voice direction | ❌ Flat, monotone | ✅ Emotion-prompted synthesis |
| Book format support | ❌ Plain text only | ✅ EPUB, PDF, MOBI/AZW3 |
| Boilerplate filtering | ❌ Reads everything | ✅ Intelligent narrative start detection |

---

## 🏗️ Architecture

The pipeline has three distinct phases:

```
┌─────────────────────────────────────────────────────────┐
│                     PHASE 1: PARSING                    │
│  EPUB/PDF/MOBI → Raw Text → Clean Text → Sentences     │
│  • Boilerplate removal (TOC, copyright, headers)        │
│  • Hyphenation repair & dash normalization              │
│  • NLTK sentence tokenization                          │
│  • Dialogue vs. narration tagging                       │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  PHASE 2: AI CLASSIFICATION             │
│  Each sentence → Emotion label + confidence score       │
│  • Fine-tuned DistilBERT classifier                     │
│  • 28 emotion classes (joy, fear, anger, love, ...)     │
│  • Hosted on Hugging Face Hub                           │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 PHASE 3: AUDIO SYNTHESIS                │
│  Emotion-tagged sentences → Expressive speech → .wav    │
│  • Bark TTS with emotion prompt prefixing               │
│  • Consistent voice preset (v2/en_speaker_6)            │
│  • Natural pauses between sentences (800ms)             │
│  • GPU-accelerated generation                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start — Google Colab (Recommended)

The fastest way to run this project — no local setup required.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dhruv0rathore/AUDIO/blob/master/Audiobook_Director_AI.ipynb)

1. Click the badge above (or open `Audiobook_Director_AI.ipynb` in Colab)
2. Set runtime to **T4 GPU** (`Runtime → Change runtime type → T4 GPU`)
3. Run all cells — upload your `.epub` when prompted
4. Download your generated `.wav` audiobook

---

## 💻 Local Setup

### Prerequisites

- Python 3.11+
- CUDA-compatible GPU (strongly recommended)
- ~4 GB disk space for Bark model weights

### Installation

```bash
git clone https://github.com/dhruv0rathore/AUDIO.git
cd AUDIO

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
pip install git+https://github.com/suno-ai/bark.git
python download_nltk.py
```

### Usage

Place your book file in the project root as `my_book.epub`, then:

```bash
python main.py
```

The pipeline will process the first 10 sentences and output `final_prompted_audiobook.wav`.

---

## 📁 Project Structure

```
AUDIO/
├── main.py                          # Entry point — orchestrates the full pipeline
├── my_book.epub                     # Your input book (not tracked in git)
├── requirements.txt                 # Python dependencies
├── download_nltk.py                 # One-time NLTK data setup
├── Audiobook_Director_AI.ipynb      # Google Colab notebook
└── src/
    ├── book_parser.py               # EPUB / PDF / MOBI parsing & boilerplate removal
    ├── text_processor.py            # Text cleanup, dash normalization, dialogue tagging
    ├── pdf_parser.py                # Sentence tokenization (NLTK) & content filtering
    ├── emotion_classifier.py        # HuggingFace emotion classification (28 classes)
    └── voice_synthesizer.py         # Bark TTS with emotion-prompted synthesis
```

---

## 🧠 Emotion Classification

The classifier is a fine-tuned DistilBERT model hosted on Hugging Face Hub:

**[`rememberme4ever/emotion_classifier_v2`](https://huggingface.co/rememberme4ever/emotion_classifier_v2)**

It classifies text into **28 emotion categories**:

> admiration · amusement · anger · annoyance · approval · caring · confusion · curiosity · desire · disappointment · disapproval · disgust · embarrassment · excitement · fear · gratitude · grief · joy · love · nervousness · optimism · pride · realization · relief · remorse · sadness · surprise · neutral

Non-neutral emotions are prepended as `[emotion]` tags to guide Bark's synthesis toward the appropriate tone.

---

## 🎙️ Voice Synthesis

Audio is generated using [Bark](https://github.com/suno-ai/bark) by Suno AI — a transformer-based text-to-audio model capable of producing highly natural speech with emotional variation. The system:

- Uses a consistent voice preset (`v2/en_speaker_6`) across all sentences for narrator continuity
- Prepends emotion tags (e.g., `[excitement] The door flew open!`) to guide vocal expression
- Inserts 800ms silent pauses between sentences for natural pacing
- Exports the final concatenated audio as a standard `.wav` file

---

## ⚠️ Known Limitations

- **Bark is slow on CPU.** GPU is strongly recommended — a T4 can synthesize ~10 sentences in a few minutes.
- **Long sentences may be truncated.** Bark has a token limit per generation; very long sentences may get cut off.
- **Voice consistency is approximate.** Bark's voice presets produce similar but not identical voices across generations.
- **Emotion prompting is heuristic.** Bark wasn't explicitly trained on `[emotion]` tags, but they meaningfully influence output tone in practice.

---

## 🗺️ Roadmap

- [ ] Chapter-aware synthesis with configurable chapter breaks
- [ ] Multi-voice support (different voices for dialogue vs. narration)
- [ ] Speaker diarization for multi-character scenes
- [ ] Real-time streaming synthesis
- [ ] Fine-tuned Bark model for audiobook narration style
- [ ] Web UI for upload, preview, and download

---

## 📄 License

This project is for educational and research purposes.

---

<p align="center">
  <i>Built with 🎵 by <a href="https://github.com/dhruv0rathore">Dhruv Rathore</a></i>
</p>
