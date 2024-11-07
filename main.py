import os
import telebot
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variables de configuración
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MYSQL_HOST = os.getenv('MYSQLHOST')
MYSQL_DATABASE = os.getenv('MYSQLDATABASE')
MYSQL_USER = os.getenv('MYSQLUSER')
MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD')
MYSQL_PORT = os.getenv('MYSQLPORT')

bot = telebot.TeleBot(TOKEN)

# Conectar a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )

# Maneja el comando /start y /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el bot de Aerolínea Benjíro. Puedes usar el comando /buscar para encontrar vuelos!")

# Función de búsqueda de vuelos con el comando /buscar
@bot.message_handler(commands=['buscar'])
def buscar_vuelos(message):
    try:
        # Dividir el mensaje para obtener los criterios de búsqueda
        params = message.text.split()
        if len(params) < 3:
            bot.reply_to(message, "Por favor, usa el formato: /buscar <origen> <destino>")
            return

        origen = params[1]
        destino = params[2]

        # Conectar y realizar la consulta
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vuelos WHERE origen = %s AND destino = %s", (origen, destino))
        resultados = cursor.fetchall()

        if resultados:
            respuesta = "Vuelos encontrados:\n"
            for vuelo in resultados:
                respuesta += f"Origen: {vuelo['origen']}, Destino: {vuelo['destino']}, Fecha: {vuelo['fecha']}, Precio: {vuelo['precio']}\n"
        else:
            respuesta = "No se encontraron vuelos para los criterios especificados."

        bot.reply_to(message, respuesta)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        bot.reply_to(message, "Hubo un error al buscar vuelos.")
    finally:
        cursor.close()
        conn.close()

# Echo para otros mensajes
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
