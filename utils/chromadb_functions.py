# import chromadb
# from chromadb.utils import embedding_functions
# import torch

# #Esta linea previene que salga una advertencia en consola por un error que tiene temporalmente Streamlit con Torch.
# #No es obligatoria y no tiene relacion con la aplicacion
# torch.classes.__path__ = [] 

# #Funcion para almacenar un documento con un identificador en la coleccion "mi coleccion" de la base de datos vectorial
# def agregar_documento_bd(identificador:str, documento:str):
#     #Iniciar cliente para conectarse a la base de datos vectorial persistente
#     #La primera vez que se ejecuta esta sentencia se crea la carpeta chroma en el proyecto
#     #En es carpeta va a estar la base de datos vectorial
#     chroma_client = chromadb.PersistentClient(path="./chroma")  

#     #Definir la funcion de embedding que se va a utilizar en la coleccion de la base de datos vectorial
#     embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
#         model_name="ibm-granite/granite-embedding-278m-multilingual"
#     )

#     #Crear o acceder a la coleccion llamada "mi_coleccion" de la base de datos vectorial
#     #Se define la funcion de embedding que se va a usar en los documentos de la coleccion
#     mi_coleccion = chroma_client.get_or_create_collection(
#         name="mi_coleccion", 
#         embedding_function=embedding_function,
#         configuration={
#             "hnsw": {
#                 "space":"cosine"
#             }
#         }
#     )

#     #Se agrega el documento a la base de datos vectorial:
#     #La base de datos se encarga de almacenar el documento y el embedding calculado con la funcion definida
#     mi_coleccion.add(
#         ids=[identificador],
#         documents=[documento]
#     )


# #Funcion para consultar todos los documentos guardados en la colección llamada "mi_coleccion" en la base de datos vectorial
# def obtener_todos_los_documentos_bd():
#     #Iniciar cliente para conectarse a la base de datos vectorial persistente
#     #La primera vez que se ejecuta esta sentencia se crea la carpeta chroma en el proyecto
#     #En es carpeta va a estar la base de datos vectorial
#     chroma_client = chromadb.PersistentClient(path="./chroma")  

#     #Definir la funcion de embedding que se va a utilizar en la coleccion de la base de datos vectorial
#     embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
#         model_name="ibm-granite/granite-embedding-278m-multilingual"
#     )

#     #Crear o acceder a la coleccion llamada "mi_coleccion" de la base de datos vectorial
#     #Se define la funcion de embedding que se va a usar en los documentos de la coleccion
#     mi_coleccion = chroma_client.get_or_create_collection(
#         name="mi_coleccion", 
#         embedding_function=embedding_function,
#         configuration={
#             "hnsw": {
#                 "space":"cosine"
#             }
#         }
#     )

#     #Obtener los documentos guardados en la coleccion "mi_coleccion"
#     diccionario_documentos_guardados = mi_coleccion.get()

#     return diccionario_documentos_guardados


# #Funcion para eliminar un documento de la base de datos segun su id:
# def eliminar_documento_segun_id_bd(identificador:str):
#     #Iniciar cliente para conectarse a la base de datos vectorial persistente
#     #La primera vez que se ejecuta esta sentencia se crea la carpeta chroma en el proyecto
#     #En es carpeta va a estar la base de datos vectorial
#     chroma_client = chromadb.PersistentClient(path="./chroma")  

#     #Definir la funcion de embedding que se va a utilizar en la coleccion de la base de datos vectorial
#     embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
#         model_name="ibm-granite/granite-embedding-278m-multilingual"
#     )

#     #Crear o acceder a la coleccion llamada "mi_coleccion" de la base de datos vectorial
#     #Se define la funcion de embedding que se va a usar en los documentos de la coleccion
#     mi_coleccion = chroma_client.get_or_create_collection(
#         name="mi_coleccion", 
#         embedding_function=embedding_function,
#         configuration={
#             "hnsw": {
#                 "space":"cosine"
#             }
#         }
#     )

#     #Eliminar de la coleccion "mi_coleccion" el documento que tiene el identificador recibido
#     mi_coleccion.delete(
#         ids=[identificador]
#     )


# #Funcion que permite realizar una consulta a la base de datos vectorial y obtener la cantidad max_resultados de 
# # documentos más relevantes para la consulta realizada
# def realizar_consulta_a_la_bd(documento_consulta:str, max_resultados:int):
#     #Iniciar cliente para conectarse a la base de datos vectorial persistente
#     #La primera vez que se ejecuta esta sentencia se crea la carpeta chroma en el proyecto
#     #En es carpeta va a estar la base de datos vectorial
#     chroma_client = chromadb.PersistentClient(path="./chroma")  

#     #Definir la funcion de embedding que se va a utilizar en la coleccion de la base de datos vectorial
#     embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
#         model_name="ibm-granite/granite-embedding-278m-multilingual"
#     )

#     #Crear o acceder a la coleccion llamada "mi_coleccion" de la base de datos vectorial
#     #Se define la funcion de embedding que se va a usar en los documentos de la coleccion
#     mi_coleccion = chroma_client.get_or_create_collection(
#         name="mi_coleccion", 
#         embedding_function=embedding_function,
#         configuration={
#             "hnsw": {
#                 "space":"cosine"
#             }
#         }
#     )

#     #Obtener los documentos guardados en la coleccion "mi_coleccion"
#     documentos = mi_coleccion.query(
#         query_texts = [documento_consulta],
#         n_results=max_resultados
#     )

#     #Retornar los documentos relevantes para la consulta
#     return documentos