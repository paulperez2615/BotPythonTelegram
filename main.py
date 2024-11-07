import os
import telebot
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar el token del bot
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Maneja el comando /start y /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el bot de Aerolínea Benjíro. Puedes usar el comando /buscar_simulado para encontrar vuelos simulados.")

# Comando simulado de búsqueda de vuelos
@bot.message_handler(commands=['buscar_simulado'])
def buscar_vuelos_simulado(message):
    # Simulación de respuesta de búsqueda
    origen = "CDMX"
    destino = "Cancún"
    fecha = "2024-12-15"
    precio = "$3000 MXN"

    respuesta = (
        f"Vuelos simulados encontrados:\n"
        f"Origen: {origen}\n"
        f"Destino: {destino}\n"
        f"Fecha: {fecha}\n"
        f"Precio: {precio}"
    )

    bot.reply_to(message, respuesta)

# Echo para otros mensajes
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
