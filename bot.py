# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler,CallbackQueryHandler
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

		# Manejador del comando /viewtamagochi
		viewtamagochi_handler = CommandHandler('viewtamagochi',self.view_tamagochi)
		self.dispatcher.add_handler(viewtamagochi_handler)

		# Manejador de la botonera del menu
		menu_handler = CallbackQueryHandler(self.menu_botonera)
		self.dispatcher.add_handler(menu_handler)

	# Metodo ejecutado al recibir el comando /start
	def start(self,bot,update):
		bot.send_message(chat_id=update.message.chat_id,text='¡Ha nacido un nuevo tamagochi!')
		self.tamagochi = Tamagochi(bot,update.message.chat_id)

	# Metodo ejecutado al recibir el comando /status
	def status(self,bot,update):
		bot.send_message(chat_id=update.message.chat_id,text=self.tamagochi.status())

	def view_tamagochi(self,bot,update):
		try:
			bot.delete_message(chat_id=update.message.chat_id,message_id=self.tamagochi.dialogo_tamagochi.message_id)
			bot.delete_message(chat_id=update.message.chat_id,message_id=self.tamagochi.stats_tamagochi.message_id)
			self.tamagochi.crear_mensajes_estaticos()
		except e:
			self.tamagochi.crear_mensajes_estaticos()

	def menu_botonera(self,bot,update):
		if update.callback_query.data == "comida":
			self.tamagochi.actualizar_dialogo(self.tamagochi.comer(10))
		elif update.callback_query.data == "bebida":
			self.tamagochi.actualizar_dialogo(self.tamagochi.beber(10))
		elif update.callback_query.data == "jugar":
			self.tamagochi.actualizar_dialogo(self.tamagochi.jugar(10))
		elif update.callback_query.data == "dormir":
			self.tamagochi.actualizar_dialogo(self.tamagochi.dormir(10))

		return True

######### EJECUCION PRINCIPAL
updater = Updater(token='502745914:AAEM0dsBQLS4oaCmH-G7PdtChI5XUc1axW0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# instancia del "bot"
Main(dispatcher)

# bucle principal del bot
updater.start_polling(clean=True,read_latency=0.5)
updater.idle()