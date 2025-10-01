import json
import random
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import pickle
import re

# Download necessário do NLTK (execute apenas uma vez)
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class ChatbotPizzaria:
    def __init__(self):
        self.intents = self.load_intents()
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        self.train_model()
    
    def load_intents(self):
        """Carrega as intenções do arquivo JSON"""
        try:
            with open('intents.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Arquivo intents.json não encontrado!")
            return {"intents": []}
    
    def preprocess_text(self, text):
        """Pré-processa o texto removendo pontuações e normalizando"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def train_model(self):
        """Treina o modelo TF-IDF com as frases das intenções"""
        self.training_sentences = []
        self.intent_labels = []
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                self.training_sentences.append(self.preprocess_text(pattern))
                self.intent_labels.append(intent['tag'])
        
        if self.training_sentences:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.training_sentences)
    
    def get_intent(self, user_input):
        """Identifica a intenção da mensagem do usuário"""
        user_input_processed = self.preprocess_text(user_input)
        user_vector = self.vectorizer.transform([user_input_processed])
        
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        best_match_idx = np.argmax(similarities)
        confidence = similarities[best_match_idx]
        
        if confidence > 0.1:  # Limiar de confiança
            intent_tag = self.intent_labels[best_match_idx]
            return intent_tag, confidence
        else:
            return "unknown", 0.0
    
    def get_response(self, intent_tag):
        """Retorna uma resposta aleatória para a intenção identificada"""
        for intent in self.intents['intents']:
            if intent['tag'] == intent_tag:
                return random.choice(intent['responses'])
        return "Desculpe, não entendi sua mensagem. Pode reformular?"
    
    def process_message(self, user_input):
        """Processa a mensagem do usuário e retorna resposta com detalhes"""
        # Dividir a mensagem em frases (para múltiplas frases)
        sentences = [s.strip() for s in user_input.split('.') if s.strip()]
        if not sentences:
            sentences = [user_input]
        
        results = []
        
        for sentence in sentences:
            if sentence.strip():
                intent, confidence = self.get_intent(sentence)
                response = self.get_response(intent)
                
                results.append({
                    'sentence': sentence,
                    'intent': intent,
                    'confidence': round(confidence * 100, 2),
                    'response': response
                })
        
        return results

# Instanciar o chatbot
chatbot = ChatbotPizzaria()

def chat():
    """Interface de linha de comando para o chatbot"""
    print("🍕 Bem-vindo à Pizzaria do Patusco! 🍕")
    print("Digite 'sair' para encerrar a conversa.")
    print("-" * 50)
    
    while True:
        user_input = input("\nVocê: ")
        
        if user_input.lower() in ['sair', 'quit', 'exit']:
            print("Chatbot: Obrigado por visitar a Pizzaria do Patusco! Até logo! 🍕")
            break
        
        results = chatbot.process_message(user_input)
        
        for result in results:
            print(f"\nFrase: '{result['sentence']}'")
            print(f"Intenção: {result['intent']}")
            print(f"Confiança: {result['confidence']}%")
            print(f"Resposta: {result['response']}")
            print("-" * 30)

if __name__ == "__main__":
    chat()