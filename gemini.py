import google.generativeai as genai
import os # Para gestionar variables de entorno, una buena práctica

# --- Configuración de la API Key ---
# Es una buena práctica no poner la API Key directamente en el código.
# Para este ejemplo, la pondremos directamente, pero en proyectos reales
# la cargarías desde una variable de entorno o un archivo de configuración.
# Por ejemplo, podrías crear una variable de entorno llamada 'GEMINI_API_KEY'
# y accederla con os.getenv('GEMINI_API_KEY')
# Por simplicidad para empezar, la ponemos directo:
API_KEY = "AIzaSyA9HuSzktlo1LDmBOSpHl6qDAGKxyJ9eY8" # ¡CAMBIA ESTO POR TU CLAVE REAL!

# Configura la librería con tu API Key
genai.configure(api_key=API_KEY)

# --- Inicializar el modelo Gemini ---
# Puedes elegir diferentes modelos, 'gemini-pro' es ideal para texto
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Función para interactuar con la IA ---
def conversar_con_gemini(pregunta):
    print(f"Tú: {pregunta}")
    try:
        # Envía la pregunta al modelo Gemini
        response = model.generate_content(pregunta)

        # Imprime la respuesta de Gemini
        # Algunas respuestas pueden venir en 'parts', por eso unimos
        respuesta_gemini = "".join(part.text for part in response.parts)
        print(f"Gemini: {respuesta_gemini}")
        return respuesta_gemini
    except Exception as e:
        print(f"Error al comunicarse con Gemini: {e}")
        return None

# --- Bucle de conversación simple ---
if __name__ == "__main__":
    print("¡Hola! Estoy listo para conversar. Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú (escribe 'salir' para terminar): ")
        if user_input.lower() == 'salir':
            print("¡Hasta luego!")
            break
        conversar_con_gemini(user_input)