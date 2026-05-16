from transformers import TrainingArguments

args = TrainingArguments(
    output_dir="out",
    evaluation_strategy="epoch",
    num_train_epochs=1
)
print("✅ TrainingArguments working fine!")
