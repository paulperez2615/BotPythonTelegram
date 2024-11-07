import os
import telebot
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Token del bot
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Configuración de conexión a la base de datos
db_config = {
    'host': os.getenv('MYSQLHOST'),
    'database': os.getenv('MYSQLDATABASE'),
    'user': os.getenv('MYSQLUSER'),
    'password': os.getenv('MYSQLPASSWORD'),
    'port': os.getenv('MYSQLPORT')
}

# Comando de bienvenida
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el bot de Aerolínea Benjíro. Puedes usar el comando /buscar para encontrar vuelos.")

# Comando para buscar vuelos
@bot.message_handler(commands=['buscar'])
def buscar_vuelos(message):
    # Obtener el texto después del comando para usarlo como criterio de búsqueda
    parametros = message.text.split()[1:]  # Separar origen y destino
    if len(parametros) < 2:
        bot.reply_to(message, "Por favor, ingresa el origen y el destino en el formato: /buscar [origen] [destino]")
        return

    origen, destino = parametros[0], parametros[1]

    # Conectar a la base de datos
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Realizar la consulta
        query = "SELECT * FROM vuelos WHERE origen = %s AND destino = %s"
        cursor.execute(query, (origen, destino))
        resultados = cursor.fetchall()

        # Verificar si hay resultados
        if resultados:
            for vuelo in resultados:
                respuesta = (
                    f"Vuelo ID: {vuelo['id']}\n"
                    f"Origen: {vuelo['origen']}\n"
                    f"Destino: {vuelo['destino']}\n"
                    f"Fecha: {vuelo['fecha']}\n"
                    f"Precio: ${vuelo['precio']}\n"
                )
                bot.reply_to(message, respuesta)
        else:
            bot.reply_to(message, "No se encontraron vuelos para esos destinos.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        bot.reply_to(message, "Hubo un problema al buscar los vuelos. Inténtalo más tarde.")
    
    finally:
        cursor.close()
        conn.close()

# Manejador para otros mensajes
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "No entiendo ese comando. Usa /buscar para buscar vuelos.")

bot.polling()
