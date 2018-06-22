# -*- coding: utf-8 -*-

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

		# Manejador del comando /eat
		eat_handler = CommandHandler('eat',self.eat, pass_args=True)
		self.dispatcher.add_handler(eat_handler)

		# Manejador del comando /drink
		drink_handler = CommandHandler('drink',self.drink, pass_args=True)
		self.dispatcher.add_handler(drink_handler)

		# Manejador del comando /play
		play_handler = CommandHandler('play',self.play, pass_args=True)
		self.dispatcher.add_handler(play_handler)

		# Manejador del comando /sleep
		sleep_handler = CommandHandler('sleep',self.sleep, pass_args=True)
		self.dispatcher.add_handler(sleep_handler)

	# Metodo ejecutado al recibir el comando /start
	def start(self,bot,update):
		bot.send_message(chat_id=update.message.chat_id,text='¡Ha nacido un nuevo tamagochi!')
		self.tamagochi = Tamagochi(bot,update.message.chat_id)

	# Metodo ejecutado al recibir el comando /status
	def status(self,bot,update):
		bot.send_message(chat_id=update.message.chat_id,text=self.tamagochi.status())

	# Metodo ejecutado al recibir el comando /eat
	def eat(self,bot,update,args):
		if len(args) != 1:
			bot.send_message(chat_id=update.message.chat_id,text="Debe introducir un único numero con las unidades de comida")	
			return False
		bot.send_message(chat_id=update.message.chat_id,text=self.tamagochi.comer(int(args[0])))

	# Metodo ejecutado al recibir el comando /drink
	def drink(self,bot,update,args):
		if len(args) != 1:
			bot.send_message(chat_id=update.message.chat_id,text="Debe introducir un único numero con las unidades de comida")
			return False
		bot.send_message(chat_id=update.message.chat_id,text=self.tamagochi.beber(int(args[0])))

	# Metodo ejecutado al recibir el comando /play
	def play(self,bot,update,args):
		if len(args) != 1:
			bot.send_message(chat_id=update.message.chat_id,text="Debe introducir un único numero con las unidades de comida")
			return False
		bot.send_message(chat_id=update.message.chat_id,text=self.tamagochi.jugar(int(args[0])))

	# Metodo ejecutado al recibir el comando /sleep
	def sleep(self,bot,update,args):
		if len(args) != 1:
			bot.send_message(chat_id=update.message.chat_id,text="Debe introducir un único numero con las unidades de comida")
			return False
		bot.send_message(chat_id=update.message.chat_id,text=self.tamagochi.dormir(int(args[0])))

######### EJECUCION PRINCIPAL
updater = Updater(token='573394178:AAH4srX3a137jknT3wHQI973SoTjBivAvZE')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# instancia del "bot"
Main(dispatcher)

# bucle principal del bot
updater.start_polling(clean=True,read_latency=0.5)
updater.idle()