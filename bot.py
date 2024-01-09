import logging
import os
import openai
from dotenv import load_dotenv
from pyrogram import Client, filters

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de logging
logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

# Credenciales de acceso del bot
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')  # Agrega tu clave de API de OpenAI aquí

# Inicialización del cliente de Pyrogram
app = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Configuración de la clave de API de OpenAI
openai.api_key = OPENAI_API_KEY

@app.on_message(filters.command(['start']))
async def start_command(client, message):
    """
    Comando de inicio del bot
    """
    await client.send_message(message.chat.id, '¡Hola! Soy tu bot de ChatGPT. ¡Pregúntame lo que quieras!')

@app.on_message(filters.text)
async def handle_message(client, message):
    """
    Manejador de mensajes para preguntas y respuestas con OpenAI's GPT-3
    """
    user_input = message.text

    # Utiliza OpenAI's GPT-3 para generar una respuesta
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=150
        )
        bot_reply = response.choices[0].text.strip()
        await client.send_message(message.chat.id, bot_reply)
    except Exception as e:
        logging.error(f'Error en la generación de respuesta con GPT-3: {str(e)}')
        await client.send_message(message.chat.id, 'Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo más tarde.')

# Iniciar el bot de Pyrogram
app.run()
