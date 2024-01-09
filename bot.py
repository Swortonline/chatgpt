import os
import logging
from pyrogram import Client, filters
import openai

# Credenciales de acceso del bot
API_ID = "28146160"
API_HASH = "05d80a5935831931b5a16d14f8289b8c"
BOT_TOKEN = "6836340890:AAHNZC3n4sbGz06Sc1OIuw0p57UOIcOuAFA"
OPENAI_API_KEY = "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"  # Agrega tu clave de API de OpenAI aquí

# Inicialización del cliente de Pyrogram
app = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Configuración de la clave de API de OpenAI
openai.api_key = OPENAI_API_KEY

def generate_gpt_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f'Error en la generación de respuesta con GPT-3: {str(e)}')
        return 'Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo más tarde.'

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
    bot_reply = generate_gpt_response(user_input)

    # Envía la respuesta al chat
    await client.send_message(message.chat.id, bot_reply)

# Iniciar el bot de Pyrogram
app.run()
