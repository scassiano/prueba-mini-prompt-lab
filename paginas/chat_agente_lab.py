import streamlit as st

from utils.langchain_functions import call_agent_with_tools
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.tool import ToolMessage

# Hacer esta página amplia
st.set_page_config(layout="wide")

# Inicializar el historial de mensajes de langchain (Se reinicia cada vez que el usuario recarga la página)
if "agent_langchain_messages" not in st.session_state:
    st.session_state.agent_langchain_messages = []

# Inicializar el historial de mensajes del chat, para que sean mostrados en la interfaz
if "agent_chat_messages" not in st.session_state:
    st.session_state.agent_chat_messages = []

#Agregar una función auxiliar para limpiar el chat y los mensajes
def borrar_chat_agente():
    if "agent_langchain_messages" in st.session_state:
        st.session_state.agent_langchain_messages = []
    
    if "agent_chat_messages" in st.session_state:
        st.session_state.agent_chat_messages = []
    

#Titulo de la página
st.subheader("Chatear con un agente")

#Definir columnas para la interfaz
col1, col2 = st.columns([0.6,0.4])

with col2:
    #Elegir las tools a las que se quiere que tenga acceso el agente
    seleccionar_tool_fecha = st.toggle("Activar Herramienta Fecha Actual")
    seleccionar_tool_clima = st.toggle("Activar Herramienta Clima Actual")
    seleccionar_tool_youtube = st.toggle("Activar Busqueda en Youtube")
    seleccionar_tool_suma = st.toggle("Activar Herramienta Suma de dos Numeros")
    seleccionar_tool_web= st.toggle("Activar Busqueda Web")
    seleccionar_tool_arxiv= st.toggle("Activar Busqueda en ArXiv")
    seleccionar_tool_contenido_web = st.toggle("Activar Busqueda por URL")
    seleccionar_tool_wikipedia = st.toggle("Activar Busqueda en Wikipedia")

with col1:
    messages_container = st.container(height=350)
    # Mostrar los mensajes que actualmente estan en el historial
    with messages_container:
        for message in st.session_state.agent_chat_messages:
            if message[0] == "tool":
                with st.chat_message(message[0], avatar=":material/build:"):
                    with st.expander("Haz click aqui para ver la informacion obtenida."):
                        st.write(message[1])
            else:
                with st.chat_message(message[0]):
                    st.write(message[1])

    # Recibir el input del usuario
    prompt = st.chat_input("Escribe tu prompt aquí")

    # Si el usuario envio un mensaje
    if prompt:
        # Dibujar el mensaje del usuario en la pantalla
        with messages_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        #Agregar el Human message al historial para langchain
        st.session_state.agent_langchain_messages.append(HumanMessage(content=prompt))

        # Agregar el mensaje del usuario al historial
        st.session_state.agent_chat_messages.append(("human",prompt))

        #Llamar al modelo 
        respuesta = call_agent_with_tools(
            messages = st.session_state.agent_langchain_messages,
            amount_of_current_messages= len(st.session_state.agent_langchain_messages),
            tool_fecha = seleccionar_tool_fecha,
            tool_clima = seleccionar_tool_clima,
            tool_youtube = seleccionar_tool_youtube,
            tool_suma = seleccionar_tool_suma,
            tool_web=seleccionar_tool_web,
            tool_arxiv=seleccionar_tool_arxiv,
            tool_revision_url=seleccionar_tool_contenido_web,
            tool_wikipedia = seleccionar_tool_wikipedia
        )

        for result in respuesta:
            with messages_container:
                if result["chat_message"][0] == "tool":
                    with st.chat_message(result["chat_message"][0], avatar=":material/build:"):
                        with st.expander("Haz click aqui para ver la informacion obtenida."):
                            st.write(result["chat_message"][1])
                else:
                    with st.chat_message(result["chat_message"][0]):
                        st.write(result["chat_message"][1])
                        
            st.session_state.agent_langchain_messages.append(result["langchain_message"])
            st.session_state.agent_chat_messages.append(result["chat_message"])

with col2:
    inner_column1, inner_column2, inner_column3 = st.columns([0.25,0.5,0.25])
    with inner_column2:
        boton_borrar_chat_agentes = st.button("Borrar el chat", on_click=borrar_chat_agente, disabled=(len(st.session_state.agent_chat_messages) <= 0), use_container_width=True)