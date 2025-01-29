import re
import pandas as pd
from unidecode import unidecode


# Load noise dataset
def load_noise_dataset(noise_path="data/noise_dataset.csv"):

    try:
        noise_df = pd.read_csv(noise_path) # Uses pandas.read_csv to load the CSV file into a DataFrame (noise_df)
        noise_phrases = noise_df["Noise"].str.lower().tolist()  # Convert to lowercase for consistent comparison
        return noise_phrases
    except Exception as e:
        print(f"Error loading noise dataset: {e}")
        return []


# Preprocess text with noise filtering
def preprocess_text(text, noise_phrases=None):

    text = unidecode(text)  # Normalize special characters
    text = text.lower().strip()
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove unwanted characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space

    # Remove noise phrases if provided
    if noise_phrases:
        for phrase in noise_phrases:
            text = text.replace(phrase, "")

    return text.strip()
