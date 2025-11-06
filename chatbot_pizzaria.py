import json
import random
import string
import os
import requests
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import pickle
import re
import unicodedata

# Download necessário do NLTK (execute apenas uma vez)
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class ChatbotPizzaria:
    def __init__(self):
        self.intents = self.load_intents()
        # tentar carregar stopwords em português do NLTK; se falhar, sem stopwords
        try:
            from nltk.corpus import stopwords
            pt_stopwords = stopwords.words('portuguese')
        except Exception:
            pt_stopwords = None

        self.vectorizer = TfidfVectorizer(stop_words=pt_stopwords, lowercase=True)
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
        # remover acentuação
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('ASCII')
        # remover pontuação
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def get_dish_from_text(self, text):
        """Tenta extrair o nome do prato a partir do texto checando a intent 'escolha_sabor'."""
        text_proc = self.preprocess_text(text)

        # coletar pratos (raw e processados) a partir do intent 'escolha_sabor'
        dishes_raw = []
        dishes_proc = []
        for intent in self.intents.get('intents', []):
            if intent.get('tag') == 'escolha_sabor':
                for p in intent.get('patterns', []):
                    dishes_raw.append(p)
                    dishes_proc.append(self.preprocess_text(p))
                break

        # 1) Se o usuário enviar apenas um número, interpretar como índice (1-based)
        if text_proc.strip().isdigit():
            idx = int(text_proc.strip()) - 1
            if 0 <= idx < len(dishes_proc):
                return dishes_raw[idx]

        # 2) Procurar correspondência direta (exata ou contida)
        for raw, proc in zip(dishes_raw, dishes_proc):
            if proc in text_proc.split() or proc in text_proc:
                return raw

        return None

    def _contains_ingredient_keyword(self, text):
        """Checa se o texto contém palavras-chave relacionadas a 'ingredientes'."""
        kws = ['ingredientes', 'ingrediente', 'receita', 'o que tem', 'o que leva', 'quais os ingredientes', 'buscar ingredientes']
        t = self.preprocess_text(text)
        for kw in kws:
            if self.preprocess_text(kw) in t:
                return True
        return False

    def query_deepseek(self, dish_name):
        """
        Consulta a Deepseek (endpoint configurável via env vars).
        Requer as variáveis de ambiente: DEEPSEEK_API_KEY e opcionalmente DEEPSEEK_API_URL.
        Retorna texto com a resposta (ou mensagem de erro amigável).
        """
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        api_url = os.environ.get('DEEPSEEK_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
        model = os.environ.get('DEEPSEEK_MODEL', 'deepseek/deepseek-r1:free')

        if not api_key:
            return "Para buscar a receita preciso da sua chave da Deepseek (variável DEEPSEEK_API_KEY não encontrada)."

        prompt = f"Qual a receita do prato {dish_name}?"
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        payload = {
            'model': model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ]
        }

        # tentativa com retry simples
        last_exc = None
        for attempt in range(2):
            try:
                resp = requests.post(api_url, headers=headers, json=payload, timeout=20)
                resp.raise_for_status()
                data = resp.json()

                # Exemplo de parsing compatível com OpenRouter-style responses
                if isinstance(data, dict):
                    choices = data.get('choices') or []
                    if choices and isinstance(choices, list) and len(choices) > 0:
                        first = choices[0]
                        if isinstance(first, dict):
                            content = first.get('message', {}).get('content') or first.get('text')
                            if content:
                                return content

                    # tentar chaves alternativas
                    for key in ('answer', 'result', 'results', 'data', 'text'):
                        if key in data and data[key]:
                            val = data[key]
                            if isinstance(val, list):
                                return '\n'.join([str(x) for x in val])
                            if isinstance(val, dict):
                                for sub in ('text', 'answer'):
                                    if sub in val:
                                        return val[sub]
                                return json.dumps(val, ensure_ascii=False)
                            return str(val)

                return resp.text[:4000]
            except requests.RequestException as e:
                last_exc = e
                # backoff curto
                time.sleep(1)
                continue

        return f"Erro ao contatar Deepseek após tentativas: {str(last_exc)}"
    
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

        # fallback por palavra-chave (especialmente para 'ingredientes')
        if self._contains_ingredient_keyword(user_input):
            return 'ingredientes', 0.25

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
            if not sentence.strip():
                continue

            # 1) Se a frase contém o nome de um prato, tratar como pedido de ingredientes
            dish = self.get_dish_from_text(sentence)
            if dish:
                # Consulta Deepseek para ingredientes
                deepseek_resp = self.query_deepseek(dish)
                results.append({
                    'sentence': sentence,
                    'intent': 'ingredientes',
                    'confidence': round(100.0, 2),
                    'response': deepseek_resp
                })
                continue

            # 2) Caso contrário, identificar intenção normalmente
            intent, confidence = self.get_intent(sentence)

            # Se a intenção é 'ingredientes' mas não há prato no texto, pedir seleção ao usuário
            if intent == 'ingredientes':
                # montar lista de pratos disponíveis
                dishes = []
                for it in self.intents.get('intents', []):
                    if it.get('tag') == 'escolha_sabor':
                        dishes = [p for p in it.get('patterns', [])]
                        break

                prompt = "Claro — qual prato você quer? Escolha um dos seguintes: " + ", ".join(dishes)

                results.append({
                    'sentence': sentence,
                    'intent': intent,
                    'confidence': round(confidence * 100, 2),
                    'response': prompt,
                    'expecting_dish': True
                })
                continue

            # comportamento padrão
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