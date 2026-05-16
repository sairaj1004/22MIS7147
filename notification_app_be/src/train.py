import os
import sys
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
)

# -----------------------------
# 1️⃣ Configuration
# -----------------------------
MODEL_NAME = "Salesforce/codet5-small"
DATA_FILE = "data/raw/code_review_data.csv"  # Your downloaded CSV
OUTPUT_DIR = "models"
LOG_DIR = "logs"
MAX_LENGTH = 256
EPOCHS = 3
BATCH_SIZE = 2
LR = 5e-5

# -----------------------------
# 2️⃣ Create folders if missing
# -----------------------------
for folder in [OUTPUT_DIR, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)

# -----------------------------
# 3️⃣ Load CSV dataset
# -----------------------------
print("🔹 Loading CSV dataset...")
if not os.path.exists(DATA_FILE):
    print(f"⚠️ CSV file not found: {DATA_FILE}")
    sys.exit(1)

df = pd.read_csv(DATA_FILE)

# Rename columns to match code & review
if "patch" in df.columns and "responce" in df.columns:
    df = df.rename(columns={"patch": "code", "responce": "review"})
else:
    print("⚠️ CSV must contain 'patch' and 'responce' columns.")
    print(f"Columns found: {df.columns.tolist()}")
    sys.exit(1)

# Drop rows with missing code or review
df = df.dropna(subset=["code", "review"]).reset_index(drop=True)
print(f"✅ CSV loaded with {len(df)} examples.")

# Convert to HuggingFace Dataset
dataset = Dataset.from_pandas(df)

# Split into train/validation
dataset = dataset.train_test_split(test_size=0.1)
train_dataset = dataset["train"]
val_dataset = dataset["test"]

# -----------------------------
# 4️⃣ Load tokenizer & model
# -----------------------------
print("🔹 Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# -----------------------------
# 5️⃣ Preprocess (tokenize)
# -----------------------------
def preprocess_function(examples):
    # Ensure all inputs are strings
    codes = [str(c) for c in examples["code"]]
    reviews = [str(r) for r in examples["review"]]

    # Tokenize code (inputs)
    model_inputs = tokenizer(
        codes,
        max_length=MAX_LENGTH,
        truncation=True,
        padding="max_length",
    )

    # Tokenize review (labels)
    labels = tokenizer(
        reviews,
        max_length=MAX_LENGTH,
        truncation=True,
        padding="max_length",
    )

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

print("🔹 Tokenizing dataset...")
tokenized_train = train_dataset.map(preprocess_function, batched=True)
tokenized_val = val_dataset.map(preprocess_function, batched=True)

# -----------------------------
# 6️⃣ Setup training
# -----------------------------
print("🔹 Preparing training arguments...")
args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    learning_rate=LR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    weight_decay=0.01,
    save_strategy="epoch",
    logging_dir=LOG_DIR,
    logging_steps=10,
    evaluation_strategy="epoch",
    report_to="none",
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# -----------------------------
# 7️⃣ Train model
# -----------------------------
print("🚀 Starting training...")
trainer.train()

# -----------------------------
# 8️⃣ Save model & tokenizer
# -----------------------------
print("💾 Saving model and tokenizer...")
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"✅ Training complete! Model and tokenizer saved to '{OUTPUT_DIR}'")
