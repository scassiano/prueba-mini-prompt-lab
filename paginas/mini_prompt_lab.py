import streamlit as st
from utils.watsonx_functions import call_watsonx_text_model

st.title("Mini Prompt Lab")

modelo_seleccionado = st.selectbox("Elige el modelo que quieres utilizar", ["ibm/granite-3-3-8b-instruct","mistralai/mistral-large", "meta-llama/llama-3-3-70b-instruct", "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"])

min_tokens_seleccionados = st.number_input("Tokens de respuesta mínimos", min_value=0)

max_tokens_seleccionados = st.number_input("Tokens de respuesta máximos", min_value=0, value=200)

modo_seleccionado = st.radio("Elige un modo de decodificación", ["Greedy", "Sampling"])

if modo_seleccionado == "Sampling":
    temperature_seleccionada = st.slider("Temperature", min_value=0.00, max_value=2.00, value=0.7, step=0.01)
    top_p_seleccionado = st.slider("Top P", min_value=0.01, max_value=1.00, value=1.00, step=0.01)
    top_n_seleccionado = st.slider("Top K", min_value=1, max_value=100, value=50, step=1)
    random_seed_seleccionada = st.number_input("Random seed", min_value=1, value=None)

repetition_penalty_seleccionada = st.slider("Repetition Penalty", min_value=1.00, max_value=2.00, value=1.00, step=0.01)

prompt_del_usuario = st.text_area("Prompt", placeholder="Escribe aquí tu prompt")

boton_llamar_modelo = st.button("Llamar al modelo")

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
    
    with st.expander("Respuesta Generada ", expanded=True):
        st.write(respuesta_generada)