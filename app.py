from openai import OpenAI
import streamlit as st
from guardrails.hub import RestrictToTopic
from guardrails import Guard

# Constants and Configuration
COMPANY_LOGO_URL = "logo.jpg"
VALID_TOPICS = [
    "greeting", "health", "diseases", "accident", "patient", "doctor", "osteogenesis imperfecta"
]

# Guard configuration
guard = Guard().use(
    RestrictToTopic(
        valid_topics=VALID_TOPICS,
        disable_classifier=True,
        disable_llm=False,
        on_fail="exception"  # Raises an exception if input is off-topic
    )
)

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def setup_page():
    """Set up the page configuration, title, favicon, and CSS styles."""
    st.set_page_config(
        page_title="Hakura Orientações Pré-Hospistalares",
        page_icon=COMPANY_LOGO_URL,
        layout="centered"
    )
    # Inject custom CSS and fonts
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        .stAppHeader, .st-emotion-cache-hzygls {
            background-color: #5271ff;
        }
        body, .stTextInput, .stTextArea, .stMarkdown, .stCodeBlock, .stChatMessage, .css-1d391kg p {
            color: #000000;
            font-family: 'Poppins', sans-serif;
        }
        body, input, textarea {
            font-size: 1.1rem;
            line-height: 1.5;
        }
        h1 {
            font-size: 1.75rem;
            font-weight: 600;
        }
        .st-emotion-cache-janbn0, .stAlertContainer {
            background-color: #FFFFFF;
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title
    st.markdown(
        "<h1 style='color: black; text-align: center;'>Hakura Orientações Pré-Hospitalares</h1>",
        unsafe_allow_html=True
    )


def initialize_messages():
    """Initialize message history with system prompt and initial assistant response."""
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state:
        # Add the initial system message
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
                    Você é uma inteligência artificial projetada para ajudar pacientes com osteogênese imperfeita (OI),
                    oferecendo suporte em dúvidas sobre a condição e orientações em casos de acidentes.

                    ### Instruções gerais:
                    1. Inicie a conversa se apresentando de maneira amigável como uma inteligência artificial da empresa 
                       Hakura e procure saber se ele possui dúvidas sobre osteogênese imperfeita ou se sofreu algum acidente; 
                    2. Caso o paciente faça perguntas sobre osteogênese imperfeita, responda com informações claras, 
                       baseadas em evidências científicas, e adaptadas à linguagem leiga. 
                    3. Não dar diagnósticos nem condutas ou recomendações de remédios , no caso de sintomas e dores 
                       deve recomendar que o paciente vá ao médico!
                    4. Se o paciente relatar ter sofrido um acidente: 
                       - Pergunte como foi o acidente.
                       - Classifique o acidente com base na área afetada, escolhendo entre as seguintes opções:
                         - *braço*
                         - *antebraço*
                         - *cabeça*
                         - *joelho*
                         - *perna*
                         - *coxa*
                         - *tórax*
                       - Salve a área identificada no parâmetro <local_acidente>.

                    ### Recomendações baseadas no <local_acidente>:
                    1. *Braço*:
                       - Assista ao vídeo de orientação: [Imobilização do Braço](https://www.youtube.com/watch?v=yiB04G30Eww).
                       - Realize a imobilização conforme descrito no vídeo.
                       - Procure um pronto-socorro para radiografias.

                    2. *Antebraço*:
                       - Assista ao vídeo de orientação: [Imobilização do Antebraço](https://www.youtube.com/watch?v=dFmDD0B4kz0).
                       - Realize a imobilização conforme descrito no vídeo.
                       - Procure um pronto-socorro para radiografias.

                    3. *Cabeça*:
                       - Procure um pronto-socorro urgentemente para avaliação de possível trauma cranioencefálico.

                    4. *Joelho*:
                       - Assista ao vídeo de orientação: [Imobilização do Joelho](https://www.youtube.com/watch?v=6xs2SdilvME).
                       - Realize a imobilização conforme descrito no vídeo.
                       - Procure um pronto-socorro para radiografias.

                    5. *Perna*:
                       - Assista ao vídeo de orientação: [Imobilização da Perna](https://www.youtube.com/watch?v=zSCxE3-Q0FI).
                       - Realize a imobilização conforme descrito no vídeo.
                       - Procure um pronto-socorro para radiografias.

                    6. *Coxa*:
                       - Assista ao vídeo de orientação: [Imobilização da Coxa](https://www.youtube.com/watch?v=gRMBk_h-x9M).
                       - Realize a imobilização conforme descrito no vídeo.
                       - Procure um pronto-socorro para radiografias.

                    7. *Tórax*:
                       - Procure um pronto-socorro urgentemente para avaliação de possível trauma toráxico. 

                    ### Observações:
                    - Sempre ofereça recomendações baseadas na gravidade do caso e priorize a busca por atendimento médico 
                      adequado.
                    - Adapte as respostas para garantir que sejam compreensíveis para pessoas leigas.
                """
            }
        ]

        # Generate the initial assistant message
        try:
            initial_response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages
            )
            initial_content = initial_response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": initial_content})
        except Exception as e:
            initial_content = f"Erro ao gerar mensagem inicial: {e}"
            st.session_state.messages.append({"role": "assistant", "content": initial_content})


def display_messages():
    """Display all chat messages (excluding system messages) with appropriate avatars."""
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            avatar = COMPANY_LOGO_URL if msg["role"] == "assistant" else None
            with st.chat_message(name=msg["role"], avatar=avatar):
                st.write(msg["content"])


def handle_user_input():
    """Handle user's input, validate it, and generate assistant response."""
    prompt = st.chat_input("Digite sua mensagem...")
    if prompt:
        # Validate user input with Guard
        try:
            guard.validate(prompt)  # Raise exception if validation fails

            # Display user message
            with st.chat_message(name="user"):
                st.write(prompt)

            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Generate assistant response
            with st.chat_message("assistant", avatar=COMPANY_LOGO_URL):
                try:
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                except Exception as e:
                    response = f"Error: {e}"
                    st.write(response)

            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            print("New messages appended!")

        except Exception:
            # If validation fails, show error
            st.error("Por favor, insira uma mensagem relacionada a tópicos de saúde ou acidentes.")


# Run setup functions
setup_page()
initialize_messages()
display_messages()
handle_user_input()
