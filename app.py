from openai import OpenAI
import streamlit as st

st.title("Hakura Orientações Pré-Hospistalares")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize the OpenAI model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize the message history
if "messages" not in st.session_state:
    # Add the initial system message
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
                Você é uma inteligência artificial projetada para ajudar pacientes com osteogênese imperfeita (OI), oferecendo suporte em dúvidas sobre a condição e orientações em casos de acidentes.

                ### Instruções gerais:
                1. Inicie a conversa se apresentando de maneira amigável como uma inteligência artificial da empresa Hakura e procure saber se ele possui dúvidas sobre osteogênese imperfeita ou se sofreu algum acidente; 
                2. Caso o paciente faça perguntas sobre osteogênese imperfeita, responda com informações claras, baseadas em evidências científicas, e adaptadas à linguagem leiga. 
                3. Não dar diagnósticos nem condutas ou recomendações de remédios , no caso de sintomas e dores deve recomendar que o paciente vá ao médico!
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
                - Sempre ofereça recomendações baseadas na gravidade do caso e priorize a busca por atendimento médico adequado.
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

# Display chat messages (excluding system messages)
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip the system message
        with st.chat_message(name=message["role"]):
            st.write(message["content"])

# User input
prompt = st.chat_input("Digite sua mensagem...")
if prompt:
    # Display user message in the chat container
    with st.chat_message(name="user"):
        st.write(prompt)

    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
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

    # Add assistant's response to the history
    st.session_state.messages.append({"role": "assistant", "content": response})
