import streamlit as st
from utils.watsonx_functions import call_watsonx_text_model

# Hacer esta página amplia
st.set_page_config(layout="wide")

st.subheader("Interacción directa con un LLM")

columna_inicial_1, columna_inicial_2, columna_inicial_3 = st.columns([0.5,0.25,0.25])
with columna_inicial_1:
    modelo_seleccionado = st.selectbox("Elige el modelo que quieres utilizar", ["IBM Granite 3.3","Mistral Large", "Mistral Small 3.1","Llama 3.3", "Llama 4 Maverick"])

with columna_inicial_2:
    min_tokens_seleccionados = st.number_input("Tokens de respuesta mínimos", min_value=0)

with columna_inicial_3:
    max_tokens_seleccionados = st.number_input("Tokens de respuesta máximos", min_value=0, value=200)

modo_seleccionado = st.radio("Elige un modo de decodificación", ["Greedy", "Sampling"], horizontal=True, help="El modo de decodificación Greedy hace que el modelo tienda a responder casi siempre de la misma manera, por el contrario, el modo Sampling permite que el modelo tenga más variedad en sus respuestas.")

columna_intermedia_1, columna_intermedia_2, columna_intermedia_3 = st.columns(3)

if modo_seleccionado == "Sampling":
    with columna_intermedia_1:
        temperature_seleccionada = st.slider("Temperatura", min_value=0.00, max_value=2.00, value=0.7, step=0.01)
        top_p_seleccionado = st.slider("Top P", min_value=0.01, max_value=1.00, value=1.00, step=0.01)
        top_n_seleccionado = st.slider("Top K", min_value=1, max_value=100, value=50, step=1)
        random_seed_seleccionada = st.number_input("Random seed", min_value=1, value=None)

with columna_intermedia_1:
    repetition_penalty_seleccionada = st.slider("Repetition Penalty", min_value=1.00, max_value=2.00, value=1.00, step=0.01)

prompt_del_usuario = st.text_area("Prompt", placeholder="Escribe aquí tu prompt")

boton_llamar_modelo = st.button("Enviar prompt al modelo")

if boton_llamar_modelo:
    if modo_seleccionado == "Greedy":
        respuesta_generada = call_watsonx_text_model(
            prompt=prompt_del_usuario,
            id_modelo=modelo_seleccionado,
            min_tokens= min_tokens_seleccionados,
            max_tokens = max_tokens_seleccionados,
            modo = modo_seleccionado,
            repetition_penalty=repetition_penalty_seleccionada
        )

    elif modo_seleccionado == "Sampling":
        respuesta_generada = call_watsonx_text_model(
            prompt=prompt_del_usuario,
            id_modelo=modelo_seleccionado,
            min_tokens= min_tokens_seleccionados,
            max_tokens = max_tokens_seleccionados,
            modo = modo_seleccionado,
            repetition_penalty=repetition_penalty_seleccionada,
            temperatura=temperature_seleccionada,
            top_p=top_p_seleccionado,
            top_n=top_n_seleccionado,
            random_seed=random_seed_seleccionada
        )
    
    with st.expander("Respuesta Generada: (En azul se resalta el texto generado por el modelo a partir del prompt del usuario. El prompt del usuario no se resalta).", expanded=True):
        texto_generado = ""
        with st.empty():
            for chunk in respuesta_generada:
                texto_generado += chunk
                lineas_texto_generado = texto_generado.splitlines()
                lineas_no_vacias_texto_generado = [linea for linea in lineas_texto_generado if (len(linea)>0) ]
                lineas_texto_resaltado = [f":blue-background[{texto_linea}]" for texto_linea in lineas_no_vacias_texto_generado]
                st.write(prompt_del_usuario+"\n\n".join(lineas_texto_resaltado))
