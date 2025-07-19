from transformers import pipeline

# --- IMPORTANT ---
# Replace this with your actual Hugging Face model repository name
MODEL_REPO_ID = "rememberme4ever/emotion_classifier_v2"
# ---

# We initialize the pipeline here. The first time this runs, 
# it will download the model from the Hub. Subsequent runs will use the cached version.
print("Loading emotion classification model...")
classifier = pipeline("text-classification", model=MODEL_REPO_ID)

# The mapping from label ID to emotion name
# This must match the order from our training dataset
EMOTION_LABELS = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 
    'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval', 
    'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 
    'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 
    'relief', 'remorse', 'sadness', 'surprise', 'neutral'
]

def classify_emotions(typed_sentences: list[dict]) -> list[dict]:
    print(f"Classifying emotions for {len(typed_sentences)} sentences...")
    
    # Extract just the sentence text for the pipeline
    sentence_texts = [item['sentence'] for item in typed_sentences]
    results = classifier(sentence_texts)
    
    # Add the emotion data back to our original structure
    for i, item in enumerate(typed_sentences):
        result = results[i]
        label_id = int(result['label'].split('_')[1])
        item['emotion'] = EMOTION_LABELS[label_id]
        item['score'] = result['score']
            
    print("Classification complete.")
    return typed_sentences