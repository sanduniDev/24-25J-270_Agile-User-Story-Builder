import pickle  #load train model ,Converts a Python object into a byte stream
import re    #splitting text into sentences, used for working with regular expressions in Python
from preprocessor import preprocess_text

# Load the trained model and vectorizer
model_path = "models/task_nfr_extraction_model.pkl"
vectorizer_path = "models/vectorizer.pkl"

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))


def split_sentences(text):

    sentences = re.split(r'(?<=[.!?])\s+', text)  # Split by sentence-ending punctuation
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def classify_sentences(sentences):   #Classify each sentence into one of the categories: Task, Subtask, or NFR

    X_tfidf = vectorizer.transform(sentences)
    predictions = model.predict(X_tfidf)
    return predictions

#Split into sentences.#Preprocess the sentences to remove noise #Organize sentences into Tasks, Subtasks, and NFRs

def extract_requirements(text, noise_phrases=None):

    sentences = split_sentences(text) #break down in  to sentence

    # Preprocess sentences with noise filtering
    if noise_phrases:
        preprocessed_sentences = [preprocess_text(sentence, noise_phrases) for sentence in sentences]
    else:
        preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]

    # Vectorize sentences
    X_tfidf = vectorizer.transform(preprocessed_sentences)
    predictions = model.predict(X_tfidf)

    tasks = []              #Categorize Sentences
    subtasks = {}
    nfrs = []

    current_task = None

    for sentence, label in zip(preprocessed_sentences, predictions):
        if label == "Task":
            tasks.append(sentence)
            current_task = sentence
            subtasks[current_task] = []  # Initialize a new list for subtasks under this task
        elif label == "Subtask":
            if current_task:
                subtasks[current_task].append(sentence)  # Associate with the current task
            else:
                if "Orphaned" not in subtasks:
                    subtasks["Orphaned"] = []
                subtasks["Orphaned"].append(sentence)  # Add to 'Orphaned' if no task is active
        elif label == "NFR":
            nfrs.append(sentence)

    return tasks, subtasks, nfrs


def associate_subtasks(sentences, predictions):

    tasks = []
    subtasks = {"Orphaned": []}  # Initialize 'Orphaned' key
    current_task = None

    for sentence, label in zip(sentences, predictions):
        if label == "Task":
            tasks.append(sentence)
            current_task = sentence
            subtasks[current_task] = []  # Create a list for this task's subtasks
        elif label == "Subtask":
            if current_task:
                subtasks[current_task].append(sentence)  # Add to the current task
            else:
                subtasks["Orphaned"].append(sentence)  # Add to 'Orphaned' if no task is found

    return tasks, subtasks
