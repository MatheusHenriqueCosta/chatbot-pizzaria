from flask import Flask, render_template, request, jsonify
from chatbot_pizzaria import ChatbotPizzaria
import json

app = Flask(__name__)
chatbot = ChatbotPizzaria()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Mensagem vazia'})
    
    # Processar mensagem
    results = chatbot.process_message(user_message)
    
    # Combinar todas as respostas
    combined_response = ""
    intents_detected = []
    avg_confidence = 0
    
    for result in results:
        combined_response += result['response'] + " "
        intents_detected.append(f"{result['intent']} ({result['confidence']}%)")
        avg_confidence += result['confidence']
    
    if len(results) > 0:
        avg_confidence = avg_confidence / len(results)
    
    return jsonify({
        'response': combined_response.strip(),
        'intents': ', '.join(intents_detected),
        'confidence': round(avg_confidence, 2),
        'details': results
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)