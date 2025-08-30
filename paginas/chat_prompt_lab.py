import streamlit as st
from utils.watsonx_functions import call_watsonx_chat_mode

# Hacer esta página amplia
st.set_page_config(layout="wide")

# Inicializar el historial de mensajes (Se reinicia cada vez que el usuario recarga la página)
if "messages" not in st.session_state:
    st.session_state.messages = []

#Agregar una función auxiliar para limpiar el chat
def borrar_chat():
    if "messages" in st.session_state:
        st.session_state.messages = []

#Titulo de la página
st.subheader("Chatear con un LLM")

#Definir columnas para la interfaz
col1, col2 = st.columns([0.6,0.4])

with col2:
    modelo_seleccionado = st.selectbox("Elige el modelo que quieres utilizar", ["ibm/granite-3-3-8b-instruct","mistralai/mistral-large", "mistralai/mistral-small-3-1-24b-instruct-2503", "meta-llama/llama-3-3-70b-instruct", "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"])

    max_tokens_seleccionados = st.number_input("Tokens de respuesta máximos", min_value=0, value=200)

    temperature_seleccionada = st.slider("Temperatura", min_value=0.00, max_value=2.00, value=0.00, step=0.01, help="Entre mayor sea la temperatura, las respuestas van a ser más variadas entre sí. Una temperatura muy alta puede hacer que el modelo empiece a generar texto sin sentido")
    
    top_p_seleccionado = st.slider("Top P", min_value=0.01, max_value=1.00, value=1.00, step=0.01, help="Entre mayor sea el valor de Top P, las respuestas van a ser más variadas.")


with col1:
    messages_container = st.container(height=350)
    # Mostrar los mensajes que actualmente estan en el historial
    with messages_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Recibir el input del usuario
    prompt = st.chat_input("Escribe tu prompt aquí")

    # Si el usuario envio un mensaje
    if prompt:
        # Dibujar el mensaje del usuario en la pantalla
        with messages_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        # Agregar el mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})

        #Llamar al modelo 
        respuesta = call_watsonx_chat_mode(
            messages=st.session_state["messages"], 
            id_modelo= modelo_seleccionado, 
            max_tokens_respuesta= max_tokens_seleccionados,
            temperatura=temperature_seleccionada,
            top_p=top_p_seleccionado)
        
        # Display assistant response in chat message container
        with messages_container:
            with st.chat_message("assistant"):
                respuesta_final = st.write_stream(respuesta)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": respuesta_final})

with col2:
    inner_column1, inner_column2 = st.columns(2)
    with inner_column2:
        boton_borrar_chat = st.button("Borrar el chat", on_click=borrar_chat, disabled=(len(st.session_state.messages) <= 0), use_container_width=True)