#Importar las dependencias
import os
import time
import requests

from langchain_ibm import ChatWatsonx
from langchain_core.tools import Tool
from langchain_core.tools import tool
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.tool import ToolMessage

from langchain_community.tools import YouTubeSearchTool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities import ArxivAPIWrapper


from langgraph.prebuilt import create_react_agent

#Credenciales plataforma watsonx
WATSONX_APIKEY = os.environ["WATSONX_API_KEY"]
URL = os.environ["IBM_CLOUD_URL"]
WATSONX_PROJECT_ID = os.environ["WATSONX_PROJECT_ID"]

#Credenciales openweathermap para poder acceder al clima
OPENWEATHERMAP_API_KEY = os.environ["OPENWEATHERMAP_API_KEY"]


#Definicion de herramientas

#Herramienta para busqueda del clima
weather_search_function = OpenWeatherMapAPIWrapper(openweathermap_api_key=OPENWEATHERMAP_API_KEY)
weather_search_tool = Tool(
    name="busqueda_del_clima",
    description="Get weather for a city and country code, e.g. Athens, GR",
    func=weather_search_function.run,
)

#Herramienta para busqueda en youtube
youtube_search_function = YouTubeSearchTool()
youtube_search_tool = Tool(
    name="busqueda_en_youtube",
    description="Search YouTube for video links.",
    func=youtube_search_function.run,
)

#Herramienta para la busqueda web
wrapper_duck_duck_go = DuckDuckGoSearchAPIWrapper(region="co-es", max_results=5)
duck_duck_go_search_function = DuckDuckGoSearchResults(api_wrapper=wrapper_duck_duck_go,output_format="string")
duck_duck_go_search_tool = Tool(
    name="busqueda_web",
    description="Busca información relevante y actualizada sobre un tema en la web.",
    func=duck_duck_go_search_function.run,
)


#Herramienta personalizada para calcular la suma de dos numeros
@tool
def suma_dos_numeros(a: int, b: int) -> int:
    """Siempre que necesites sumar dos numeros usa esta herramienta."""
    return a + b

#Herramienta para buscar informacion de un articulo de ArXiv
arxiv_wrapper = ArxivAPIWrapper()
arxiv_search_tool = Tool(
    name="busqueda_en_arxiv",
    description="Busca información sobre articulos u autores en ArXiv.",
    func=arxiv_wrapper.run,
)

#Herramienta personalizada que intenta obtener el contenido de una pagina web
@tool
def obtener_contenido_pagina_web(url: str) -> str:
    """Si el usuario te pide ver el contenido de una url, usa esta herramienta, pasa como argumento la url a la cual el usuario quiera acceder"""

    #Intentar consultar la pagina
    try:
        info_pagina = requests.get(url)
        texto_pagina = info_pagina.text
    except:
        #Si no se logra obtener la información
        texto_pagina = f"No se pudo obtener información de la página {url}"
    
    return texto_pagina



def call_agent_with_tools(
        messages: list, 
        amount_of_current_messages: int = 0,
        tool_clima: bool = False,
        tool_youtube: bool = False,
        tool_suma: bool = False,
        tool_web: bool = False,
        tool_arxiv: bool = False,
        tool_revision_url: bool = False):
    
    #Definir el modelo que se va a usar
    llm = ChatWatsonx(
        model_id="mistralai/mistral-small-3-1-24b-instruct-2503", #Seleccionamos el modelo que queremos usar
        url = URL,
        apikey = WATSONX_APIKEY,
        project_id = WATSONX_PROJECT_ID,
        params = {
            "decoding_method": "greedy",
            "temperature": 0,
            "min_new_tokens": 5,
            "max_new_tokens": 2000
            }
    )

    #Definir la lista de herramientas que tendra el agente
    tools = []

    if tool_clima:
        tools.append(weather_search_tool)
    if tool_youtube:
        tools.append(youtube_search_tool)
    if tool_suma:
        tools.append(suma_dos_numeros)
    if tool_web:
        tools.append(duck_duck_go_search_tool)
    if tool_arxiv:
        tools.append(arxiv_search_tool)
    if tool_revision_url:
        tools.append(obtener_contenido_pagina_web)

    #Definir el agente y las tools a las que va a tener acceso
    agent_executor = create_react_agent(llm, tools)

    #Llamar al agente con los mensajes que se tienen actualmente
    response = agent_executor.invoke({"messages": messages})

    # Se crea un contador de mensajes, solo se retornan los mensajes nuevos, no los antiguos
    contador_mensajes_en_respuesta = 0

    #Retornar los mensajes de toda la conversación generados
    for message in response["messages"]:
        contador_mensajes_en_respuesta +=1

        #Solo retornar los mensajes nuevos
        if contador_mensajes_en_respuesta > amount_of_current_messages:
            #Si es un mensaje humano
            if type(message) == HumanMessage:
                yield {"langchain_message": message, "chat_message":("user",message.content) }
                time.sleep(2) # Se agrega un tiempo de espera para dar la ilusión de tiempo

            #Si es un mensaje del modelo
            elif type(message) == AIMessage:
                if message.response_metadata.get("finish_reason", "") == "tool_calls":
                    yield {"langchain_message":message, "chat_message":("assistant", "El modelo requiere más información para responder, va a usar la herramienta **"+message.tool_calls[0]["name"]+"**.") }
                    time.sleep(4) # Se agrega un tiempo de espera para dar la ilusión de tiempo
                else:
                    yield {"langchain_message":message, "chat_message":("assistant", message.content)}

            #Si es el resultado del llamado a una herramienta
            elif type(message) == ToolMessage:
                yield {"langchain_message":message, "chat_message":("tool", f"La herramienta **{message.name}** trajo la siguiente información a la conversación: \n\n{message.content}")}
                time.sleep(4) # Se agrega un tiempo de espera para dar la ilusión de tiempo