from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler,Filters
import logging
from clases import Tamagochi


# Clase que gestiona las respuestas a los comandos enviados
#   por el usuario
class Main:

	# Constructor
	def __init__(self,dispatcher):
		
		self.dispatcher = dispatcher

		# Manejador del comando /start
		start_handler = CommandHandler('start',self.start)
		self.dispatcher.add_handler(start_handler)

		# Manejador del comando /status
		status_handler = CommandHandler('status',self.status)
		self.dispatcher.add_handler(status_handler)

	# Metodo ejecutado al recibir el comando /start
	def start(self,bot,update):
		bot.send_message(chat_id=update.message.chat_id,text='¡Ha nacido un nuevo tamagochi!')
		self.tamagochi = Tamagochi(bot,update.message.chat_id)

	# Metodo ejecutado al recibir el comando /status
	def status(self,bot,update):
		bot.send_message(chat_id=update.message.chat_id,text=self.tamagochi.status())


######### EJECUCION PRINCIPAL
updater = Updater(token='502745914:AAEM0dsBQLS4oaCmH-G7PdtChI5XUc1axW0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# instancia del "bot"
Main(dispatcher)

# bucle principañ del bot
updater.start_polling(clean=True,read_latency=0.5)
updater.idle()