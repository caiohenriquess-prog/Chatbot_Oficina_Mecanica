# -----------------------------------------------------------------------------
# BOT ESPECIALISTA - OFICINA MECÂNICA "AUTOTECH SILVA"
# -----------------------------------------------------------------------------
# Adaptado do exemplo "OrderBot" do curso DeepLearning.AI
# (https://learn.deeplearning.ai/courses/chatgpt-prompt-eng/lesson/jtmdv/chatbot)
#
# Objetivo desta atividade:
#   - Criar um bot que responde SEM ALUCINAR sobre um conhecimento fechado,
#     que não está disponível publicamente na internet (o catálogo de
#     serviços e as políticas fictícias da oficina abaixo).
#   - O bot responde exatamente 3 perguntas do usuário.
#   - Ao final da 3ª resposta, ele gera um resumo do que foi respondido
#     e encerra a conversa.
#
# Provedor de LLM: Google (Gemini), via biblioteca google-generativeai
# -----------------------------------------------------------------------------

import os
import google.generativeai as genai
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1) CONFIGURAÇÃO DA API DO GOOGLE (GEMINI)
# -----------------------------------------------------------------------------
# A chave é lida do arquivo .env (veja env.example para o formato esperado).
# Gere uma chave gratuita em https://aistudio.google.com/app/apikey

load_dotenv()  # carrega as variáveis do arquivo .env para o ambiente

API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY não encontrada. Copie o arquivo 'env.example' para "
        "'.env' e preencha o valor da sua chave antes de rodar o script."
    )

genai.configure(api_key=API_KEY)

MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

# -----------------------------------------------------------------------------
# 2) CONTEXTO DO BOT (equivalente ao "system message" do exemplo original)
#    Contém os 3 elementos pedidos na atividade:
#       a) Personalidade do atendente
#       b) Objetivos e tarefa a ser executada
#       c) Conhecimento necessário (catálogo/políticas da oficina)
# -----------------------------------------------------------------------------

CONTEXTO_SISTEMA = """
Você é o AutoBot, o assistente virtual de atendimento da oficina mecânica
"AutoTech Silva".

# PERSONALIDADE
- Você é simpático, objetivo e fala como um atendente de oficina experiente:
  direto ao ponto, sem enrolação, mas educado e prestativo.
- Use uma linguagem simples, evitando jargão técnico excessivo; quando usar
  um termo técnico, explique-o rapidamente.
- Trate o cliente sempre por "você" e feche as respostas de forma cordial.

# OBJETIVO E TAREFA
- Sua única tarefa é tirar dúvidas dos clientes com base EXCLUSIVAMENTE nas
  informações da seção "CONHECIMENTO DA OFICINA" abaixo.
- Você deve responder no máximo 3 perguntas do cliente nesta conversa.
- NUNCA invente preços, prazos, serviços, peças ou políticas que não estejam
  listados no CONHECIMENTO DA OFICINA. Se a pergunta não puder ser respondida
  com essas informações, diga claramente que não possui essa informação e
  sugira que o cliente entre em contato pelo telefone (11) 4002-8900 ou
  WhatsApp (11) 90000-1234 para mais detalhes. Não tente adivinhar.
- Não responda perguntas fora do escopo de oficina mecânica/AutoTech Silva
  (ex.: assuntos gerais, outras empresas, etc.); apenas informe educadamente
  que seu escopo é limitado ao atendimento da AutoTech Silva.
- Depois que o cliente fizer a 3ª pergunta e você a responder, você deve,
  na mesma resposta, apresentar um "Resumo do atendimento" listando de forma
  breve as 3 perguntas feitas e o que foi respondido, e então encerrar a
  conversa de forma cordial, informando que o atendimento foi finalizado.

# CONHECIMENTO DA OFICINA (AutoTech Silva)

## Dados gerais
- Endereço: Av. das Oficinas, 500 - Praia Grande/SP
- Horário de funcionamento: Segunda a sexta, 8h às 18h; sábados, 8h às 12h.
- Telefone: (11) 4002-8900 | WhatsApp: (11) 90000-1234
- Formas de pagamento: dinheiro, PIX, débito, crédito (em até 6x sem juros
  acima de R$ 300).

## Catálogo de serviços e preços (a partir de)
| Serviço                                   | Preço a partir de | Prazo médio        |
|--------------------------------------------|--------------------|---------------------|
| Troca de óleo e filtro                     | R$ 180,00          | 40 minutos          |
| Alinhamento e balanceamento (4 rodas)      | R$ 150,00          | 1 hora              |
| Revisão completa (itens de segurança)      | R$ 350,00          | 3 horas             |
| Troca de pastilhas de freio (por eixo)     | R$ 220,00          | 1h30                |
| Diagnóstico eletrônico (scanner)           | R$ 120,00          | 30 minutos          |
| Troca de correia dentada + tensores        | R$ 480,00          | 4 horas             |
| Manutenção de ar-condicionado              | R$ 250,00          | 2 horas             |
| Suspensão (troca de amortecedores, o par)  | R$ 600,00          | 3 horas             |

## Política de garantia
- Todo serviço realizado tem garantia de 90 dias OU 3.000 km rodados
  (o que ocorrer primeiro), cobrindo apenas o serviço executado, não peças
  desgastadas por uso normal após o prazo.
- Peças trocadas têm garantia conforme o fabricante (informada na nota
  fiscal do serviço).

## Como agendar um serviço
1. Cliente entra em contato via telefone ou WhatsApp informando modelo/ano
   do veículo e o serviço desejado.
2. Atendente verifica disponibilidade de horário e peça (se necessário) e
   confirma um horário de entrada do veículo.
3. Cliente leva o veículo no horário agendado; um checklist de entrada é
   preenchido e assinado por ambas as partes.
4. Após execução, o cliente é avisado por telefone/WhatsApp para retirada
   e pagamento.
5. Na retirada, é entregue a nota fiscal do serviço, que também serve como
   comprovante de garantia.

## Política de devolução/reclamação de serviço
- Caso o cliente identifique um problema relacionado ao serviço executado
  dentro do prazo de garantia, deve entrar em contato pelo telefone ou
  WhatsApp e agendar uma reavaliação gratuita.
- Se o problema for confirmado como falha do serviço prestado, o reparo é
  refeito sem custo. Se for um problema novo, não relacionado ao serviço
  original, será orçado separadamente.
- Não há devolução de valores para serviços já executados corretamente;
  apenas correção do serviço, quando aplicável à garantia.

## Retirada de peças substituídas
- O cliente pode solicitar a devolução das peças antigas substituídas no
  momento da retirada do veículo, exceto peças enviadas para garantia do
  fabricante (ex.: motor de arranque, alternador).
"""

# -----------------------------------------------------------------------------
# 3) LÓGICA DA CONVERSA
#    - Usa o histórico de chat do Gemini (start_chat) para manter contexto.
#    - Limita a exatamente 3 perguntas do usuário.
#    - Ao final da 3ª resposta, pede um resumo e encerra.
# -----------------------------------------------------------------------------

def criar_chat():
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=CONTEXTO_SISTEMA,
    )
    return model.start_chat(history=[])


def rodar_bot():
    chat = criar_chat()
    print("AutoBot: Olá! Sou o assistente virtual da AutoTech Silva. "
          "Você pode me fazer até 3 perguntas sobre nossos serviços. "
          "Como posso ajudar?\n")

    MAX_PERGUNTAS = 3
    for numero_pergunta in range(1, MAX_PERGUNTAS + 1):
        pergunta = input(f"Você (pergunta {numero_pergunta}/{MAX_PERGUNTAS}): ")

        if numero_pergunta < MAX_PERGUNTAS:
            prompt_envio = pergunta
        else:
            # Na última pergunta, já pedimos o resumo + encerramento
            # na mesma resposta, conforme instruído no CONTEXTO_SISTEMA.
            prompt_envio = (
                f"{pergunta}\n\n"
                "(Esta foi a última pergunta permitida nesta conversa. "
                "Responda normalmente e, em seguida, apresente o "
                "'Resumo do atendimento' e encerre a conversa, conforme "
                "as instruções do seu contexto.)"
            )

        resposta = chat.send_message(prompt_envio)
        print(f"\nAutoBot: {resposta.text}\n")

    print("--- Atendimento encerrado. Obrigado por falar com a AutoTech Silva! ---")


if __name__ == "__main__":
    rodar_bot()
