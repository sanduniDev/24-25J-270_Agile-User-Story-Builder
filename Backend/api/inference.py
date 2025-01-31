import re
import nltk
from transformers import pipeline

# Classify sentences as requirements or not.
# Generate user stories from sentences,
# particularly by removing subjects and formatting the sentence 
# in a user-story format.
class RequirementClassifier:
    def __init__(self, model_path="./models/requirement_classifier", story_model="google/flan-t5-large"):
        self.model_path = model_path
        self.story_model = story_model
        self.classifier = None
        self._download_nltk_resources()
        self._load_pipelines()

    @staticmethod
    def _download_nltk_resources():
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger_eng')
        except LookupError:
            nltk.download('averaged_perceptron_tagger_eng')

    def _load_pipelines(self):
        try:
            self.classifier = pipeline("text-classification", model=self.model_path, tokenizer=self.model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load pipelines: {e}")

    @staticmethod
    def split_paragraph_into_sentences(paragraph):
        paragraph = re.sub(r'\s+', ' ', paragraph.strip())
        sentences = nltk.sent_tokenize(paragraph)
        return sentences

    @staticmethod
    def remove_subject(sentence):
        doc = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(doc)

        subject_pos_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']

        subject_removed = False
        for i, (word, pos) in enumerate(tagged):
            if pos in subject_pos_tags:
                sentence = sentence.replace(word, "", 1)
                subject_removed = True
                break

        if subject_removed:
            sentence = sentence.strip()

        return sentence
    def generate_user_story(self, text):
       sentence=self.remove_subject(text)
       complete_sentence=f"As a User, I {sentence} , So that I can improve functionality or experience of the system. "
       return complete_sentence

    def classify_requirements(self, sentence):
        result = self.classifier(sentence)[0]
        if result['label'] == 'LABEL_1' and result['score'] > 0.5:
            return {
                'Label': 'Requirement' if result['label'] == 'LABEL_1' else 'Non Requirement',
                'sentence': sentence,
                'story': self.generate_user_story(sentence),
                'confidence': result['score']
            }