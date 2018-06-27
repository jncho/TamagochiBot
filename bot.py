# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler,CallbackQueryHandler
from telegram.ext import MessageHandler,Filters
import logging
from clases import Tamagochi
import telegram


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
		menu_handler = CallbackQueryHandler(self.menu_botonera,pattern="menu_.")
		self.dispatcher.add_handler(menu_handler)

		# Manejador de la botonera de la comida
		comida_handler = CallbackQueryHandler(self.comida_botonera,pattern="comida_.")
		self.dispatcher.add_handler(comida_handler)

		# Manejador de la botonera de la bebida
		bebida_handler = CallbackQueryHandler(self.bebida_botonera,pattern="bebida_.")
		self.dispatcher.add_handler(bebida_handler)

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
		if update.callback_query.data == "menu_comida":
			rows = list()
			for c in self.tamagochi.inventario.comidas:
				row = list()
				row.append(telegram.InlineKeyboardButton(text=c.nombre+" ("+str(c.valor)+"%)",callback_data="comida_"+str(c.id)))
				rows.append(row)
			rows.append([telegram.InlineKeyboardButton(text="Menu",callback_data="comida_menu")])
			menu_comida = telegram.InlineKeyboardMarkup(rows)
			self.tamagochi.menu_actual = menu_comida

			try:
				self.tamagochi.stats_tamagochi.edit_text(text=self.tamagochi.status(),parse_mode=telegram.ParseMode.MARKDOWN
					,reply_markup=telegram.InlineKeyboardMarkup(menu_comida))
			except Exception:
				return
			#self.tamagochi.actualizar_dialogo(self.tamagochi.comer(10))
		elif update.callback_query.data == "menu_bebida":
			rows = list()
			for b in self.tamagochi.inventario.bebidas:
				row = list()
				row.append(telegram.InlineKeyboardButton(text=b.nombre+" ("+str(b.valor)+"%)",callback_data="bebida_"+str(b.id)))
				rows.append(row)
			rows.append([telegram.InlineKeyboardButton(text="Menu",callback_data="bebida_menu")])
			menu_bebida = telegram.InlineKeyboardMarkup(rows)
			self.tamagochi.menu_actual = menu_bebida

			try:
				self.tamagochi.stats_tamagochi.edit_text(text=self.tamagochi.status(),parse_mode=telegram.ParseMode.MARKDOWN
					,reply_markup=telegram.InlineKeyboardMarkup(menu_bebida))
			except Exception:
				return


			#self.tamagochi.actualizar_dialogo(self.tamagochi.beber(10))
		elif update.callback_query.data == "menu_jugar":
			self.tamagochi.actualizar_dialogo(self.tamagochi.jugar(10))
		elif update.callback_query.data == "menu_dormir":
			self.tamagochi.actualizar_dialogo(self.tamagochi.dormir(10))

		return True

	def comida_botonera(self,bot,update):

		if (update.callback_query.data == "comida_menu"):
			self.tamagochi.menu_actual = self.tamagochi.menu
			self.tamagochi.actualizar_stats()
		elif (update.callback_query.data[:6] == "comida"):
			id_comida=int(update.callback_query.data.split('_')[1])
			comida = self.tamagochi.inventario.get_comida(id_comida)
			self.tamagochi.inventario.del_comida(id_comida)
			self.tamagochi.menu_actual.inline_keyboard.remove([br for br in self.tamagochi.menu_actual.inline_keyboard if br[0].callback_data == update.callback_query.data][0])
			self.tamagochi.actualizar_dialogo(self.tamagochi.comer(comida.valor))
	
	def bebida_botonera(self,bot,update):

		if (update.callback_query.data == "bebida_menu"):
			self.tamagochi.menu_actual = self.tamagochi.menu
			self.tamagochi.actualizar_stats()
		elif (update.callback_query.data[:6] == "bebida"):
			id_bebida=int(update.callback_query.data.split('_')[1])
			bebida = self.tamagochi.inventario.get_bebida(id_bebida)
			self.tamagochi.inventario.del_bebida(id_bebida)
			self.tamagochi.menu_actual.inline_keyboard.remove([br for br in self.tamagochi.menu_actual.inline_keyboard if br[0].callback_data == update.callback_query.data][0])
			self.tamagochi.actualizar_dialogo(self.tamagochi.beber(bebida.valor))

######### EJECUCION PRINCIPAL
updater = Updater(token='502745914:AAEM0dsBQLS4oaCmH-G7PdtChI5XUc1axW0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# instancia del "bot"
Main(dispatcher)

# bucle principal del bot
updater.start_polling(clean=True,read_latency=0.5)
updater.idle()