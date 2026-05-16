import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Absolute path to your trained model folder
model_path = "C:/Users/saira/Downloads/codereview-gen/models"

# Load tokenizer and model
print("[INFO] Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()
print("[INFO] Model loaded successfully.\n")

# Prediction loop
while True:
    text = input("Enter code review text (or 'exit' to quit): ")
    if text.lower() == "exit":
        print("Exiting...")
        break

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    
    print(f"[RESULT] Predicted class: {predicted_class}\n")
