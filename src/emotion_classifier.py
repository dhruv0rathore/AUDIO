from transformers import pipeline

# --- IMPORTANT ---
# Replace this with your actual Hugging Face model repository name
MODEL_REPO_ID = "rememberme4ever/emotion-classifier-frankenstein"
# ---

# We initialize the pipeline here. The first time this runs, 
# it will download the model from the Hub. Subsequent runs will use the cached version.
print("Loading emotion classification model...")
classifier = pipeline("text-classification", model=MODEL_REPO_ID)

# The mapping from label ID to emotion name
# This must match the order from our training dataset
EMOTION_LABELS = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

def classify_emotions(sentences: list[str]) -> list[dict]:
    """
    Classifies a list of sentences, returning a list of dictionaries 
    with the sentence, predicted emotion, and confidence score.
    """
    print(f"Classifying emotions for {len(sentences)} sentences...")
    # The pipeline can process a list of sentences much more efficiently than one by one
    results = classifier(sentences)

    # Map the numeric labels (e.g., "LABEL_1") to human-readable names
    for result in results:
        label_id = int(result['label'].split('_')[1])
        result['emotion'] = EMOTION_LABELS[label_id]

    # Combine the original sentence with its prediction
    # (This is a more structured way to return the data)
    output = []
    for sentence, result in zip(sentences, results):
        output.append({
            "sentence": sentence,
            "emotion": result['emotion'],
            "score": result['score']
        })

    print("Classification complete.")
    return output