import re
import nltk
from transformers import pipeline

def download_nltk_resources():
   
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

def split_paragraph_into_sentences(paragraph):
   
    paragraph = re.sub(r'\s+', ' ', paragraph.strip())
    sentences = nltk.sent_tokenize(paragraph)
    
    return sentences

def classify_requirements(paragraph, model_path="./models/requirement_classifier"):
   
    download_nltk_resources()
    
    classifier = pipeline("text-classification", model=model_path, tokenizer=model_path)
    
    sentences = split_paragraph_into_sentences(paragraph)
    
    requirements = []
    for sentence in sentences:
        result = classifier(sentence)[0]
        
        if result['label'] == 'requirement' and result['score'] > 0.5:
            requirements.append({
                'sentence': sentence,
                'confidence': result['score']
            })
    
    return requirements