import os
import telebot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Replace 'TELEGRAM_BOT_TOKEN' with the token you received from BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el bot de Aerolínea Benjíro. Puedes usar el comando /buscar para encontrar vuelos!.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
