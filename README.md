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
## Integração com Deepseek (ingredientes)

Este projeto adiciona uma integração opcional com a Deepseek/OpenRouter para buscar receitas/ingredientes de um prato.

Segue um passo-a-passo claro para o professor cadastrar a chave e testar — comandos em PowerShell (Windows):

1) Pré-requisito

- Ter o projeto extraído e um ambiente virtual criado (veja seção de instalação). O script `setup_deepseek.ps1` também foi incluído para facilitar.

2) Opções para definir a chave (escolha A, B ou C)

- A) Definir a chave apenas para a sessão atual (recomendado para testes):

```powershell
# define a variável só para a sessão atual
$env:DEEPSEEK_API_KEY = 'sua_chave_aqui'

# verificar (mostra a string)
echo $env:DEEPSEEK_API_KEY
```

- B) Definir a chave permanentemente (persistente entre sessões — use apenas se necessário):

```powershell
# grava a variável no perfil do usuário (disponível em novas janelas do terminal)
setx DEEPSEEK_API_KEY "sua_chave_aqui"

# OBS: feche e reabra o PowerShell para a variável entrar em vigor
# verificar só após abrir novo terminal
echo $env:DEEPSEEK_API_KEY
```

- C) Usar o script guiado `setup_deepseek.ps1` (recomendado para ficar mais fácil, professor!)

1. Abra PowerShell na pasta do projeto (onde está `app.py`).
2. Execute:

```powershell
.\setup_deepseek.ps1
```

O script pede a chave de forma segura (entrada oculta), pergunta opcionalmente por `DEEPSEEK_MODEL` e `DEEPSEEK_API_URL`, ativa o `.venv` (se existir) e inicia `app.py` no terminal atual.

3) Testar a configuração

Com o servidor rodando (ex.: `python app.py`), teste o endpoint `/chat` com um POST ou use a interface web.

Exemplo (PowerShell) usando Invoke-RestMethod:

```powershell
$body = @{ message = "Quais são os ingredientes da calabresa?" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:5000/chat -Method POST -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 4
```

Ou abra `http://localhost:5000` no navegador e interaja (por exemplo: "Quais são os ingredientes?" → o bot pedirá o prato → responda "1" ou o nome do prato).

4) Remover/limpar a chave

- Limpar só nesta sessão:

```powershell
Remove-Item Env:\DEEPSEEK_API_KEY
```

- Remover a variável criada por `setx` (GUI):

Abra Painel de Controle → Sistema → Configurações avançadas → Variáveis de Ambiente e edite/remova `DEEPSEEK_API_KEY` da seção de variáveis do usuário. Alternativamente, sobrescreva com vazio:

```powershell
setx DEEPSEEK_API_KEY ""
```

5) Observações de segurança e boas práticas

- Nunca comite sua chave no repositório. Adicione um `.env` ao `.gitignore` se usar arquivos locais para testes.
- Para produção (Heroku/GCP/Azure/GitHub Actions) use os mecanismos de secrets/variables da plataforma.

## Autor
Desenvolvido para o projeto de Chatbot com NLP
Data: 2025

## Licença
Projeto acadêmico - Uso livre para fins educacionais