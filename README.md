# AutoBot - Bot Especialista da Oficina Mecânica AutoTech Silva

Atividade acadêmica (6º ciclo - ADS) que consiste em criar um bot especialista
capaz de responder, sem alucinar, sobre um conhecimento fechado (que não está
disponível publicamente na internet).

O projeto é baseado no exemplo **OrderBot** do curso da DeepLearning.AI
([ChatGPT Prompt Engineering for Developers](https://learn.deeplearning.ai/courses/chatgpt-prompt-eng/lesson/jtmdv/chatbot)),
adaptado para:

- um novo domínio: atendimento de uma oficina mecânica fictícia chamada
  **AutoTech Silva** (catálogo de serviços, preços, política de garantia,
  fluxo de agendamento e política de devolução/reclamação);
- um novo provedor de LLM: **Google Gemini** (via biblioteca
  `google-generativeai`), no lugar da API da OpenAI usada no exemplo original.

## O que o bot faz

- Responde exatamente **3 perguntas** do usuário, com base apenas no
  conhecimento inserido no contexto do sistema (personalidade, objetivo/tarefa
  e o "cardápio" de serviços da oficina).
- Se a pergunta não puder ser respondida com essas informações, o bot informa
  isso claramente em vez de inventar uma resposta.
- Ao final da **3ª resposta**, o bot apresenta um **resumo do atendimento**
  (as 3 perguntas feitas e o que foi respondido) e encerra a conversa.

## Estrutura do repositório

```
.
├── oficina_bot.py     # script principal do bot
├── requirements.txt   # dependências do projeto
├── env.example         # modelo do arquivo de variáveis de ambiente
├── .gitignore
└── README.md
```

## Pré-requisitos

- Python 3.9 ou superior instalado
- Uma chave de API gratuita do Google AI Studio: https://aistudio.google.com/app/apikey

## Passo a passo para reproduzir a execução (mesma do vídeo)

1. **Clone o repositório**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd <NOME_DA_PASTA_DO_REPOSITORIO>
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure sua chave de API**
   - Copie o arquivo `env.example` e renomeie a cópia para `.env`
   - Abra o `.env` e preencha:
     ```
     GOOGLE_API_KEY=sua_chave_aqui
     ```

5. **Execute o bot**
   ```bash
   python oficina_bot.py
   ```

6. **Converse com o bot**
   - O AutoBot vai se apresentar e pedir a primeira pergunta.
   - Digite uma pergunta sobre a oficina (ex.: "Quanto custa a troca de óleo?")
     e aperte Enter.
   - Isso se repete por até 3 perguntas. Na 3ª resposta, o bot já apresenta o
     resumo do atendimento e encerra a conversa automaticamente.

## Tecnologias utilizadas

- Python
- [google-generativeai](https://pypi.org/project/google-generativeai/) (SDK do Google Gemini)
- python-dotenv (leitura de variáveis de ambiente a partir do arquivo `.env`)

## Referência

- Exemplo base: [OrderBot - DeepLearning.AI](https://learn.deeplearning.ai/courses/chatgpt-prompt-eng/lesson/jtmdv/chatbot)
