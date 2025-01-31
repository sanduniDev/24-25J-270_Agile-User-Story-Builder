import pandas as pd
from transformers import BertTokenizer
from models.requirement_classifier import load_model
from utils.preprocess import preprocess_data
from models.trainer import train_model, evaluate_model

train_df = pd.read_csv('data/train.csv')
test_df = pd.read_csv('data/test.csv')
validate_df = pd.read_csv('data/validate.csv')

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

train_dataset = preprocess_data(train_df, tokenizer)
test_dataset = preprocess_data(test_df, tokenizer)
validate_dataset = preprocess_data(validate_df, tokenizer)

model = load_model()

trainer = train_model(model, train_dataset, validate_dataset, tokenizer)

evaluate_model(trainer, test_dataset)

model.save_pretrained("./models/requirement_classifier")
tokenizer.save_pretrained("./models/requirement_classifier")
