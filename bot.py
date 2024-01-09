import logging
import openai
from pyrogram import Client, filters
from configparser import ConfigParser

# Configuración de logging
logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

# Cargar configuración desde el archivo INI
config = ConfigParser()
config.read('config.ini')

# Credenciales de acceso del bot
API_ID = int(config.get('pyrogram', 'api_id'))
API_HASH = config.get('pyrogram', 'api_hash')
BOT_TOKEN = config.get('pyrogram', 'bot_token')
OPENAI_API_KEY = config.get('pyrogram', 'openai_api_key')

# Inicialización del cliente de Pyrogram
app = Client(
    'my_bot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode='markdown',  # Corregido el valor del parse_mode
)

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
        await client.send_message(message.chat.id, bot_reply, parse_mode='markdown')  # Corregido el valor del parse_mode
    except Exception as e:
        logging.error(f'Error en la generación de respuesta con GPT-3: {str(e)}')
        await client.send_message(message.chat.id, 'Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo más tarde.')

# Iniciar el bot de Pyrogram
app.run()
