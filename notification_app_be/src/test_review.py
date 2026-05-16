import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ============================================
# 🔹 Set your trained model path
# ============================================
BASE_MODEL_DIR = r"c:\Users\saira\Downloads\codereview-gen\models\final_model_epoch_50"  # <-- Update path here

# Find latest checkpoint if available
subdirs = [d for d in os.listdir(BASE_MODEL_DIR) if d.startswith("final_model_epoch_50")]
if subdirs:
    # sort numerically by checkpoint number and take latest
    latest_checkpoint = sorted(subdirs, key=lambda x: int(x.split("-")[1]))[-1]
    MODEL_DIR = os.path.join(BASE_MODEL_DIR, latest_checkpoint)
else:
    MODEL_DIR = BASE_MODEL_DIR

print(f"🔹 Loading model from: {MODEL_DIR}")

# ============================================
# 🔹 Load Tokenizer & Model
# ============================================
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
except Exception as e:
    raise FileNotFoundError(f"❌ Could not load model from '{MODEL_DIR}'.\nError: {e}")

print("✅ Model and tokenizer loaded successfully!")

# ============================================
# 🔹 Input Code for Review
# ============================================
user_code = """
def init():
     objreg.register('command-history', command_history)
     save_manager.add_saveable('command-history', command_history.save,
                               command_history.changed)


def init_fprompt():
"""

print("\n🔹 Generating AI Review for your code...")

inputs = tokenizer(user_code, return_tensors="pt", truncation=True, padding=True, max_length=512)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        num_beams=5,
        early_stopping=True
    )

review = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\n💡 AI Code Review Suggestion:")
print("--------------------------------------------------")
print(review)
print("--------------------------------------------------")
