import streamlit as st
import torch

#Esta linea previene que salga una advertencia en consola por un error que tiene temporalmente Streamlit con Torch.
#No es obligatoria y no tiene relacion con la aplicacion
torch.classes.__path__ = [] 

#Definir las páginas que va a tener la aplicacion
pagina_mini_prompt_lab = st.Page(page='./paginas/mini_prompt_lab.py', title='Mini Prompt Lab')
pagina_multimodal_prompt_lab = st.Page(page='./paginas/multimodal_prompt_lab.py', title='Multimodal Prompt Lab')
pagina_interaccion_db = st.Page(page='./paginas/interaccion_db.py', title='Interaccion con BD Vectorial')
pagina_rag = st.Page(page='./paginas/rag.py', title='RAG')

#Se pasan las paginas al st.navigation(), el cual se encarga de permitir la navegacion entre las paginas
# y mostrarlas en la barra lateral de la aplicacion
pagina_seleccionada = st.navigation([pagina_mini_prompt_lab,pagina_multimodal_prompt_lab,pagina_interaccion_db,pagina_rag])

#Se ejecuta la pagina que el usuario haya seleccionado en la barra de navegacion
pagina_seleccionada.run()