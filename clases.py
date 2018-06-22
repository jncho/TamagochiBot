#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
from threading import Thread
import time

# Clase del tamagochi encargada de almacenar los datos y de
#   generar mensajes cada cierto tiempo de su estado
class Tamagochi:

	# Constructor
	def __init__(self,bot,chat_id):

		# Informacion necesaria para enviar mensajes al usuario
		self.bot = bot
		self.chat_id = chat_id

		# Atributos de juancho
		self.nivelHambre=50
		self.nivelSed=50
		self.nivelAburrimiento=50
		self.nivelSueno=50

		# Incrementos del juego
		

		# Hilo encargado de enviar mensajes del estado del bot al usuario
		self.thread = Thread(target = self.comprueba_estado_thread)
		self.thread.start()

	# Muestra el estado de los atributos del tamagochi
	def status(self):
		
		text = 'Hambre: ' + str(self.nivelHambre) + '%\n'
		text += 'Sed: ' + str(self.nivelSed) + '%\n'
		text += 'Aburrimiento: ' + str(self.nivelAburrimiento) + '%\n'
		text += 'Sueño: ' + str(self.nivelSueno) + '%\n'

		return text

	# Cada cierto tiempo consulta los atributos del tamagochi
	#   y envia un mensaje al usuario advirtiendole
	def comprueba_estado_thread(self):
		while True:
			sleep(1)
			self.comprueba_hambre()

	# Comprueba el atributo hambre
	def comprueba_hambre(self):
		if self.nivelHambre < 10:
			self.enviar('¡O me das de comer o me MUEROO maldita sea!')
		elif self.nivelHambre < 20:
			self.enviar('¡Tengo muchísima hambre!')
		elif self.nivelHambre < 40:
			self.enviar('¡Noto un vacio en mi estómago!')
		else:
			self.enviar('Hmmm, quiero picar algo...')

	# El bot envia al chat el texto pasado por argumento
	def enviar(self,texto):
		self.bot.send_message(chat_id=self.chat_id,text=texto)