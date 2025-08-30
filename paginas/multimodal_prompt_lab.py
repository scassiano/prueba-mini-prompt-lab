import streamlit as st 
from utils.watsonx_functions import call_watsonx_vision_model

st.header("Interacción con un LLM multimodal")

modelo_seleccionado = st.selectbox("Elige el modelo que quieres utilizar", ["meta-llama/llama-4-maverick-17b-128e-instruct-fp8", "meta-llama/llama-3-2-90b-vision-instruct","meta-llama/llama-3-2-11b-vision-instruct", "ibm/granite-vision-3-2-2b", "mistralai/mistral-small-3-1-24b-instruct-2503"]) 

max_tokens_seleccionados = st.number_input("Tokens de respuesta máximos", min_value=0, value=900)

modo_subir_imagen = st.radio("Selecciona una opcion", ["Subir imagen desde mi dispositivo", "Tomar una foto con la cámara"])

if modo_subir_imagen == "Subir imagen desde mi dispositivo":
    imagen_subida = st.file_uploader("Sube una imagen", type=["jpg","jpeg","png"])
    if imagen_subida is not None:
        with st.expander("Visualización de la imagen subida", expanded=True):
            st.image(imagen_subida)

elif modo_subir_imagen == "Tomar una foto con la cámara":
    imagen_subida = st.camera_input("Toma una foto")

if imagen_subida is not None:
    prompt_del_usuario = st.text_area("Prompt", placeholder="Escribe aquí tu prompt")
    boton_llamar_watsonx = st.button("Llamar al modelo multimodal")
    if boton_llamar_watsonx:
        respuesta_generada = call_watsonx_vision_model(
            prompt=prompt_del_usuario,
            imagen=imagen_subida,
            id_modelo=modelo_seleccionado,
            max_tokens=max_tokens_seleccionados
        )

        with st.expander("Respuesta Generada", expanded=True):
            st.write(respuesta_generada)