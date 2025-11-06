from flask import Flask, render_template, request, jsonify, session
from chatbot_pizzaria import ChatbotPizzaria
import os

app = Flask(__name__)
# secret key para sessions; para produção defina FLASK_SECRET_KEY
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(24)
chatbot = ChatbotPizzaria()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Mensagem vazia'})

    # se o usuário estava no fluxo 'ingredientes' esperando o prato, tratar aqui
    if session.get('expecting_dish'):
        # tentar extrair prato da mensagem
        dish = chatbot.get_dish_from_text(user_message)
        if not dish:
            # reenviar lista de pratos
            dishes = []
            for it in chatbot.intents.get('intents', []):
                if it.get('tag') == 'escolha_sabor':
                    dishes = list(it.get('patterns', []))
                    break

            return jsonify({
                'response': "Desculpe, não identifiquei o prato. Escolha um dos seguintes: " + ", ".join(dishes),
                'intents': 'ingredientes (0%)',
                'confidence': 0.0,
                'details': [{'sentence': user_message, 'intent': 'ingredientes', 'confidence': 0.0, 'response': 'awaiting dish', 'expecting_dish': True}]
            })

        # achou o prato -> consultar Deepseek
        deepseek_resp = chatbot.query_deepseek(dish)
        # limpar estado
        session.pop('expecting_dish', None)

        return jsonify({
            'response': deepseek_resp,
            'intents': 'ingredientes (100%)',
            'confidence': 100.0,
            'details': [{'sentence': user_message, 'intent': 'ingredientes', 'confidence': 100.0, 'response': deepseek_resp}]
        })
    
    results = chatbot.process_message(user_message)
    
    combined_response = ""
    intents_detected = []
    avg_confidence = 0
    
    for result in results:
        combined_response += result['response'] + " "
        intents_detected.append(f"{result['intent']} ({result['confidence']}%)")
        avg_confidence += result['confidence']
        # se o chatbot está pedindo que o usuário escolha o prato, marcar sessão
        if result.get('expecting_dish'):
            session['expecting_dish'] = True
    
    if len(results) > 0:
        avg_confidence = avg_confidence / len(results)
    
    return jsonify({
        'response': combined_response.strip(),
        'intents': ', '.join(intents_detected),
        'confidence': round(avg_confidence, 2),
        'details': results
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)