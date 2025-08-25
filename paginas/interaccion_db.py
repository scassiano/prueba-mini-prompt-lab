import streamlit as st
from utils.chromadb_functions import *

st.title("Interaccion con la base de datos vectorial")

operaciones = ["Agregar un documento", "Ver documentos guardados", "Eliminar un documento", "Realizar una consulta a la base de datos"]

operacion_seleccionada = st.pills("Selecciona una operacion a realizar en la base de datos", operaciones)

if operacion_seleccionada == "Agregar un documento":
    identificador_a_agregar = st.text_input("Identificador para el documento a agregar", placeholder="Escribe aquí el identificador")
    documento_a_agregar = st.text_area("Documento a agregar", placeholder="Escribe aquí el documento que quieres agregar a la base de datos")

    boton_agregar = st.button("Agregar documento")
    if boton_agregar:
        resultados = obtener_todos_los_documentos_bd()
        if identificador_a_agregar in resultados['ids']:
            st.error("No se pudo agregar el documento debido a que ya existe un documento con el mismo identificador en la coleccion de la base de datos")
        else:
            agregar_documento_bd(identificador_a_agregar, documento_a_agregar)
            st.success("Documento agregado exitosamente a la base de datos")

elif operacion_seleccionada == "Ver documentos guardados":
    resultados = obtener_todos_los_documentos_bd()
    if len(resultados['ids']) == 0:
        st.warning("No hay documentos guardados en la base de datos")
    else:
        #Se realiza un bucle para recorrer los documentos y mostrarlos
        #Se recorre cada uno de los ids y se muestra el id en el titulo del contendor
        # y dentro del contendor se muestra el documento almacenado asociado a ese id
        for index in range(len(resultados['ids'])):
            with st.expander(f"ID: _{resultados['ids'][index]}_", expanded=False): 
                st.write(resultados['documents'][index])

elif operacion_seleccionada == "Eliminar un documento":
    #Se obtienen los documentos guardados
    resultados = obtener_todos_los_documentos_bd()

    #Se obtiene la lista de identificadores de los documentos guardados
    lista_ids = resultados['ids']

    #Se muestra la lista de identificadores en un menu tipo dropdown
    identificador_seleccionado = st.selectbox("Selecciona el identificador del documento a eliminar",lista_ids)

    #Si se selecciono un identificador
    if identificador_seleccionado is not None:
        boton_eliminar = st.button("Haz clic aquí para eliminar el documento seleccionado", on_click=eliminar_documento_segun_id_bd, args=[identificador_seleccionado])


elif operacion_seleccionada == "Realizar una consulta a la base de datos":
    #Mostar un documento en pantalla
    st.write("Escribe una consulta y observa cuales son los documentos con menor distancia al texto de la consulta")

    #Crear un text area para que el usuario pueda escribir su consulta
    texto_consulta = st.text_area("Escribe el texto con el cual realizar la consulta a la base de datos")

    #Crear un number_input para que el usuario pueda decir máximo cuantos resultados quiere obtener
    max_resultados = st.number_input("Ingresa la cantidad maxima de resultados que quieres obtener", min_value=1, value=3)

    #Crear un boton para realizar la consulta
    boton_realizar_consulta = st.button("Realizar la consulta")
    if boton_realizar_consulta:
        #Llamar la función para realizar la consulta a la base de datos
        resultados = realizar_consulta_a_la_bd(texto_consulta, max_resultados)
        #Si hubo 0 resultados, decir en pantalla
        if len(resultados['ids'][0]) == 0:
            st.warning("No se encontraron documentos")
        
        else:
            #Si hubo resultados, mostrarlos en un contenedor cada uno, indicando su id, distancia y contenido
            for index in range(len(resultados['ids'][0])):
                with st.expander(f"ID: _{resultados['ids'][0][index]}_ ↔️ Distancia respecto a la consulta: {resultados['distances'][0][index]}", expanded=False): 
                    st.write(resultados['documents'][0][index])