import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

class T5UserStoryGenerator:
    def __init__(self, model_name='t5-base'):
       
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    def generate_user_story(self, text, max_length=100):
      
        input_text = f"convert to user story: {text}"
        
        inputs = self.tokenizer.encode(
            input_text, 
            return_tensors='pt', 
            max_length=512, 
            truncation=True
        ).to(self.device)
        
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7, 
            do_sample=True
        )
        
        user_story = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return user_story
    
    def fine_tune_model(self, training_texts, user_stories):
       
        train_encodings = self.tokenizer(
            [f"convert to user story: {text}" for text in training_texts],
            truncation=True,
            padding=True,
            max_length=512
        )
        
        train_labels = self.tokenizer(
            user_stories,
            truncation=True,
            padding=True,
            max_length=512
        )
        
        class UserStoryDataset(torch.utils.data.Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels
            
            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item['labels'] = torch.tensor(self.labels['input_ids'][idx])
                return item
            
            def __len__(self):
                return len(self.encodings['input_ids'])
        
        print("Fine-tuning requires additional training infrastructure")
    
    def generate_user_stories(self, texts):
       
        return [self.generate_user_story(text) for text in texts]