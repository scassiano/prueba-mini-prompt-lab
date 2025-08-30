# import streamlit as st
# from utils.watsonx_functions import call_watsonx_text_model
# from utils.chromadb_functions import *

# st.header("RAG sobre los documentos guardados")

# # En esta seccion de la aplicación se podrá realizar una consulta a un LLM que se soporta en los documentos mas relevantes
# #Para esto, primero se verifica que existan documentos guardados en la base de datos
# resultados = obtener_todos_los_documentos_bd()

# if len(resultados['documents']) > 0:
#     st.write("Aquí podrás realizar una consulta a un LLM y el modelo va a responder basandose en los 3 documentos guardados más relevantes para la pregunta que esten guardados en la base de datos vectorial. (Los documentos deben tener una distancia menor o igual a 0.5 respecto a la pregunta para ser considerados relevantes.). Si no hay documentos relevantes, el modelo responderá que no encontró información relevante para la pregunta.")

#     modelo_seleccionado = st.selectbox("Elige el modelo que quieres utilizar", ["ibm/granite-3-3-8b-instruct","mistralai/mistral-large", "meta-llama/llama-3-3-70b-instruct", "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"])

#     min_tokens_seleccionados = st.number_input("Tokens de respuesta mínimos", min_value=0)

#     max_tokens_seleccionados = st.number_input("Tokens de respuesta máximos", min_value=0, value=200)
    
#     consulta_usuario = st.text_input("Escribe tu consulta para el LLM",placeholder="Escribe tu consulta")

#     boton_consulta_llm = st.button("Consultar al LLM")
#     if boton_consulta_llm:
#         #Llamamos la funcion encargada de extraer los documentos mas relevantes para la consulta del usuario
#         documentos= realizar_consulta_a_la_bd(consulta_usuario, max_resultados=3)

#         #Se construye un string con cada uno de los documentos relevantes obtenidos
#         #Se realiza un bucle para recorrer los documentos y agregarlos a un string
#         string_documentos = ""
#         contador = 0
#         for index in range(len(documentos['ids'][0])):
#             if documentos['distances'][0][index] <= 0.5:
#                 contador += 1
#                 string_documentos += f"Apunte {contador}: {documentos['documents'][0][index]}\n\n"

#         #En caso de que no se encontró ningun apunte relevante
#         if string_documentos == "":
#             string_documentos = "No se encontraron apuntes relevantes para la pregunta"

#         #Una vez se tiene un string con todos los documentos relevantes se insertan estos documentos
#         # En el prompt final que se va a realizar al LLM
#         prompt_final =(
#            "Eres un asistente encargado de resolver preguntas del usuario basandote principalmente en los documentos que se tienen guardados sobre el tema de la pregunta del usuario\n\n"
#            "Tu objetivo es responder la pregunta del usuario basandote principalmente en la siguiente lista de documentos, "
#            "en caso de que en los documentos no haya informacion relevante para resolver la pregunta del usuario "
#            "entonces unicamente responde 'No se encontraron documentos relevantes para la pregunta' y unicamente mencionas cual fue la pregunta del usuario.\n\n"
#            "La lista de documentos es la siguiente:\n\n"
#            f"{string_documentos}"
#            f"La pregunta del usuario es la siguiente: {consulta_usuario}\n\n"
#            "Tu respuesta es:\n\n"
#         ) 

#         #Se llama al modelo del lenguaje con el prompt creado, algunos parametros dados por el usuario
#         # y el modo Greedy y Repetition Penalty de 1:
#         respuesta_llm = call_watsonx_text_model(prompt_final,id_modelo=modelo_seleccionado, min_tokens=min_tokens_seleccionados, max_tokens=max_tokens_seleccionados, modo="Greedy", repetition_penalty=1)
        
#         #Una vez armado el prompt se muestra el verdadero prompt que se realizo al LLM
#         # el cual que incluye los documentos relevantes
#         with st.expander("📄 Prompt enviado al LLM", expanded=False):
#             st.write(prompt_final)
        
#         #Se muestra la respuesta generada por el LLM
#         with st.expander("✨ Respuesta generada", expanded=True):
#             st.write_stream(respuesta_llm)

# else:
#     st.warning("No tienes documentos guardados en la base de datos, por favor agrega al menos uno para poder realizar consultas en esta pestaña")