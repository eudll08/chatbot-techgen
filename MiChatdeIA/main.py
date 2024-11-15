import streamlit as st # type: ignore
from groq import Groq # type: ignore

clave_usuario = ""
usuario = ""
modelo_actual = ""
mensaje = ""
modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

def crear_usuario_groq():
    clave_usuario = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_usuario)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    #RETORNAMOS LA FUNCION QUE PROCESA EL MENSAJE DEL USUARIO
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
)

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_de_chat():
    contenedor_del_chat = st.container(height=400, border=True)
    with contenedor_del_chat:
        mostrar_historial()

def inicializar_estado():
    if "mensajes" not in st.session_state:
        #CREAMOS LA LISTA DE "mensajes"
        st.session_state.mensajes = []

def configurar_pagina():
    #CAMBIAR NOMBRE DE PESTAÑA
    st.set_page_config("New Chat")
    #AGREGAMOS UN TITULO
    st.title("TechGen, tu IA personal")
    #AGREGAR SIDEBAR
    st.sidebar.title("Opciones")
    m = st.sidebar.selectbox("Modelos", modelos, index = 0)
    return m

def main():
#BLOQUE DE EJECUCION
    #LLAMAMOS AL ESTADO DE MENSAJE
    inicializar_estado()
    #CREAMOS UN USUARIO A PARTIR DE LA CLAVE_API
    usuario = crear_usuario_groq()
    #CONFIGURAMOS LA PAGINA Y SELECCIONAMOS UN MODELO
    modelo_actual = configurar_pagina()
    #LLAMO AL AREA DEL CHAT
    area_de_chat()
    #CREAMOS EL CHAT BOT
    mensaje = st.chat_input("Escribí tu mensaje :D")
    #PROCESAR UNA RESPUESTA A PARTIR DE UN MODELO ELEGIDO
    if mensaje:
        actualizar_historial("user", mensaje, "🙉")
        respuesta_chat_bot = configurar_modelo(usuario, modelo_actual, mensaje)
    if respuesta_chat_bot:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(respuesta_chat_bot))
            actualizar_historial("assistant", respuesta_completa,"✨")
            
            st.rerun()

if __name__ == "__main__":
    main()
#DEPLOY