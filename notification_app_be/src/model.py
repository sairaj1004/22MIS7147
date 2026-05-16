# src/model.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "Salesforce/codet5-small"  # You can later switch to codet5-base or codet5p-220m

def load_model():
    """
    Load the tokenizer and model for code review generation.
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model
