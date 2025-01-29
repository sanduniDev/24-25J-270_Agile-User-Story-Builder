import os
import pandas as pd
from sklearn.model_selection import train_test_split   #Splits data into training and test sets for model training and evaluation
from sklearn.feature_extraction.text import TfidfVectorizer   # convert data in to numerical data
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, accuracy_score
import pickle    # to save python files and models
import csv         #Provides functions to read and write CSV
import matplotlib.pyplot as plt
from sklearn.utils.multiclass import unique_labels #Retrieves unique labels from the target data for classification tasks.


# Step 1: Clean and validate dataset
def clean_and_validate_csv(input_path): # Reads the CSV file and ensures that the rows have valid data.
    cleaned_data = []
    with open(input_path, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Skip the header

        for row in reader:
            if len(row) > 3:
                sentence = ",".join(row[:-2]).strip()
                label = row[-2].strip()
                parent_task = row[-1].strip()
                cleaned_data.append([sentence, label, parent_task])
            elif len(row) == 3:
                cleaned_data.append(row)
            elif len(row) == 2:
                cleaned_data.append([row[0], row[1], ""])
            else:
                print(f"Skipping malformed row: {row}")

    return pd.DataFrame(cleaned_data, columns=["Sentence", "Label", "Parent_Task"])


# Step 2: Validate and load data
def load_training_data(data_path):
    try:
        df = clean_and_validate_csv(data_path)
        df = df.dropna(subset=["Sentence", "Label"])
        df = df[df["Sentence"].str.strip() != ""]
        return df
    except Exception as e:
        print(f"Error loading training data: {e}")
        exit()


# Step 3: Preprocess text
def preprocess_data(df):
    X = df['Sentence']
    y = df['Label']

    vectorizer = TfidfVectorizer(stop_words='english')
    X_tfidf = vectorizer.fit_transform(X)

    return X_tfidf, y, vectorizer


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)  # Ensures reproducibility using 42
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=0))

    # Visualize Accuracy
    plt.figure(figsize=(6, 4))
    plt.bar(["Accuracy"], [acc], color='skyblue')
    plt.title("Model Accuracy")
    plt.ylim(0, 1)
    plt.ylabel("Accuracy")
    plt.show()

    # Visualize Confusion Matrix
    all_labels = sorted(unique_labels(y_test, y_pred))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=all_labels, cmap='Blues'
    )
    plt.title("Confusion Matrix")
    plt.show()

    return model


# Step 5: Save the model and vectorizer
def save_model(model, vectorizer, output_dir="models/"):
    os.makedirs(output_dir, exist_ok=True)
    pickle.dump(model, open(os.path.join(output_dir, "task_nfr_extraction_model.pkl"), "wb"))
    pickle.dump(vectorizer, open(os.path.join(output_dir, "vectorizer.pkl"), "wb"))
    print(f"Model and vectorizer saved to {output_dir}")


if __name__ == "__main__":
    input_path = "data/formatted_training_data.csv"

    if not os.path.exists(input_path):
        print(f"Training data not found at {input_path}. Please provide the dataset.")
        exit()

    # Load and validate training data
    df = load_training_data(input_path)
    X, y, vectorizer = preprocess_data(df)

    # Train the model and visualize results
    model = train_model(X, y)

    # Save the model and vectorizer
    save_model(model, vectorizer)