from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler,Filters
import telegram
import logging

class Main:

	def __init__(self,dispatcher):
		start_handler = CommandHandler('start',self.start)
		dispatcher.add_handler(start_handler)

		change_handler = CommandHandler('change',self.change)
		dispatcher.add_handler(change_handler)

	def start(self,bot,update):
		self.status = bot.send_message(chat_id=update.message.chat_id,parse_mode=telegram.ParseMode.MARKDOWN ,
			text="```hola```")

	def change(self,bot,update):
		self.status.edit_text(text="jeje")

updater = Updater(token='502745914:AAEM0dsBQLS4oaCmH-G7PdtChI5XUc1axW0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


Main(dispatcher)

# bucle principal del bot
updater.start_polling(clean=True,read_latency=0.5)
updater.idle()