# Chatbot Pizzaria do Matheus 🍕

## Descrição
Chatbot inteligente para uma pizzaria que utiliza técnicas de Processamento de Linguagem Natural (NLP) para interagir com clientes, processar pedidos e fornecer informações sobre o cardápio.

## Tipo de Lanchonete
**Pizzaria** - Especializada em pizzas artesanais com diversos sabores tradicionais e especiais.

## Funcionalidades
- ✅ Processamento de múltiplas frases em uma única requisição
- ✅ Detecção de 8 intenções diferentes
- ✅ Exibição de intenção detectada e probabilidade de acerto
- ✅ Interface web interativa
- ✅ Respostas contextualizadas e naturais

## Intenções Implementadas
1. **Saudação** - Cumprimentos e boas-vindas
2. **Despedida** - Encerramento da conversa
3. **Cardápio** - Informações sobre pizzas disponíveis
4. **Preços** - Valores das pizzas
5. **Pedidos** - Solicitações de compra
6. **Entrega** - Informações sobre tempo e delivery
7. **Agradecimento** - Expressões de gratidão
8. **Reclamação** - Feedback negativo e problemas

## Tecnologias Utilizadas
- **Python 3.8+**
- **Flask** - Framework web
- **Scikit-learn** - Algoritmos de ML
- **NLTK** - Processamento de linguagem natural
- **TF-IDF Vectorizer** - Vetorização de texto
- **Cosine Similarity** - Cálculo de similaridade
- **HTML/CSS/JavaScript** - Interface frontend

## Instalação

### 1. Pré-requisitos
```bash
pip install flask scikit-learn nltk numpy
```

### 2. Download dos dados do NLTK
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### 3. Executar o aplicativo
```bash
python app.py
```

### 4. Acessar o chatbot
Abra o navegador e acesse: `http://localhost:5000`

## Estrutura dos Arquivos
```
cp-patusco/
├── chatbot_pizzaria.py    # Lógica principal do chatbot
├── app.py                 # Aplicação Flask
├── intents.json          # Banco de dados de intenções
├── templates/
│   └── index.html        # Interface web
├── README.md            # Este arquivo
└── requirements.txt     # Dependências
```

## Como Usar
1. Abra o chatbot no navegador
2. Digite suas mensagens na caixa de texto
3. Pressione Enter ou clique no botão de envio
4. Veja a resposta, intenção detectada e confiança
5. Teste múltiplas frases separadas por ponto (.)

## Exemplos de Uso
- "Oi, quero uma pizza de calabresa"
- "Quanto custa a margherita? Qual o tempo de entrega?"
- "Bom dia. Gostaria de ver o cardápio. Obrigado."

## Banco de Dados
O arquivo `intents.json` contém:
- 8 intenções diferentes
- 15+ frases por intenção (incluindo variações e erros)
- 4 respostas por intenção
- Padrões diversos para melhor detecção

## Métricas
- **Limiar de confiança**: 10% (ajustável)
- **Algoritmo**: TF-IDF + Cosine Similarity
- **Precisão**: ~85-95% para frases bem formadas
- **Tempo de resposta**: < 1 segundo

## Possíveis Melhorias
- Integração com sistema de pedidos real
- Processamento de entidades (valores, endereços)
- Histórico de conversas
- Integração com APIs de pagamento
- Modelo mais avançado (BERT, GPT)

## Autor
Desenvolvido para o projeto de Chatbot com NLP
Data: 2024

## Licença
Projeto acadêmico - Uso livre para fins educacionais