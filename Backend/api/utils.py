from transformers import pipeline

def load_model_and_tokenizer(model_path):
    return pipeline("text-classification", model=model_path, tokenizer=model_path)
