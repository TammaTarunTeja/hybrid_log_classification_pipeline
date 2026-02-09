from sentence_transformers import SentenceTransformer
import numpy as np  
import joblib
model = SentenceTransformer("all-MiniLM-L6-v2")  

lr_model = joblib.load("saved_models/lr_model.joblib")
def get_bert_embedding(log_message):
    embedding = model.encode(log_message)
    return embedding

def bert_classifier(log_message):
    embedding = get_bert_embedding(log_message)
    embedding = embedding.reshape(1, -1)  # Reshape for prediction
    predicted_label = lr_model.predict(embedding)[0]
    probability = lr_model.predict_proba(embedding).max()
    if probability < 0.5:  # Low confidence threshold
        return "Unknown"
    return predicted_label

# sample log messages for testing
if __name__ == "__main__":
    test_logs = [
        "nova.osapi_compute.wsgi.server started successfully.",
        "nova.compute.claims resource allocation failed.",
        "User User123 logged in.",
        "Backup started for server instance 456.",
        "Multiple bad login attempts detected from IP 192.168.1.100.",
    ]
    for log in test_logs:
        label = bert_classifier(log)
        print(f"Log: {log}\nPredicted Label: {label}\n")